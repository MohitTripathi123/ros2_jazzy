import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import traceback

class SafeShutdownNode(Node):
    def __init__(self):
        super().__init__('safe_shutdown_node')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(1.0, self.control_loop)
        self.count = 0
        self.active = True
        self.get_logger().info('Controller initialized.')

    def control_loop(self):
        
        if self.count == 5:
            raise Exception('Simulated error for testing safe shutdown.')
        msg = Twist()
        msg.linear.x = 2.0
        self.publisher_.publish(msg)
        self.get_logger().info('Moving forward count: %d' % self.count)
        self.count += 1
        
    def stop_robot(self):
        self.get_logger().info('Stopping robot safely...')
        stop_msg = Twist()
        stop_msg.linear.x = 0.0
        stop_msg.angular.z = 0.0
        self.publisher_.publish(stop_msg)
        self.get_logger().info('Robot stopped.')
        
    def cleanup(self):
        self.destroy_timer(self.timer)
        self.destroy_node()
        self.get_logger().info('Cleanup complete.')

def main(args=None):
    rclpy.init(args=args)
    node = SafeShutdownNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard interrupt received.')
    except Exception as e:
        node.get_logger().error('Exception occurred: %s' % str(e))
        traceback.print_exc()
    finally:
        node.stop_robot()
        node.cleanup()
        rclpy.shutdown()
        print('ROS 2 shutdown complete.')

if __name__ == '__main__':
    main()


