import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from rcl_interfaces.msg import SetParametersResult

class VelocityPublisher(Node):
    def __init__(self):
        super().__init__('velocity_publisher')
        self.declare_parameter('robot_speed', 1.0)
        self.robot_speed = self.get_parameter('robot_speed').value
        self.add_on_set_parameters_callback(self.parameter_callback)
        self.publishers_ = self.create_publisher(Float32, 'velocity', 10)
        self.timer = self.create_timer(1.0, self.publish_velocity)
    
    def parameter_callback(self, params):
        for param in params:
            if param.name == 'robot_speed':
                if param.value < 0.0 or param.value > 10.0:
                    self.get_logger().error('robot_speed cannot be negative or greater than 10.0')
                    return SetParametersResult(successful=False)
                
                self.robot_speed = param.value
                self.get_logger().info(f'Updated robot_speed to: {self.robot_speed}')
        return SetParametersResult(successful=True)
    
    def publish_velocity(self):
        msg = Float32()
        if self.robot_speed is not None:
            msg.data = float(self.robot_speed)
        else:
            self.get_logger().warn('robot_speed is None')
            return
        self.publishers_.publish(msg)
        self.get_logger().info(f'Published velocity: {msg.data}')
        
def main(args=None):
    rclpy.init(args=args)
    velocity_publisher = VelocityPublisher()
    rclpy.spin(velocity_publisher)
    velocity_publisher.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()