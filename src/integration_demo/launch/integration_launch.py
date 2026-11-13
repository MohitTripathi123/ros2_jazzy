import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory('integration_demo')
    param_file = os.path.join(pkg_share, 'config', 'params.yaml')
    robot_speed_arg = DeclareLaunchArgument(
        'robot_speed',
        default_value='1.0',
        description='Initial speed of the robot'
    )
    robot_speed = LaunchConfiguration('robot_speed')

    return LaunchDescription([
        robot_speed_arg,
        Node(
            package='integration_demo',
            executable='velocity_publisher',
            namespace='robot1',
            name='velocity_publisher',
            parameters=[param_file, {'robot_speed': robot_speed}],
            output='screen'
        ),
    ])
