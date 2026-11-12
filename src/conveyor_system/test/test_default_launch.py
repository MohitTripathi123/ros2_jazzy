"""Run the installed launch file, including its lifecycle transition wiring."""

import os
import signal
import subprocess
import time

from lifecycle_msgs.msg import State
from lifecycle_msgs.srv import GetState

import rclpy
from rclpy.context import Context
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node


def test_default_launch_activates_safety(tmp_path):
    """The shipped default launch must bring safety to ACTIVE by itself."""
    # Use a separate domain from in-process tests and terminate the whole launch
    # process group even when discovery or the assertion fails.
    domain = 180 + os.getpid() % 40
    environment = dict(os.environ, ROS_DOMAIN_ID=str(domain))
    context = Context()
    rclpy.init(context=context, domain_id=domain)
    probe = Node('launch_regression_probe', context=context)
    executor = SingleThreadedExecutor(context=context)
    executor.add_node(probe)
    client = probe.create_client(GetState, '/safety_supervisor_node/get_state')
    process = None
    log_path = tmp_path / 'conveyor-launch.log'
    try:
        with log_path.open('w') as output:
            process = subprocess.Popen(
                ['ros2', 'launch', 'conveyor_system', 'conveyor_system.launch.py'],
                env=environment, stdout=output, stderr=subprocess.STDOUT,
                start_new_session=True)
            deadline = time.monotonic() + 30.0
            active = False
            while time.monotonic() < deadline and process.poll() is None:
                if not client.wait_for_service(timeout_sec=0.2):
                    continue
                future = client.call_async(GetState.Request())
                executor.spin_until_future_complete(future, timeout_sec=1.0)
                if future.done() and future.result() is not None:
                    if future.result().current_state.id == State.PRIMARY_STATE_ACTIVE:
                        active = True
                        break
                time.sleep(0.1)
            assert active, log_path.read_text()
    finally:
        if process is not None:
            try:
                os.killpg(process.pid, signal.SIGINT)
            except ProcessLookupError:
                pass
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait(timeout=5)
        executor.shutdown()
        probe.destroy_node()
        context.shutdown()
