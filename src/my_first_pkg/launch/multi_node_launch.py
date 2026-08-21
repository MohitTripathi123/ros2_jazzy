from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.actions import GroupAction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    robot_speed_arg = DeclareLaunchArgument(
        'robot_speed',
        default_value='2.0',
        description='Initial speed of the robot'
    )
    robot_speed = LaunchConfiguration('robot_speed')
    
    enable_callback_arg = DeclareLaunchArgument(
        'enable_callback',
        default_value='true',
        description='Enable parameter callback example'
    )
    enable_callback = LaunchConfiguration('enable_callback')
    
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time'
    )
    use_sim_time = LaunchConfiguration('use_sim_time')
    
    return LaunchDescription([
        robot_speed_arg,
        enable_callback_arg,
        use_sim_time_arg,
        Node(
            package='my_first_pkg',
            executable='parameter_example',
            namespace='robot1',
            name='parameter_node',
            parameters=[{'robot_speed': robot_speed, 'use_sim_time': use_sim_time}],
            output='screen'
        ),
        Node(
            package='my_first_pkg',
            executable='parameter_callback_example',
            namespace='robot1',
            name='callback_node',
            condition=IfCondition(enable_callback),
            parameters=[{'robot_speed': robot_speed, 'use_sim_time': use_sim_time}],
            output='screen'
        ),
        ])
    