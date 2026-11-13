import math

from rcl_interfaces.msg import SetParametersResult
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from std_msgs.msg import Float32


class VelocityPublisher(Node):
    def __init__(self, **kwargs):
        super().__init__('velocity_publisher', **kwargs)
        # Startup overrides must pass the same checks as runtime updates.
        self.add_on_set_parameters_callback(self.parameter_callback)
        self.declare_parameter('robot_speed', 1.0)
        self.robot_speed = self.get_parameter('robot_speed').value
        self.add_post_set_parameters_callback(self.parameters_updated)
        self.publishers_ = self.create_publisher(Float32, 'velocity', 10)
        self.timer = self.create_timer(1.0, self.publish_velocity)

    def parameter_callback(self, params):
        # Validate only: changing state here would break rejected atomic updates.
        for param in params:
            if param.name == 'robot_speed':
                if param.type_ != Parameter.Type.DOUBLE:
                    return SetParametersResult(
                        successful=False, reason='robot_speed must be a double')
                if not math.isfinite(param.value) or not 0.0 <= param.value <= 10.0:
                    return SetParametersResult(
                        successful=False,
                        reason='robot_speed must be finite and between 0.0 and 10.0')
        return SetParametersResult(successful=True)

    def parameters_updated(self, params):
        # Jazzy calls this only after all validation succeeds and values are stored.
        if any(param.name == 'robot_speed' for param in params):
            self.robot_speed = self.get_parameter('robot_speed').value
            self.get_logger().info(f'Updated robot_speed to: {self.robot_speed}')

    def publish_velocity(self):
        msg = Float32()
        msg.data = self.robot_speed
        self.publishers_.publish(msg)
        self.get_logger().info(f'Published velocity: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    velocity_publisher = VelocityPublisher()
    rclpy.spin(velocity_publisher)
    velocity_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
