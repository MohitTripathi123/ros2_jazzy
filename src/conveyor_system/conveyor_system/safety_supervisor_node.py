"""Monitor critical box counts only while the lifecycle node is active."""

from conveyor_interfaces.msg import BoxState, SystemAlert

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.lifecycle import LifecycleNode, State, TransitionCallbackReturn
from rclpy.qos import QoSProfile, ReliabilityPolicy


class SafetySupervisorNode(LifecycleNode):
    """Tie monitoring resources and alerts to lifecycle transitions."""

    def __init__(self, **kwargs):
        """Defer subscription and publisher creation until configuration."""
        super().__init__('safety_supervisor_node', **kwargs)
        self.declare_parameter('critical_threshold', 9)
        self.critical_threshold = self.get_parameter('critical_threshold').value
        self.subscription_ = None
        self.alert_publisher = None
        self._active = False
        self.get_logger().info('Safety Supervisor node has been initialized.')

    def on_configure(self, state: State):
        """Create one set of resources for this configured cycle."""
        self.critical_threshold = self.get_parameter('critical_threshold').value
        self.subscription_ = self.create_subscription(
            BoxState, '/box_state', self.box_state_callback,
            QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE),
        )
        self.alert_publisher = self.create_lifecycle_publisher(
            SystemAlert, '/system_alert', 10,
        )
        return super().on_configure(state)

    def on_activate(self, state: State):
        """Activate managed publishers before allowing alert processing."""
        result = super().on_activate(state)
        self._active = result == TransitionCallbackReturn.SUCCESS
        return result

    def on_deactivate(self, state: State):
        """Stop monitoring as well as disabling the managed publisher."""
        self._active = False
        return super().on_deactivate(state)

    def on_cleanup(self, state: State):
        """Release resources so reconfiguration cannot duplicate callbacks."""
        self._active = False
        result = super().on_cleanup(state)
        self._release_resources()
        return result

    def on_shutdown(self, state: State):
        """Release resources regardless of the previous lifecycle state."""
        self._active = False
        result = super().on_shutdown(state)
        self._release_resources()
        return result

    def _release_resources(self):
        """Remove ROS entities and the lifecycle publisher registration."""
        if self.subscription_ is not None:
            self.destroy_subscription(self.subscription_)
            self.subscription_ = None
        if self.alert_publisher is not None:
            self.destroy_lifecycle_publisher(self.alert_publisher)
            self.alert_publisher = None

    def box_state_callback(self, msg: BoxState):
        """Ignore queued sensor callbacks unless monitoring is active."""
        # Subscriptions are not lifecycle-managed automatically. Guard their
        # callbacks too, so inactive nodes neither publish nor log new alerts.
        if not self._active or self.alert_publisher is None:
            return
        if msg.box_count >= self.critical_threshold:
            alert = SystemAlert()
            alert.level = 'CRITICAL'
            alert.message = f'Box count {msg.box_count} exceeds critical threshold!'
            self.alert_publisher.publish(alert)
            self.get_logger().warning(alert.message)


def main(args=None):
    """Run the managed safety monitor."""
    rclpy.init(args=args)
    node = SafetySupervisorNode()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
