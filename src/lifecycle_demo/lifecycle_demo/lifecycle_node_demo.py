import rclpy
from rclpy.node import Node, ReentrantCallbackGroup
from rclpy.lifecycle import LifecycleNode
from rclpy.lifecycle import State
from rclpy.lifecycle import TransitionCallbackReturn
from std_msgs.msg import String

class ManagerNode(LifecycleNode):
    def __init__(self):
        super().__init__('managed_node')
        self.publisher = None
        self.timer = None
        self.count = 0

    def on_configure(self, state: State):
        self.get_logger().info('Configuring node...')
        self.publisher = self.create_lifecycle_publisher(String, 'lifecycle_topic', 10)
        return TransitionCallbackReturn.SUCCESS

    def on_activate(self, state: State):
        self.get_logger().info('Activating Node...')
        self.timer = self.create_timer(1.0, self.publish_message)
        return TransitionCallbackReturn.SUCCESS

    def on_deactivate(self, state: State):
        self.get_logger().info('Deactivating node...')
        if self.timer:
            self.destroy_timer(self.timer)
        return TransitionCallbackReturn.SUCCESS

    def on_cleanup(self, state: State):
        self.get_logger().info('Cleaning up node...')
        if self.publisher:
            self.destroy_publisher(self.publisher)
        return TransitionCallbackReturn.SUCCESS

    def publish_message(self):
        msg = String()
        msg.data = f'Hello from Lifecycle Node! Count: {self.count}'
        if self.publisher:
            self.publisher.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.count += 1

def main(args=None):
    rclpy.init(args=args)
    manager_node = ManagerNode()
    rclpy.spin(manager_node)
    manager_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()