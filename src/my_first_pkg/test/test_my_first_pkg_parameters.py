"""Regression tests using real rclpy nodes and parameter transactions."""

import os
from pathlib import Path
import signal
import subprocess
import time

from my_first_pkg.parameter_callback_example import ParameterCallbackExampleNode
import pytest
from rcl_interfaces.msg import SetParametersResult
import rclpy
from rclpy.context import Context
from rclpy.exceptions import InvalidParameterTypeException, InvalidParameterValueException
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node
from rclpy.parameter import Parameter
from rclpy.parameter_client import AsyncParameterClient


@pytest.fixture
def context():
    """Give each test an isolated ROS context."""
    ctx = Context()
    rclpy.init(context=ctx)
    yield ctx
    rclpy.shutdown(context=ctx)


@pytest.fixture
def node(context):
    """Create the actual teaching node, not a mocked parameter implementation."""
    instance = ParameterCallbackExampleNode(context=context)
    yield instance
    instance.destroy_node()


def test_empty_parameter_callback(node):
    assert node.parameter_callback([]).successful
    assert node.set_parameters_atomically([]).successful


@pytest.mark.parametrize('value', [0.0, 3.5, 5.0])
def test_valid_updates(node, value):
    result = node.set_parameters_atomically([Parameter('robot_speed', value=value)])
    assert result.successful
    assert node.get_parameter('robot_speed').value == value


@pytest.mark.parametrize('value', [float('nan'), float('inf'), -float('inf'), -0.1, 5.1])
def test_invalid_values_leave_state_unchanged(node, value):
    result = node.set_parameters_atomically([Parameter('robot_speed', value=value)])
    assert not result.successful
    assert result.reason
    assert node.get_parameter('robot_speed').value == 1.0


@pytest.mark.parametrize('value', [1, True, 'fast'])
def test_callback_rejects_non_double(node, value):
    result = node.parameter_callback([Parameter('robot_speed', value=value)])
    assert not result.successful
    assert result.reason
    assert not node.set_parameters_atomically([
        Parameter('robot_speed', value=value)]).successful
    assert node.get_parameter('robot_speed').value == 1.0


def test_rejected_atomic_duplicates_do_not_change_state(node):
    committed = []
    node.add_post_set_parameters_callback(committed.append)
    result = node.set_parameters_atomically([
        Parameter('robot_speed', value=3.5),
        Parameter('robot_speed', value=6.0),
    ])
    assert not result.successful
    assert node.get_parameter('robot_speed').value == 1.0
    assert committed == []


def test_rejection_after_validation_does_not_change_state(node):
    def reject(params):
        return SetParametersResult(successful=False, reason='Another validator rejected it')

    # New callbacks run first: arrange our validator before the rejecting callback.
    node.add_on_set_parameters_callback(reject)
    node.remove_on_set_parameters_callback(node.parameter_callback)
    node.add_on_set_parameters_callback(node.parameter_callback)
    result = node.set_parameters_atomically([Parameter('robot_speed', value=3.5)])
    assert not result.successful
    assert node.get_parameter('robot_speed').value == 1.0


@pytest.mark.parametrize('value', [float('nan'), float('inf'), -float('inf'), -0.1, 5.1, 1])
def test_invalid_startup_overrides_fail(context, value):
    with pytest.raises((InvalidParameterValueException, InvalidParameterTypeException)):
        ParameterCallbackExampleNode(
            context=context, parameter_overrides=[Parameter('robot_speed', value=value)])


def test_valid_startup_override(context):
    instance = ParameterCallbackExampleNode(
        context=context, parameter_overrides=[Parameter('robot_speed', value=2.5)])
    try:
        assert instance.get_parameter('robot_speed').value == 2.5
    finally:
        instance.destroy_node()


def test_atomic_parameter_service(node, context):
    client_node = Node('parameter_regression_client', context=context)
    executor = SingleThreadedExecutor(context=context)
    executor.add_node(node)
    executor.add_node(client_node)
    client = AsyncParameterClient(client_node, node.get_name())
    try:
        assert client.wait_for_services(timeout_sec=5.0)
        for values, successful, expected in [
            ([2.5], True, 2.5),
            ([float('nan')], False, 2.5),
            ([3.5, 11.0], False, 2.5),
        ]:
            future = client.set_parameters_atomically([
                Parameter('robot_speed', value=value) for value in values
            ])
            executor.spin_until_future_complete(future, timeout_sec=5.0)
            assert future.done()
            assert future.result().result.successful is successful
            assert node.get_parameter('robot_speed').value == expected
    finally:
        executor.shutdown()
        client_node.destroy_node()


def test_successful_duplicate_update_uses_committed_value(node):
    result = node.set_parameters_atomically([
        Parameter('robot_speed', value=3.5),
        Parameter('robot_speed', value=2.5),
    ])
    assert result.successful
    assert node.get_parameter('robot_speed').value == 2.5


@pytest.fixture
def launch_command():
    """Use the actual launch file; the package executables must be built and sourced."""
    launch_file = Path(__file__).resolve().parents[1] / 'launch' / 'multi_node_launch.py'
    return ['ros2', 'launch', str(launch_file)]


def stop_launch(process):
    """Stop only this launch's session, escalating and always reaping its leader."""
    # Keep the leader unreaped until the last group signal. Its reserved PID prevents
    # accidentally targeting a reused process-group ID if the launch exits early.
    try:
        for sig, timeout in [(signal.SIGINT, 5.0), (signal.SIGTERM, 2.0)]:
            try:
                os.killpg(process.pid, sig)
            except ProcessLookupError:
                break
            deadline = time.monotonic() + timeout
            exited = None
            while time.monotonic() < deadline:
                exited = os.waitid(
                    os.P_PID, process.pid, os.WEXITED | os.WNOHANG | os.WNOWAIT)
                if exited is not None:
                    break
                time.sleep(0.05)
            if exited is not None:
                break
    finally:
        # The leader may have exited while one of its child nodes is still alive.
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        finally:
            process.wait(timeout=5.0)


def test_launch_integer_text_becomes_double(context, launch_command, tmp_path):
    client_node = Node('my_first_pkg_launch_regression_client', context=context)
    executor = SingleThreadedExecutor(context=context)
    executor.add_node(client_node)
    client = AsyncParameterClient(client_node, '/robot1/callback_node')
    try:
        with (tmp_path / 'launch.log').open('w') as output:
            process = subprocess.Popen(
                launch_command + ['robot_speed:=3'], stdout=output,
                stderr=subprocess.STDOUT, start_new_session=True)
            try:
                assert client.wait_for_services(timeout_sec=10.0)
                future = client.get_parameters(['robot_speed'])
                executor.spin_until_future_complete(future, timeout_sec=5.0)
                assert future.done()
                value = future.result().values[0]
                assert value.type == Parameter.Type.DOUBLE.value
                assert value.double_value == 3.0
            finally:
                stop_launch(process)
    finally:
        try:
            executor.shutdown()
        finally:
            client_node.destroy_node()


@pytest.mark.parametrize('value', ['fast', 'true', '11', 'nan', 'inf', '-1'])
def test_launch_rejects_invalid_speed(launch_command, value, tmp_path):
    with (tmp_path / 'invalid-launch.log').open('w') as output:
        process = subprocess.Popen(
            launch_command + [f'robot_speed:={value}'], stdout=output,
            stderr=subprocess.STDOUT, start_new_session=True)
        try:
            expected = ('could not convert string to float' if value in ('fast', 'true')
                        else 'robot_speed must be finite and between')
            deadline = time.monotonic() + 10.0
            log = ''
            while expected not in log and time.monotonic() < deadline:
                log = (tmp_path / 'invalid-launch.log').read_text()
                time.sleep(0.05)
            assert expected in log, log
        finally:
            stop_launch(process)
