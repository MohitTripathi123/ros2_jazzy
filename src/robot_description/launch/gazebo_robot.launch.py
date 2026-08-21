from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, EmitEvent, ExecuteProcess, GroupAction, LogInfo, RegisterEventHandler, SetEnvironmentVariable, TimerAction
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessExit, OnProcessStart
from launch.substitutions import Command, LaunchConfiguration, PythonExpression
from launch_ros.actions import LifecycleNode, Node
from launch_ros.event_handlers import OnStateTransition
from launch_ros.events.lifecycle import ChangeState
from launch_ros.parameter_descriptions import ParameterValue
from lifecycle_msgs.msg import Transition
from ament_index_python.packages import get_package_share_directory
import os
import subprocess
import tempfile


def generate_robot_sdf(xacro_file):
    robot_sdf_file = os.path.join(tempfile.gettempdir(), 'simple_robot.sdf')
    urdf_tmp = os.path.join(tempfile.gettempdir(), 'simple_robot.urdf')

    urdf = subprocess.check_output(['xacro', xacro_file], text=True)
    with open(urdf_tmp, 'w', encoding='utf-8') as urdf_handle:
        urdf_handle.write(urdf)

    sdf_output = subprocess.check_output(
        ['gz', 'sdf', '-p', urdf_tmp],
        stderr=subprocess.STDOUT,
        text=True,
    )
    with open(robot_sdf_file, 'w', encoding='utf-8') as sdf_handle:
        sdf_handle.write(sdf_output)

    return robot_sdf_file


def generate_launch_description():
    pkg_share = get_package_share_directory('robot_description')
    xacro_file = os.path.join(pkg_share, 'urdf', 'simple_robot.xacro')
    world_file = os.path.join(pkg_share, 'worlds', 'simple_robot_world.sdf')

    try:
        robot_sdf_file = generate_robot_sdf(xacro_file)
    except subprocess.CalledProcessError as error:
        raise RuntimeError(
            '[robot_description] Failed to generate SDF from xacro. '
            f'Command output:\n{error.output}'
        ) from error

    robot_description = ParameterValue(
        Command(['xacro ', xacro_file]),
        value_type=str
    )

    gz_verbosity = LaunchConfiguration('gz_verbosity')
    spawn_delay = LaunchConfiguration('spawn_delay')
    use_slam = LaunchConfiguration('use_slam')

    gz_sim = ExecuteProcess(
        cmd=['gz', 'sim', '-r', '-v', gz_verbosity, world_file],
        output='screen'
    )

    spawn_robot = ExecuteProcess(
        cmd=[
            'ros2', 'run', 'ros_gz_sim', 'create',
            '-world', 'default',
            '-file', robot_sdf_file,
            '-name', 'simple_robot',
            '-x', '0', '-y', '0', '-z', '0.3'
        ],
        output='screen'
    )

    gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='ros_gz_bridge',
        output='screen',
        arguments=[
            '/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry',
            '/world/default/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan',
            '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
            '/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image',
            '/camera/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo',
        ],
        remappings=[
            ('/world/default/clock', '/clock'),
        ],
    )

    unpause_gazebo = ExecuteProcess(
        cmd=[
            'gz', 'service',
            '-s', '/world/default/control',
            '--reqtype', 'gz.msgs.WorldControl',
            '--reptype', 'gz.msgs.Boolean',
            '--timeout', '3000',
            '--req', 'pause: false',
        ],
        output='screen',
    )
    cmd_vel_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='cmd_vel_bridge',
        output='screen',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
        ],
    )

    joint_state_pub = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': True}],
    )

    slam_toolbox = LifecycleNode(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        namespace='',
        parameters=[{
            'use_sim_time': True,
            'odom_frame': 'odom',
            'base_frame': 'base_link',
            'map_frame': 'map',
            'scan_topic': '/scan',
            'mode': 'mapping',
            'resolution': 0.05,
            'max_laser_range': 10.0,
        }],
    )

    slam_configure = EmitEvent(
        event=ChangeState(
            lifecycle_node_matcher=lambda node: node is slam_toolbox,
            transition_id=Transition.TRANSITION_CONFIGURE,
        )
    )

    slam_activate = RegisterEventHandler(
        OnStateTransition(
            target_lifecycle_node=slam_toolbox,
            start_state='configuring',
            goal_state='inactive',
            entities=[
                EmitEvent(
                    event=ChangeState(
                        lifecycle_node_matcher=lambda node: node is slam_toolbox,
                        transition_id=Transition.TRANSITION_ACTIVATE,
                    )
                )
            ],
        )
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'gz_verbosity',
            default_value='3',
            description='Gazebo verbosity level'
        ),
        DeclareLaunchArgument(
            'spawn_delay',
            default_value='3.0',
            description='Seconds to wait before spawning the robot'
        ),
        DeclareLaunchArgument(
            'use_slam',
            default_value='false',
            description='Set to true to run slam_toolbox for mapping; false when using nav2 with a pre-built map'
        ),
        SetEnvironmentVariable('FASTDDS_BUILTIN_TRANSPORTS', 'UDPv4'),
        LogInfo(msg=['[robot_description] world: ', world_file]),
        LogInfo(msg=['[robot_description] xacro: ', xacro_file]),
        LogInfo(msg=['[robot_description] generated sdf: ', robot_sdf_file]),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': robot_description,
                'use_sim_time': True,
            }]
        ),

        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='lidar_sensor_frame_publisher',
            output='screen',
            arguments=[
                '0', '0', '0',
                '0', '0', '0',
                'lidar_link',
                'simple_robot/base_link/lidar_sensor',
            ],
        ),

        gz_sim,
        RegisterEventHandler(
            OnProcessStart(
                target_action=gz_sim,
                on_start=[LogInfo(msg='[robot_description] Gazebo started')]
            )
        ),
        RegisterEventHandler(
            OnProcessExit(
                target_action=gz_sim,
                on_exit=[LogInfo(msg='[robot_description] Gazebo exited')]
            )
        ),

        TimerAction(
            period=spawn_delay,
            actions=[
                LogInfo(msg='[robot_description] Spawning simple_robot into Gazebo'),
                spawn_robot
            ]
        ),
        RegisterEventHandler(
            OnProcessExit(
                target_action=spawn_robot,
                on_exit=[
                    LogInfo(
                        msg='[robot_description] Spawn step finished. '
                        'If /scan is empty, inspect `gz topic -i -t /scan`.'
                    ),
                    unpause_gazebo,
                ]
            )
        ),

        gz_bridge,
        RegisterEventHandler(
            OnProcessStart(
                target_action=gz_bridge,
                on_start=[LogInfo(msg='[robot_description] ros_gz_bridge started')]
            )
        ),

        cmd_vel_bridge,
        joint_state_pub,
        GroupAction(
            condition=IfCondition(use_slam),
            actions=[
                slam_toolbox,
                slam_activate,
                slam_configure,
            ]
        ),
    ])
