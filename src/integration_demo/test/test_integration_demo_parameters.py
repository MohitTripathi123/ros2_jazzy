"""Regression tests using real rclpy nodes and parameter transactions."""

import time

from integration_demo.velocity_publisher import VelocityPublisher
import pytest
from rcl_interfaces.msg import SetParametersResult
import rclpy
from rclpy.context import Context
from rclpy.exceptions import InvalidParameterTypeException, InvalidParameterValueException
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node
from rclpy.parameter import Parameter
from rclpy.parameter_client import AsyncParameterClient
from std_msgs.msg import Float32


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
    instance = VelocityPublisher(context=context)
    yield instance
    instance.destroy_node()


def test_empty_parameter_callback(node):
    assert node.parameter_callback([]).successful
    assert node.set_parameters_atomically([]).successful


@pytest.mark.parametrize('value', [0.0, 3.5, 10.0])
def test_valid_updates(node, value):
    result = node.set_parameters_atomically([Parameter('robot_speed', value=value)])
    assert result.successful
    assert node.get_parameter('robot_speed').value == value
    assert node.robot_speed == value


@pytest.mark.parametrize('value', [float('nan'), float('inf'), -float('inf'), -0.1, 10.1])
def test_invalid_values_leave_state_unchanged(node, value):
    result = node.set_parameters_atomically([Parameter('robot_speed', value=value)])
    assert not result.successful
    assert result.reason
    assert node.get_parameter('robot_speed').value == 1.0
    assert node.robot_speed == 1.0


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
        Parameter('robot_speed', value=11.0),
    ])
    assert not result.successful
    assert node.get_parameter('robot_speed').value == 1.0
    assert committed == []
    assert node.robot_speed == 1.0


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
    assert node.robot_speed == 1.0


@pytest.mark.parametrize('value', [float('nan'), float('inf'), -float('inf'), -0.1, 10.1, 1])
def test_invalid_startup_overrides_fail(context, value):
    with pytest.raises((InvalidParameterValueException, InvalidParameterTypeException)):
        VelocityPublisher(
            context=context, parameter_overrides=[Parameter('robot_speed', value=value)])


def test_valid_startup_override(context):
    instance = VelocityPublisher(
        context=context, parameter_overrides=[Parameter('robot_speed', value=2.5)])
    try:
        assert instance.get_parameter('robot_speed').value == 2.5
        assert instance.robot_speed == 2.5
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
            assert node.robot_speed == expected
    finally:
        executor.shutdown()
        client_node.destroy_node()


def test_published_velocity_stays_valid_after_rejection(node, context):
    listener = Node('velocity_regression_listener', context=context)
    received = []
    listener.create_subscription(Float32, 'velocity', received.append, 10)
    executor = SingleThreadedExecutor(context=context)
    executor.add_node(node)
    executor.add_node(listener)
    try:
        assert node.set_parameters_atomically([
            Parameter('robot_speed', value=2.5)]).successful
        assert not node.set_parameters_atomically([
            Parameter('robot_speed', value=float('nan'))]).successful
        assert not node.set_parameters_atomically([
            Parameter('robot_speed', value=3.5),
            Parameter('robot_speed', value=11.0)]).successful
        deadline = time.monotonic() + 5.0
        while not received and time.monotonic() < deadline:
            executor.spin_once(timeout_sec=0.1)
        assert received
        assert all(message.data == 2.5 for message in received)
    finally:
        executor.shutdown()
        listener.destroy_node()


def test_successful_duplicate_update_uses_committed_value(node):
    result = node.set_parameters_atomically([
        Parameter('robot_speed', value=3.5),
        Parameter('robot_speed', value=2.5),
    ])
    assert result.successful
    assert node.get_parameter('robot_speed').value == 2.5
    assert node.robot_speed == 2.5
