#!/usr/bin/env bash
# ==============================================================================
# Shortcut Script: Quick Robot Diagnostics & Status Inspector
# ==============================================================================

source /opt/ros/jazzy/setup.bash
if [ -f "$HOME/four_wheel_robot_ws/install/setup.bash" ]; then
    source "$HOME/four_wheel_robot_ws/install/setup.bash"
fi

echo "======================================================"
echo " 1. ACTIVE ROS 2 NODES"
echo "======================================================"
ros2 node list

echo ""
echo "======================================================"
echo " 2. CONTROLLER MANAGER STATUS"
echo "======================================================"
ros2 control list_controllers

echo ""
echo "======================================================"
echo " 3. HARDWARE INTERFACES"
echo "======================================================"
ros2 control list_hardware_interfaces

echo ""
echo "======================================================"
echo " 4. CURRENT ODOMETRY SAMPLE"
echo "======================================================"
ros2 topic echo /diff_drive_controller/odom --once

echo ""
echo "======================================================"
echo " 5. CURRENT JOINT STATES SAMPLE"
echo "======================================================"
ros2 topic echo /joint_states --once
