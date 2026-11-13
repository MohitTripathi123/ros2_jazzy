import rclpy
from rclpy.node import Node
from rclpy.qos import QoSDurabilityPolicy, QoSProfile, QoSReliabilityPolicy
from std_msgs.msg import String


class QoSTestNode(Node):
    def __init__(self):
        super().__init__('qos_publisher')
        qos_profile = QoSProfile(depth=10)
        qos_profile.durability = QoSDurabilityPolicy.TRANSIENT_LOCAL
        qos_profile.reliability = QoSReliabilityPolicy.BEST_EFFORT
        self.publisher_ = self.create_publisher(String, 'qos_topic', qos_profile)
        timer_period = 1.0  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.count = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello, QoS! Count: {self.count}'
        self.publisher_.publish(msg)
        self.count += 1
        self.get_logger().info('Publishing: "%s"' % msg.data)


def main(args=None):
    rclpy.init(args=args)
    qos_test_node = QoSTestNode()
    rclpy.spin(qos_test_node)
    qos_test_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
