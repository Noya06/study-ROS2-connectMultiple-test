import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class CommNode(Node):
    def __init__(self):
        super().__init__('comm_node')
        self.pub = self.create_publisher(String, 'chatter', 10)
        self.sub = self.create_subscription(String, 'chatter', self.callback, 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.count = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello {self.count} from {self.get_name()}'
        self.pub.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
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
