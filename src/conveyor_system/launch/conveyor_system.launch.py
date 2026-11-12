"""Start the conveyor and bring its safety monitor into the active state."""

from launch import LaunchDescription
from launch.actions import EmitEvent, RegisterEventHandler
from launch.event_handlers import OnProcessStart
from launch.substitutions import PathJoinSubstitution

from launch_ros.actions import LifecycleNode, Node
from launch_ros.event_handlers import OnStateTransition
from launch_ros.events.lifecycle import ChangeState
from launch_ros.substitutions import FindPackageShare

from lifecycle_msgs.msg import Transition


def generate_launch_description():
    """Configure safety after process start, then activate after configuration."""
    config = PathJoinSubstitution([
        FindPackageShare('conveyor_system'), 'config', 'system_params.yaml',
    ])
    safety = LifecycleNode(
        package='conveyor_system',
        executable='safety_supervisor_node',
        name='safety_supervisor_node',
        namespace='',
        output='screen',
        parameters=[config],
    )
    # Starting a lifecycle process alone leaves it unconfigured. Register these
    # handlers first so even a fast startup cannot miss the transition events.
    configure_safety = RegisterEventHandler(OnProcessStart(
        target_action=safety,
        on_start=[EmitEvent(event=ChangeState(
            lifecycle_node_matcher=lambda node: node is safety,
            transition_id=Transition.TRANSITION_CONFIGURE,
        ))],
    ))
    activate_safety = RegisterEventHandler(OnStateTransition(
        target_lifecycle_node=safety,
        start_state='configuring',
        goal_state='inactive',
        entities=[EmitEvent(event=ChangeState(
            lifecycle_node_matcher=lambda node: node is safety,
            transition_id=Transition.TRANSITION_ACTIVATE,
        ))],
    ))
    return LaunchDescription([
        configure_safety,
        activate_safety,
        Node(
            package='conveyor_system', executable='sensor_node',
            name='sensor_node', output='screen', parameters=[config],
        ),
        Node(
            package='conveyor_system', executable='control_node',
            name='control_node', parameters=[config],
        ),
        safety,
        Node(
            package='conveyor_system', executable='logger_node', name='logger_node',
        ),
        Node(
            package='conveyor_system', executable='operator_service_node',
            name='operator_service_node',
        ),
    ])
