import rclpy
from rclpy.node import Node, ReentrantCallbackGroup
from geometry_msgs.msg import Twist
import time
from rclpy.executors import SingleThreadedExecutor, MultiThreadedExecutor
import threading

class TurtleControlNode(Node):
    def __init__(self):
        super().__init__('turtle_control')
        self.reentrant_group = ReentrantCallbackGroup()
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(1.0, self.publish_velocity, callback_group=self.reentrant_group)
        self.heavy_timer = self.create_timer(2.0, self.heavy_computation, callback_group=self.reentrant_group)
        

    def publish_velocity(self):
        self.get_logger().info('Move callback running in thread: ' + threading.current_thread().name)
        msg = Twist()
        msg.linear.x = 2.0
        #msg.angular.z = 1.0
        self.publisher_.publish(msg)
    
    def heavy_computation(self):
        self.get_logger().info('Heavy computation callback running in thread: ' + threading.current_thread().name)
        time.sleep(3)  # Simulate heavy computation
        self.get_logger().info('Heavy computation finished.')

def main(args=None):
    rclpy.init(args=args)
    turtle_control_node = TurtleControlNode()
    executor = MultiThreadedExecutor(num_threads=2)
    executor.add_node(turtle_control_node)
    executor.spin()
    turtle_control_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()