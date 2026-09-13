#!/usr/bin/env bash
# ==============================================================================
# Shortcut Script: Launch Keyboard Teleoperation Controller
# ==============================================================================

echo "======================================================"
echo "      4-Wheeled Robot Keyboard Teleoperation          "
echo "======================================================"
echo " Controls:"
echo "   i   : Forward"
echo "   ,   : Reverse"
echo "   j   : Turn Left"
echo "   l   : Turn Right"
echo "   u   : Forward Left"
echo "   o   : Forward Right"
echo "   k   : Stop"
echo "   q/z : Increase / Decrease max speed"
echo "   w/x : Increase / Decrease only linear speed"
echo "   e/c : Increase / Decrease only angular speed"
echo "======================================================"

# Source ROS 2 Jazzy underlay and workspace overlay
source /opt/ros/jazzy/setup.bash

if [ -f "$HOME/four_wheel_robot_ws/install/setup.bash" ]; then
    source "$HOME/four_wheel_robot_ws/install/setup.bash"
fi

# Run teleop_twist_keyboard publishing TwistStamped to /diff_drive_controller/cmd_vel
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p stamped:=true --remap cmd_vel:=/diff_drive_controller/cmd_vel
