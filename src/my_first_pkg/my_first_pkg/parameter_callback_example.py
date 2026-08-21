import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rcl_interfaces.msg import SetParametersResult

class ParameterCallbackExampleNode(Node):
    def __init__(self):
        super().__init__('parameter_callback_example')
        self.declare_parameter('robot_speed', 1.0)
        self.add_on_set_parameters_callback(self.parameter_callback)
        
        speed = self.get_parameter('robot_speed').value
        self.get_logger().info(f'Initial robot speed: {speed}')

    def parameter_callback(self, params):
        for param in params:
            if param.name == 'robot_speed':
                if param.type_ != Parameter.Type.DOUBLE:
                    self.get_logger().info(f'Parameter "robot_speed" changed to: {param.value}')
                    return SetParametersResult(successful=False, reason='Parameter "robot_speed" cannot be changed at runtime')
        
                if param.value < 0.0 or param.value > 5.0:
                    self.get_logger().error('Invalid value for "robot_speed". Must be between 0.0 and 5.0.')
                    return SetParametersResult(successful=False, reason='Invalid parameter value')
        
        self.get_logger().info(f'Parameter "{param.name}" updated to: {param.value}')
        
        return SetParametersResult(successful=True)

def main(args=None):
    rclpy.init(args=args)
    parameter_callback_example_node = ParameterCallbackExampleNode()
    rclpy.spin(parameter_callback_example_node)
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()