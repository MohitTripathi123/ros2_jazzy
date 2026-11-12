"""Demonstrate publication that follows the ROS lifecycle state."""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.lifecycle import LifecycleNode, State, TransitionCallbackReturn

from std_msgs.msg import String


class ManagerNode(LifecycleNode):
    """Manage a publisher and timer through repeatable lifecycle transitions."""

    def __init__(self, **kwargs):
        """Start without configured resources."""
        super().__init__('managed_node', **kwargs)
        self.publisher = None
        self.timer = None
        self.count = 0

    def on_configure(self, state: State):
        """Create the publisher without enabling publication yet."""
        self.publisher = self.create_lifecycle_publisher(String, 'lifecycle_topic', 10)
        return super().on_configure(state)

    def on_activate(self, state: State):
        """Enable the publisher before starting its periodic callback."""
        # Node transitions do not activate managed publishers unless the base
        # hook is called. Without it, publish() silently drops every message.
        result = super().on_activate(state)
        if result == TransitionCallbackReturn.SUCCESS:
            self.timer = self.create_timer(1.0, self.publish_message)
        return result

    def on_deactivate(self, state: State):
        """Stop the timer and let the base hook disable the publisher."""
        self._stop_timer()
        return super().on_deactivate(state)

    def on_cleanup(self, state: State):
        """Remove resources before the next configuration cycle."""
        result = super().on_cleanup(state)
        self._release_resources()
        return result

    def on_shutdown(self, state: State):
        """Clean up even when shutdown is requested directly from active."""
        result = super().on_shutdown(state)
        self._release_resources()
        return result

    def _stop_timer(self):
        """Clear the timer so reactivation creates only one."""
        if self.timer is not None:
            self.destroy_timer(self.timer)
            self.timer = None

    def _release_resources(self):
        """Remove the publisher from ROS and the managed-entity set."""
        self._stop_timer()
        if self.publisher is not None:
            self.destroy_lifecycle_publisher(self.publisher)
            self.publisher = None

    def publish_message(self):
        """Publish only while the managed publisher is enabled."""
        if self.publisher is None or not self.publisher.is_activated:
            return
        msg = String(data=f'Hello from Lifecycle Node! Count: {self.count}')
        self.publisher.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.count += 1


def main(args=None):
    """Run the lifecycle example."""
    rclpy.init(args=args)
    node = ManagerNode()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
