"""Publish simulated counts with overload flags matching the configured limit."""

import random

from conveyor_interfaces.msg import BoxState

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy


class SensorNode(Node):
    """Simulate the conveyor's box-count sensor."""

    def __init__(self, **kwargs):
        """Use the same configurable threshold as the controller."""
        super().__init__('sensor_node', **kwargs)
        self.declare_parameter('max_box_threshold', 7)
        self.max_box_threshold = self.get_parameter('max_box_threshold').value
        qos_profile = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        self.publisher_ = self.create_publisher(BoxState, '/box_state', qos_profile)
        self.timer = self.create_timer(1.0, self.publish_box_state)
        self.get_logger().info('Sensor node has been started.')

    def publish_box_state(self):
        """Publish a simulated reading and its threshold-derived overload flag."""
        box_count = random.randint(0, 10)
        msg = BoxState()
        msg.box_count = box_count
        # Do not keep the old hard-coded limit when YAML changes the threshold.
        msg.overload = box_count > self.max_box_threshold
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published box count: {box_count}')


def main(args=None):
    """Run the simulated sensor."""
    rclpy.init(args=args)
    node = SensorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
