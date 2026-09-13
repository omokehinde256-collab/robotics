#!/usr/bin/env bash
# ==============================================================================
# Shortcut Script: Launch 4-Wheeled Robot Simulation in Gazebo Sim 8.11.0
# ==============================================================================

set -e

# WSLg display configuration — required for Gazebo Sim GUI to render in WSL2
export DISPLAY=:0
export WAYLAND_DISPLAY=wayland-0
export XDG_RUNTIME_DIR=/mnt/wslg/runtime-dir
export PULSE_SERVER=/mnt/wslg/PulseServer

WORKSPACE_DIR="$HOME/four_wheel_robot_ws"

echo "======================================================"
echo "  Starting 4-Wheeled Robot Simulation (ROS 2 Jazzy)  "
echo "======================================================"

# 1. Source ROS 2 Jazzy
if [ -f "/opt/ros/jazzy/setup.bash" ]; then
    source /opt/ros/jazzy/setup.bash
else
    echo "[ERROR] ROS 2 Jazzy not found at /opt/ros/jazzy/setup.bash"
    exit 1
fi

# 2. Sync / copy workspace package if running from Windows mount
if [ -d "/mnt/c/Users/HP/robotics projects/four_wheel_robot" ]; then
    mkdir -p "$WORKSPACE_DIR/src"
    cp -ru "/mnt/c/Users/HP/robotics projects/four_wheel_robot" "$WORKSPACE_DIR/src/"
fi

# 3. Build workspace
cd "$WORKSPACE_DIR"
colcon build --packages-select four_wheel_robot --symlink-install

# 4. Source workspace overlay
source "$WORKSPACE_DIR/install/setup.bash"

# 5. Launch Simulation
echo "[INFO] Launching Gazebo Sim 8.11 and spawning robot..."
ros2 launch four_wheel_robot simulation.launch.py
