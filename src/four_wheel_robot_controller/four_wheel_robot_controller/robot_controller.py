import sys
import select
import termios
import tty

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped


class RobotController(Node):

    def __init__(self):
        super().__init__('robot_controller')

        self.publisher = self.create_publisher(
            TwistStamped,
            '/diff_drive_controller/cmd_vel',
            10
        )

        self.timer = self.create_timer(
            0.1,
            self.publish_command
        )

        self.linear_speed = 0.3
        self.angular_speed = 0.8

        self.linear = 0.0
        self.angular = 0.0

        self.settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())

        self.get_logger().info('Keyboard robot controller started!')
        self.get_logger().info('W = Forward')
        self.get_logger().info('S = Backward')
        self.get_logger().info('A = Left')
        self.get_logger().info('D = Right')
        self.get_logger().info('X = Stop')
        self.get_logger().info('Q = Quit')

    def get_key(self):

        key = None

        if select.select([sys.stdin], [], [], 0.0)[0]:
            key = sys.stdin.read(1)

        return key

    def publish_command(self):

        key = self.get_key()

        if key is not None:

            if key.lower() == 'w':
                self.linear = self.linear_speed
                self.angular = 0.0

            elif key.lower() == 's':
                self.linear = -self.linear_speed
                self.angular = 0.0

            elif key.lower() == 'a':
                self.linear = 0.0
                self.angular = self.angular_speed

            elif key.lower() == 'd':
                self.linear = 0.0
                self.angular = -self.angular_speed

            elif key.lower() == 'x':
                self.linear = 0.0
                self.angular = 0.0

            elif key.lower() == 'q':
                self.stop_robot()
                rclpy.shutdown()
                return

        msg = TwistStamped()

        msg.header.stamp = self.get_clock().now().to_msg()

        msg.twist.linear.x = self.linear
        msg.twist.angular.z = self.angular

        self.publisher.publish(msg)

    def stop_robot(self):

        msg = TwistStamped()

        msg.header.stamp = self.get_clock().now().to_msg()

        msg.twist.linear.x = 0.0
        msg.twist.angular.z = 0.0

        self.publisher.publish(msg)

    def shutdown(self):

        self.stop_robot()

        termios.tcsetattr(
            sys.stdin,
            termios.TCSADRAIN,
            self.settings
        )


def main(args=None):

    rclpy.init(args=args)

    node = RobotController()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.shutdown()
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()