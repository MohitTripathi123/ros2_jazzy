import rclpy
from rclpy.node import Node
from conveyor_interfaces.srv import SetMode

class OperatorServiceNode(Node):
    def __init__(self):
        super().__init__('operator_service_node')
        self.current_mode = 'NORMAL'
        
        self.srv = self.create_service(SetMode, '/set_mode', self.set_mode_callback)
        self.get_logger().info('Operator Service node has been started.')

    def set_mode_callback(self, request, response):
        mode = request.mode.upper()
        if mode in ['NORMAL', 'SLOW', 'STOP']:
            response.success = True
            response.message = f'Mode set to {mode}'
            self.get_logger().info(response.message)
        else:
            response.success = False
            response.message = 'Invalid mode. Use "normal", "slow", or "stop".'
            self.get_logger().warn(response.message)
        return response

def main(args=None):
    rclpy.init(args=args)
    operator_service_node = OperatorServiceNode()
    rclpy.spin(operator_service_node)
    operator_service_node.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()