import rclpy
from rclpy.node import Node
from conveyor_interfaces.msg import SystemAlert
from rclpy.qos import QoSProfile, ReliabilityPolicy

class LoggerNode(Node):
    def __init__(self):
        super().__init__('logger_node')
        qos_profile = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        self.subscription_ = self.create_subscription(
            SystemAlert,
            '/system_alert',
            self.alert_callback,
            qos_profile
        )
        self.get_logger().info('Logger node has been started.')

    def alert_callback(self, msg: SystemAlert):
        self.get_logger().warn(f'System Alert - Level: {msg.level}, Message: {msg.message}')
        
def main(args=None):
    rclpy.init(args=args)
    logger_node = LoggerNode()
    rclpy.spin(logger_node)
    logger_node.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()