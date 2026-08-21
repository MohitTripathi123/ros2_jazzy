import rclpy
from rclpy.node import Node
from conveyor_interfaces.msg import BoxState, BeltCommand
from rclpy.qos import QoSProfile, ReliabilityPolicy
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

class ControlNode(Node):
    def __init__(self):
        super().__init__('control_node')
        self.declare_parameter('max_box_threshold', 7)
        self.declare_parameter('normal_speed', 1.0)
        self.declare_parameter('slow_speed', 0.5)
        
        self.max_box_threshold = self.get_parameter('max_box_threshold').value
        self.normal_speed = self.get_parameter('normal_speed').value
        self.slow_speed = self.get_parameter('slow_speed').value
        
        self.callback_group = ReentrantCallbackGroup()
        qos_profile = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        self.subscription_ = self.create_subscription(
            BoxState,
            '/box_state',
            self.box_state_callback,
            qos_profile,
            callback_group=self.callback_group
        )
        self.publisher_ = self.create_publisher(BeltCommand, '/belt_command', 10)
        self.get_logger().info('Control node has been started.')
        
    def box_state_callback(self, msg):
        box_count = msg.box_count
        overload = msg.overload
        if overload:
            speed = self.slow_speed
            self.get_logger().info(f'Box count {box_count} exceeds threshold. Slowing down belt to {speed}.')
        else:
            speed = self.normal_speed
            self.get_logger().info(f'Box count {box_count} is within threshold. Setting belt speed to {speed}.')
        speed_msg = BeltCommand()
        speed_msg.speed = speed
        self.publisher_.publish(speed_msg)      
        self.get_logger().info(f'Box Count: {box_count}, Overload: {overload}, Published belt speed: {speed}')
        
def main(args=None):
    rclpy.init(args=args)
    control_node = ControlNode()
    executor = MultiThreadedExecutor()
    executor.add_node(control_node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    control_node.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()