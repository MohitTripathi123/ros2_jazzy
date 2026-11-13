"""Choose belt speed from operator mode and the configured box threshold."""

from threading import Lock

from conveyor_interfaces.msg import BeltCommand, BoxState

import rclpy
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import ExternalShutdownException, MultiThreadedExecutor
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy

from std_msgs.msg import String


class ControlNode(Node):
    """Combine sensor readings and operator commands in one control decision."""

    def __init__(self, **kwargs):
        """Initialize parameters and the two inputs to the controller."""
        super().__init__('control_node', **kwargs)
        self.declare_parameter('max_box_threshold', 7)
        self.declare_parameter('normal_speed', 1.0)
        self.declare_parameter('slow_speed', 0.5)
        self.max_box_threshold = self.get_parameter('max_box_threshold').value
        self.normal_speed = self.get_parameter('normal_speed').value
        self.slow_speed = self.get_parameter('slow_speed').value
        # Stay stopped until the retained operator mode arrives. DDS may
        # discover the sensor before it delivers an earlier STOP command.
        self.current_mode = 'STOP'
        self.box_count = None
        self._command_lock = Lock()
        self.callback_group = ReentrantCallbackGroup()
        self.publisher_ = self.create_publisher(BeltCommand, '/belt_command', 10)
        self.subscription_ = self.create_subscription(
            BoxState, '/box_state', self.box_state_callback,
            QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE),
            callback_group=self.callback_group,
        )
        # A late-starting controller must receive the latest mode, especially STOP.
        self.mode_subscription = self.create_subscription(
            String, '/conveyor_mode', self.mode_callback,
            QoSProfile(
                depth=1, reliability=ReliabilityPolicy.RELIABLE,
                durability=DurabilityPolicy.TRANSIENT_LOCAL,
            ),
            callback_group=self.callback_group,
        )
        self.get_logger().info('Control node has been started.')

    def box_state_callback(self, msg):
        """Update the count and apply the mode without bypassing STOP."""
        # Reentrant callbacks can overlap. Lock the update and publication so
        # a stale sensor callback cannot publish a moving command after STOP.
        with self._command_lock:
            self.box_count = msg.box_count
            self._publish_command()

    def mode_callback(self, msg):
        """Apply a valid mode immediately, without waiting for another box."""
        if msg.data not in ('NORMAL', 'SLOW', 'STOP'):
            self.get_logger().warning(f'Ignoring invalid conveyor mode: {msg.data}')
            return
        with self._command_lock:
            self.current_mode = msg.data
            self._publish_command()

    def _publish_command(self):
        """Publish while holding the command lock."""
        if self.current_mode == 'STOP':
            speed = 0.0
        elif self.box_count is None:
            return
        elif self.current_mode == 'SLOW' or self.box_count > self.max_box_threshold:
            # Use this controller's configured limit, not a sensor overload
            # flag that may have been calculated with a different threshold.
            speed = self.slow_speed
        else:
            speed = self.normal_speed
        self.publisher_.publish(BeltCommand(
            speed=float(speed), stop=self.current_mode == 'STOP',
        ))
        self.get_logger().info(
            f'Mode: {self.current_mode}, Box count: {self.box_count}, '
            f'Published belt speed: {speed}'
        )


def main(args=None):
    """Run concurrent callbacks and wait for them before releasing the node."""
    rclpy.init(args=args)
    node = ControlNode()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
