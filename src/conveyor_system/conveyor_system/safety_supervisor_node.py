import rclpy
from rclpy.node import Node
from rclpy.lifecycle import LifecycleNode
from rclpy.lifecycle import State
from rclpy.lifecycle import TransitionCallbackReturn

from conveyor_interfaces.msg import BoxState, SystemAlert
from rclpy.qos import QoSProfile, ReliabilityPolicy

class SafetySupervisorNode(LifecycleNode):
    def __init__(self):
        super().__init__('safety_supervisor_node')
        self.declare_parameter('critical_threshold', 9)
        self.critical_threshold = self.get_parameter('critical_threshold').value
        
        qos_profile = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        self.subscription_ = None
        self.alert_publisher = None
        self.get_logger().info('Safety Supervisor node has been initialized.')

    def on_configure(self, state: State):
        self.get_logger().info('Configuring Safety Supervisor node...')
        
        qos_profile = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        self.subscription_ = self.create_subscription(
            BoxState,
            '/box_state',
            self.box_state_callback,
            qos_profile
        )
        self.alert_publisher = self.create_publisher(SystemAlert, '/system_alert', 10)
        
        return TransitionCallbackReturn.SUCCESS
    
    def on_activate(self, state: State):
        self.get_logger().info('Activating Safety Supervisor node...')
        return TransitionCallbackReturn.SUCCESS
    
    def on_deactivate(self, state: State):
        self.get_logger().info('Deactivating Safety Supervisor node...')
        return TransitionCallbackReturn.SUCCESS
    
    def on_cleanup(self, state: State):
        self.get_logger().info('Cleaning up Safety Supervisor node...')
        return TransitionCallbackReturn.SUCCESS
    
    def box_state_callback(self, msg: BoxState):
        if msg.box_count >= self.critical_threshold:
            alert_msg = SystemAlert()
            alert_msg.level = 'CRITICAL'
            alert_msg.message = f'Box count {msg.box_count} exceeds critical threshold!'
            if self.alert_publisher is not None:
                self.alert_publisher.publish(alert_msg)
            self.get_logger().warn(alert_msg.message)

def main(args=None):
    rclpy.init(args=args)
    safety_supervisor_node = SafetySupervisorNode()
    rclpy.spin(safety_supervisor_node)
    safety_supervisor_node.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()