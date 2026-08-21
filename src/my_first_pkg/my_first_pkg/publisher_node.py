import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class PublishNode(Node):
    def __init__(self):
        super().__init__('publisher_node')
        self.publisher_ = self.create_publisher(String,'hello_topic',10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        
    def timer_callback(self):
        msg  = String()
        msg.data = 'Hello from ROS 2'
        self.publisher_.publish(msg)
        self.get_logger().info(msg.data)
        
def main(args=None):
    rclpy.init(args=args)
    node = PublishNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


