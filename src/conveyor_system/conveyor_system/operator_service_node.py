"""Validate operator requests and deliver the selected mode to the controller."""

from conveyor_interfaces.srv import SetMode

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy

from std_msgs.msg import String


class OperatorServiceNode(Node):
    """Expose mode switching as a service with a retained mode topic."""

    def __init__(self, **kwargs):
        """Publish the initial mode and make the mode service available."""
        super().__init__('operator_service_node', **kwargs)
        self.current_mode = 'NORMAL'
        self.mode_publisher = self.create_publisher(
            String, '/conveyor_mode',
            QoSProfile(
                depth=1, reliability=ReliabilityPolicy.RELIABLE,
                durability=DurabilityPolicy.TRANSIENT_LOCAL,
            ),
        )
        self.mode_publisher.publish(String(data=self.current_mode))
        self.srv = self.create_service(SetMode, '/set_mode', self.set_mode_callback)
        self.get_logger().info('Operator Service node has been started.')

    def set_mode_callback(self, request, response):
        """Keep invalid requests from changing the last accepted mode."""
        mode = request.mode.strip().upper()
        if mode in ('NORMAL', 'SLOW', 'STOP'):
            self.current_mode = mode
            # Returning success alone does not change the belt. Deliver the
            # mode to the node that actually publishes BeltCommand messages.
            self.mode_publisher.publish(String(data=mode))
            response.success = True
            response.message = f'Mode set to {mode}'
            self.get_logger().info(response.message)
        else:
            response.success = False
            response.message = 'Invalid mode. Use "normal", "slow", or "stop".'
            self.get_logger().warning(response.message)
        return response


def main(args=None):
    """Run the operator service."""
    rclpy.init(args=args)
    node = OperatorServiceNode()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
