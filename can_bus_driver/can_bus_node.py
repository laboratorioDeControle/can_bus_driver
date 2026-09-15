import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt8MultiArray, Bool

import can


class CanBusNode(Node):
    def __init__(self):
        super().__init__('can_bus_node')
        self.get_logger().info("Starting CanBusNode...")
        
        self._can_bus = None 
        try:
            self._can_bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=250000)
        except OSError:
            print("CanBusNode: CAN Bus not detected. CanBus in print mode...")

        self.payloads_can_tx_msg_sub = self.create_subscription(
            UInt8MultiArray,
            '/payloads_can_tx',
            self.payloads_can_tx_msg_callback,
            10)
            
        self.general_can_tx_msg_sub = self.create_subscription(
            UInt8MultiArray,
            '/general_purpose_can_tx',
            self.general_can_tx_msg_callback,
            10)

        self.actuators_can_tx_sub = self.create_subscription(
            UInt8MultiArray,
            '/actuators_can_tx',
            self.actuators_can_tx_msg_callback,
            10)
        self.get_logger().info('CanBusNode started successfully.')

    def general_can_tx_msg_callback(self, msg):
        self.send_msg(msg.data[0], msg.data[1::])

    def payloads_can_tx_msg_callback(self, msg):
        self.send_msg(0x03, msg.data)
        
    def actuators_can_tx_msg_callback(self, msg):
        self.send_msg(0x01, msg.data)
    
    def send_msg(self, msg_id: int, msg_data: list):
        can_msg = can.Message(arbitration_id=msg_id, data=msg_data, is_extended_id=False)

        if self._can_bus is not None:
            self._can_bus.send(can_msg)
        else:
            print("CanBusNode: ")
            print("  msg_id: ", msg_id)
            print("  msg_data: ", msg_data)


def main(args=None):
    rclpy.init(args=args)
    node = CanBusNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Ctrl+C detected. Shutting down safely...")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
