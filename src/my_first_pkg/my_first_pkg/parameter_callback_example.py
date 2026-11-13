import math

from rcl_interfaces.msg import SetParametersResult
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter


class ParameterCallbackExampleNode(Node):
    def __init__(self, **kwargs):
        super().__init__('parameter_callback_example', **kwargs)
        # Register validation before declaration so startup overrides are checked too.
        self.add_on_set_parameters_callback(self.parameter_callback)
        self.declare_parameter('robot_speed', 1.0)
        self.add_post_set_parameters_callback(self.parameters_updated)

        speed = self.get_parameter('robot_speed').value
        self.get_logger().info(f'Initial robot speed: {speed}')

    def parameter_callback(self, params):
        for param in params:
            if param.name == 'robot_speed':
                if param.type_ != Parameter.Type.DOUBLE:
                    return SetParametersResult(
                        successful=False, reason='robot_speed must be a double')
                if not math.isfinite(param.value) or not 0.0 <= param.value <= 5.0:
                    return SetParametersResult(
                        successful=False,
                        reason='robot_speed must be finite and between 0.0 and 5.0')
        return SetParametersResult(successful=True)

    def parameters_updated(self, params):
        # Validation can still be rejected by another callback. Log only after commit.
        if any(param.name == 'robot_speed' for param in params):
            speed = self.get_parameter('robot_speed').value
            self.get_logger().info(f'Parameter "robot_speed" updated to: {speed}')


def main(args=None):
    rclpy.init(args=args)
    parameter_callback_example_node = ParameterCallbackExampleNode()
    rclpy.spin(parameter_callback_example_node)
    parameter_callback_example_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
