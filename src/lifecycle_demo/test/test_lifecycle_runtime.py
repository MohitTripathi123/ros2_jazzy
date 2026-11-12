"""Check actual lifecycle publisher delivery and resource cleanup."""

import time
import uuid

from lifecycle_demo.lifecycle_node_demo import ManagerNode

import rclpy
from rclpy.context import Context
from rclpy.executors import SingleThreadedExecutor
from rclpy.lifecycle import TransitionCallbackReturn
from rclpy.node import Node

from std_msgs.msg import String


def test_manager_publishes_only_while_active_and_can_reconfigure():
    """Exercise two complete lifecycle rounds with real ROS messages."""
    context = Context()
    rclpy.init(context=context)
    executor = SingleThreadedExecutor(context=context)
    topic = '/lifecycle_regression_' + uuid.uuid4().hex
    manager = ManagerNode(context=context, cli_args=[
        '--ros-args', '-r', f'lifecycle_topic:={topic}'])
    probe = Node('lifecycle_probe', context=context)
    messages = []
    probe.create_subscription(String, topic, messages.append, 10)
    executor.add_node(manager)
    executor.add_node(probe)

    def spin(seconds):
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            executor.spin_once(timeout_sec=0.05)

    success = TransitionCallbackReturn.SUCCESS
    baseline_publishers = len(tuple(manager.publishers))
    try:
        for _ in range(2):
            assert manager.trigger_configure() == success
            assert not manager.publisher.is_activated
            spin(0.2)
            assert not messages
            for _ in range(2):
                assert manager.trigger_activate() == success
                assert manager.publisher.is_activated
                assert len(tuple(manager.timers)) == 1
                deadline = time.monotonic() + 5.0
                while not messages and time.monotonic() < deadline:
                    executor.spin_once(timeout_sec=0.05)
                assert messages, 'Active lifecycle publisher delivered no messages'
                assert messages[0].data.startswith('Hello from Lifecycle Node!')
                assert manager.trigger_deactivate() == success
                assert not manager.publisher.is_activated
                assert not tuple(manager.timers)
                spin(0.2)
                messages.clear()
                spin(1.2)
                assert not messages
            assert manager.trigger_cleanup() == success
            assert not tuple(manager.timers)
            assert len(tuple(manager.publishers)) == baseline_publishers
    finally:
        executor.shutdown()
        probe.destroy_node()
        manager.destroy_node()
        context.shutdown()
