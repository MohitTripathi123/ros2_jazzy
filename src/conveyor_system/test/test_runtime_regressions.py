"""Exercise conveyor behavior over real DDS topics and ROS services."""

import time
import uuid

from conveyor_interfaces.msg import BeltCommand, BoxState, SystemAlert
from conveyor_interfaces.srv import SetMode

from conveyor_system.control_node import ControlNode
from conveyor_system.operator_service_node import OperatorServiceNode
from conveyor_system.safety_supervisor_node import SafetySupervisorNode

import pytest

import rclpy
from rclpy.context import Context
from rclpy.executors import SingleThreadedExecutor
from rclpy.lifecycle import TransitionCallbackReturn
from rclpy.node import Node
from rclpy.parameter import Parameter


class RosGraph:
    """Keep each test's real ROS entities isolated and deterministically cleaned."""

    def __init__(self):
        """Initialize an isolated ROS graph."""
        self.context = Context()
        rclpy.init(context=self.context)
        self.executor = SingleThreadedExecutor(context=self.context)
        self.nodes = []
        prefix = '/regression_' + uuid.uuid4().hex
        self.args = ['--ros-args']
        for topic in ('box_state', 'belt_command', 'conveyor_mode',
                      'set_mode', 'system_alert'):
            self.args.extend(['-r', f'/{topic}:={prefix}/{topic}'])
        self.probe = self.add(Node, 'probe')

    def add(self, factory, *args, **kwargs):
        """Create and register a node on this executor."""
        node = factory(*args, context=self.context, cli_args=self.args, **kwargs)
        self.nodes.append(node)
        self.executor.add_node(node)
        return node

    def until(self, predicate, timeout=8.0):
        """Spin until an observable condition holds."""
        deadline = time.monotonic() + timeout
        while not predicate() and time.monotonic() < deadline:
            self.executor.spin_once(timeout_sec=0.05)
        assert predicate(), 'Timed out waiting for the ROS graph'

    def spin(self, seconds=0.3):
        """Process callbacks for a bounded observation window."""
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            self.executor.spin_once(timeout_sec=0.02)

    def close(self):
        """Release all ROS resources even after an assertion fails."""
        self.executor.shutdown()
        for node in reversed(self.nodes):
            node.destroy_node()
        self.context.shutdown()


@pytest.fixture
def graph():
    """Provide a fresh executor and remapped graph for every test."""
    instance = RosGraph()
    try:
        yield instance
    finally:
        instance.close()


def command_probe(graph):
    """Subscribe before sending commands so immediate STOP cannot be missed."""
    commands = []
    graph.probe.create_subscription(
        BeltCommand, '/belt_command', commands.append, 10)
    boxes = graph.probe.create_publisher(BoxState, '/box_state', 10)
    return commands, boxes


def set_mode(graph, client, mode):
    """Call the public service rather than invoking its callback directly."""
    graph.until(client.service_is_ready)
    future = client.call_async(SetMode.Request(mode=mode))
    graph.until(future.done)
    return future.result()


def send_box(graph, boxes, commands, count, overload, expected):
    """Wait for a new command for the exact sensor sample sent."""
    graph.until(lambda: boxes.get_subscription_count() > 0)
    before = len(commands)
    boxes.publish(BoxState(box_count=count, overload=overload))
    graph.until(lambda: len(commands) > before)
    assert commands[-1].speed == pytest.approx(expected)
    assert commands[-1].stop is (expected == 0.0)


def test_service_modes_stop_immediately_and_persist(graph):
    """Operator modes reach control, including STOP without another sample."""
    operator = graph.add(OperatorServiceNode)
    graph.add(ControlNode)
    commands, boxes = command_probe(graph)
    client = graph.probe.create_client(SetMode, '/set_mode')
    graph.until(lambda: graph.probe.count_publishers(
        graph.probe.resolve_topic_name('/belt_command')) == 1)
    graph.spin()  # Let the initial transient-local NORMAL sample drain.
    send_box(graph, boxes, commands, 2, False, 1.0)

    before = len(commands)
    assert set_mode(graph, client, 'stop').success
    graph.until(lambda: len(commands) > before and commands[-1].speed == 0.0)
    assert operator.current_mode == 'STOP'
    send_box(graph, boxes, commands, 1, False, 0.0)
    send_box(graph, boxes, commands, 20, True, 0.0)

    assert not set_mode(graph, client, 'turbo').success
    assert operator.current_mode == 'STOP'
    send_box(graph, boxes, commands, 1, False, 0.0)
    assert set_mode(graph, client, 'SLOW').success
    graph.spin()
    send_box(graph, boxes, commands, 1, False, 0.5)
    assert set_mode(graph, client, 'NORMAL').success
    graph.spin()
    send_box(graph, boxes, commands, 1, False, 1.0)
    send_box(graph, boxes, commands, 8, False, 0.5)


def test_late_controller_receives_latched_stop(graph):
    """A restarted controller must inherit STOP, not restart the belt."""
    graph.add(OperatorServiceNode)
    client = graph.probe.create_client(SetMode, '/set_mode')
    assert set_mode(graph, client, 'STOP').success
    commands, boxes = command_probe(graph)
    graph.add(ControlNode)
    graph.until(lambda: bool(commands) and commands[-1].speed == 0.0)
    send_box(graph, boxes, commands, 1, False, 0.0)


def test_controller_uses_its_configured_threshold(graph):
    """Control uses box count and its parameter, not a stale overload flag."""
    graph.add(OperatorServiceNode)
    controller = graph.add(ControlNode, parameter_overrides=[
        Parameter('max_box_threshold', value=3)])
    commands, boxes = command_probe(graph)
    graph.until(lambda: controller.current_mode == 'NORMAL')
    graph.spin()
    send_box(graph, boxes, commands, 3, True, 1.0)
    send_box(graph, boxes, commands, 4, False, 0.5)


def test_controller_stays_stopped_until_operator_mode_arrives(graph):
    """Sensor discovery before the mode publisher must never start the belt."""
    controller = graph.add(ControlNode)
    commands, boxes = command_probe(graph)
    graph.spin()
    send_box(graph, boxes, commands, 1, False, 0.0)
    before = len(commands)
    graph.add(OperatorServiceNode)
    graph.until(lambda: controller.current_mode == 'NORMAL')
    graph.until(lambda: len(commands) > before)
    assert commands[-1].speed == pytest.approx(1.0)
    assert not commands[-1].stop
    send_box(graph, boxes, commands, 2, False, 1.0)


def test_safety_lifecycle_gates_alerts_and_releases_resources(graph):
    """Inactive safety is silent and repeated configuration leaks no entities."""
    safety = graph.add(SafetySupervisorNode)
    alerts = []
    graph.probe.create_subscription(SystemAlert, '/system_alert', alerts.append, 10)
    boxes = graph.probe.create_publisher(BoxState, '/box_state', 10)
    baseline_subscriptions = len(tuple(safety.subscriptions))
    baseline_publishers = len(tuple(safety.publishers))
    success = TransitionCallbackReturn.SUCCESS
    for _ in range(2):
        assert safety.trigger_configure() == success
        graph.until(lambda: boxes.get_subscription_count() == 1)
        boxes.publish(BoxState(box_count=10, overload=True))
        graph.spin()
        assert not alerts
        assert safety.trigger_activate() == success
        assert safety.alert_publisher.is_activated
        boxes.publish(BoxState(box_count=10, overload=True))
        graph.until(lambda: len(alerts) == 1)
        assert alerts[0].level == 'CRITICAL'
        assert safety.trigger_deactivate() == success
        assert not safety.alert_publisher.is_activated
        graph.spin()
        alerts.clear()
        boxes.publish(BoxState(box_count=10, overload=True))
        graph.spin()
        assert not alerts
        assert safety.trigger_cleanup() == success
        assert len(tuple(safety.subscriptions)) == baseline_subscriptions
        assert len(tuple(safety.publishers)) == baseline_publishers
        graph.until(lambda: boxes.get_subscription_count() == 0)
