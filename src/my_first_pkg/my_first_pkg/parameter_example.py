import rclpy
from rclpy.node import Node

class ParameterExampleNode(Node):
    def __init__(self):
        super().__init__('parameter_example')
        self.declare_parameter('robot_speed', 1.0)
        self.get_logger().info('Parameter "robot_speed" declared with default value: 1.0')
        parameter = self.get_parameter('robot_speed')
        self.get_logger().info(f'Current value of "robot_speed": {parameter.value}')
        robot_speed = parameter.value
        self.get_logger().info(f'Using robot speed: {robot_speed}')

def main(args=None):
    rclpy.init(args=args)
    parameter_example_node = ParameterExampleNode()
    rclpy.spin(parameter_example_node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()