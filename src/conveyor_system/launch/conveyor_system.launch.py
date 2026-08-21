from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    config = PathJoinSubstitution([
        FindPackageShare('conveyor_system'),
        'config',
        'system_params.yaml'
    ]) 
    return LaunchDescription([
        Node(
            package='conveyor_system',
            executable='sensor_node',
            name='sensor_node',
            output='screen',
            parameters=[config]
        ),
        Node(
            package='conveyor_system',
            executable='control_node',
            name='control_node',
            parameters=[config]
        ),
        Node(
            package='conveyor_system',
            executable='safety_supervisor_node',
            name='safety_supervisor_node',
            parameters=[config]
        ),
        Node(
            package='conveyor_system',
            executable='logger_node',
            name='logger_node',
        ),
        Node(
            package='conveyor_system',
            executable='operator_service_node',
            name='operator_service_node',
        )
    ])