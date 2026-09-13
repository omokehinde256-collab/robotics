import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro


def generate_launch_description():
    pkg_four_wheel_robot = get_package_share_directory('four_wheel_robot')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    # Path to Xacro robot description
    xacro_file = os.path.join(pkg_four_wheel_robot, 'description', 'robot.urdf.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    robot_description_raw = robot_description_config.toxml()

    # Path to Gazebo Sim SDF world
    world_file = os.path.join(pkg_four_wheel_robot, 'worlds', 'four_wheel_world.sdf')

    # 1. Robot State Publisher Node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description_raw,
            'use_sim_time': True
        }]
    )

    # 2. Gazebo Sim Launch
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={
            'gz_args': f'-r {world_file}'
        }.items()
    )

    # 3. Spawn Robot in Gazebo Sim
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'four_wheel_robot',
            '-z', '0.15'
        ]
    )

    # 4. Clock Bridge (Gazebo Sim /clock -> ROS 2 /clock)
    clock_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        output='screen',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'
        ]
    )

    # 5. Spawners for Controllers (Triggered once the robot entity is created in Gazebo)
    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        output='screen',
        arguments=['joint_state_broadcaster']
    )

    diff_drive_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        output='screen',
        arguments=['diff_drive_controller']
    )

    delayed_controller_spawners = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_entity,
            on_exit=[
                joint_state_broadcaster_spawner,
                diff_drive_controller_spawner
            ]
        )
    )

    return LaunchDescription([
        node_robot_state_publisher,
        gz_sim,
        spawn_entity,
        clock_bridge,
        delayed_controller_spawners
    ])
