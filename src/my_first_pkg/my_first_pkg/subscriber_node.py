import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SubsriberNode(Node):
    def __init__(self):
        super().__init__('subsriber_node')
        self.subscription = self.create_subscription(
            String,
            'hello_topic',
            self.listner_callback,
            10,
        )

    def listner_callback(self, msg):
        self.get_logger().info(f'Received: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = SubsriberNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
