import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import socket
import platform


def get_pc_info():
    try:
        hostname = socket.gethostname()
        # get primary outward-facing IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        os_info = platform.platform()
        return f'host={hostname}, ip={ip}, os={os_info}'
    except Exception as e:
        return f'pc_info_error:{e}'


class CommNode(Node):
    def __init__(self):
        super().__init__('comm_node')
        self.pub = self.create_publisher(String, 'chatter', 10)
        self.sub = self.create_subscription(String, 'chatter', self.callback, 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.count = 0
        self.pc_info = get_pc_info()

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello {self.count} from {self.get_name()} ({self.pc_info})'
        self.pub.publish(msg)
        self.count += 1

    def callback(self, msg):
        self.get_logger().info(f'Received: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    node = CommNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
