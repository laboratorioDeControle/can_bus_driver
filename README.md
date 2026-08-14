# CAN Bus Driver

A ROS 2 package that provides an interface to communicate with devices over the CAN bus.

## Topics

### `/payloads_can_tx`
- **Type**: `std_msgs/UInt8MultiArray`
- **Message Size**: 6 bytes
- **CAN ID**: 0x03
- **Function**: Controls 3 relays. Byte pairs (0,3), (1,4), and (2,5) enable relays 1, 2, and 3 respectively when set to 1. The first 3 bytes trigger the relays, while the last 3 bytes indicate which relay will be updated.

### `/actuators_can_tx`
- **Type**: `std_msgs/UInt8MultiArray`
- **Message Size**: 7 bytes
- **CAN ID**: 0x01
- **Function**: Controls 4 servo motors and 1 motor. 
  - Bytes 0-3: Servo motor signals (0-255 range)
  - Byte 4: Motor direction
  - Byte 5: Motor speed
  - Byte 6: Motor enable

### `/general_purpose_can_tx`
- **Type**: `std_msgs/UInt8MultiArray`
- **Function**: General-purpose topic for direct CAN bus testing. First byte specifies the CAN ID, remaining bytes are the message data.

## Configuration

- **CAN Interface**: can0
- **Bus Type**: socketcan
- **Bitrate**: 250 kbps

## Usage Examples

### Enable Relay 1
```bash
ros2 topic pub --once /payloads_can_tx std_msgs/msg/UInt8MultiArray "{data: [1, 0, 0, 1, 0, 0]}"
```

### Rotate Motor at Maximum Speed
```bash
ros2 topic pub --once /actuators_can_tx std_msgs/msg/UInt8MultiArray "{data: [0, 0, 0, 0, 1, 255, 1]}"
```
