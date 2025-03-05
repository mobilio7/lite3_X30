# Lite3 & X30 Remote Host Control

## Overview
This repository contains implementations for controlling Lite3 and X30 robots remotely using hand gestures and voice commands. The control systems interact with robot components via UDP and TCP communication.

## Robot System Architecture

### Lite3 LiDAR
- **Internal Computers**: 2 (Motion Host, Recognition Host)
- **Recognition Host**: Collects LiDAR data for SLAM and navigation.
- **Motion Host**: Controls robot movements via UDP packets from the Recognition Host or external controllers.

#### **External Control for Lite3**
- To send movement commands, obtain the robot's internal IP via WiFi (192.168.2.x).
- Send UDP packets to **192.168.2.1:43893**.
- Hand gesture-based control system detects gestures via a connected camera and sends appropriate motion packets to the Motion Host.

### X30
- **Internal Computers**: 3 (Motion Host, Recognition Host, Navigation Host)
- **Motion Host**: Controls robot movements (similar to Lite3).
- **Recognition Host**: Processes LiDAR data and supports SLAM & navigation.
- **Nav Host**: Provides a TCP server for external communication and control.

#### **External Control for X30**
- **Direct UDP Control**
  - Obtain the robot's internal IP via WiFi (192.168.1.x).
  - Send UDP packets to **192.168.1.103:43893**.
- **TCP-based Control via Nav Host**
  - Connect to **192.168.1.106:30000** via TCP.
  - Send pre-defined XML-based API commands to control the robot.

## Key Files

| File Name              | Description                                                   |
|------------------------|---------------------------------------------------------------|
| `hand_and_socket2`     | Hand gesture-based control for Lite3.                         |
| `hand_control_X30`     | Hand gesture-based control for X30.                           |
| `socket_speech`        | Voice recognition-based control for Lite3.                    |
| Other test files       | Packet testing, camera recognition, and API testing.         |

## Usage Instructions
1. **Connect to the robot's WiFi network** to obtain an IP.
2. **Run the appropriate control script**:
   - Lite3: `hand_and_socket2.py`
   - X30: `hand_control_X30.py`
   - Voice control for Lite3: `socket_speech.py`
3. Ensure communication protocols (UDP/TCP) are properly configured.

## Notes
- The Lite3 and X30 robots require different IP addresses and ports for control.
- The Nav Host on X30 allows for TCP-based indirect control.
- Ensure the robot’s camera system is functional for gesture-based control.

For further details, refer to the specific script implementations.

