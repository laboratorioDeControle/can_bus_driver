import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt8MultiArray, Bool

import can


class CanBusNode(Node):
    def __init__(self):
        super().__init__('can_bus_node')

        self._can_bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=250000)

        self.arbitrary_msg_sub = self.create_subscription(
            UInt8MultiArray,
            '/write_can_msg',
            self.arbitrary_msg_callback,
            10)

        self.actuators_sub = self.create_subscription(
            UInt8MultiArray,
            '/actuators_signals',
            self.actuators_msg_callback,
            10)

    def arbitrary_msg_callback(self, msg):
        self.send_msg(msg.data[0], msg.data[1::])

    def actuators_msg_callback(self, msg):
        self.send_msg(0x01, msg.data)
    
    def send_msg(self, msg_id: int, msg_data: list):
        can_msg = can.Message(arbitration_id=msg_id, data=msg_data, is_extended_id=False)
        self._can_bus.send(can_msg)


def main(args=None):
    rclpy.init(args=args)
    node = CanBusNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Ctrl+C detectado. Encerrando com segurança...")
        node.stop_all()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()