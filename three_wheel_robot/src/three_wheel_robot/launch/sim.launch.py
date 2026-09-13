import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():

    package_name = 'three_wheel_robot'

    pkg_share = get_package_share_directory(package_name)

    xacro_file = os.path.join(
        pkg_share,
        'urdf',
        'three_wheel_robot.urdf.xacro'
    )

    controllers_file = os.path.join(
        pkg_share,
        'config',
        'controllers.yaml'
    )

    # Convert Xacro
    import xacro

    robot_description = xacro.process_file(xacro_file).toxml()

    # Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            )
        ),
        launch_arguments={
            'gz_args': '-r empty.sdf'
        }.items()
    )

    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {
                'robot_description': robot_description
            }
        ],
        output='screen'
    )

    # Spawn robot into Gazebo
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic',
            'robot_description',
            '-name',
            'three_wheel_robot',
            '-x', '0',
            '-y', '0',
            '-z', '0.2'
        ],
        output='screen'
    )

    # Joint State Broadcaster
    joint_state_broadcaster = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_state_broadcaster',
            '--param-file',
            controllers_file
        ],
        output='screen'
    )

    # Differential Drive Controller
    diff_drive_controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'diff_drive_controller',
            '--param-file',
            controllers_file
        ],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_robot,

        TimerAction(
            period=3.0,
            actions=[
                joint_state_broadcaster
            ]
        ),

        TimerAction(
            period=5.0,
            actions=[
                diff_drive_controller
            ]
        )
    ])