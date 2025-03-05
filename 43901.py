import socket
import json
import time

# 로봇 IP
ROBOT_IP = "192.168.2.1"

# 포트 정의
PORTS = [44900, 43893]
JSON_PORT = 43901

# UDP 소켓 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 030c 패킷 (12바이트)
follow_packet = b"\x03\x0c\x01\x21\x00\x00\x00\x00\x00\x00"

# 020c 패킷 (추적 취소)
cancel_packet = b"\x02\x0c\x01\x21\x00\x00\x00\x00\x00\x00"


sock.sendto(follow_packet, (ROBOT_IP, 44900))
sock.sendto(follow_packet, (ROBOT_IP, 43893))
sock.sendto(follow_packet, (ROBOT_IP, 44900))
sock.sendto(follow_packet, (ROBOT_IP, 43893))

# JSON 패킷 생성 함수
def send_json(target_id, enabled):
    json_data = {
        "timestamp": int(time.time() * 1000),
        "sendIP": "192.168.2.90",
        "destIP": ROBOT_IP,
        "targetID": target_id,
        "enabled": enabled
    }
    json_str = json.dumps(json_data)
    sock.sendto(json_str.encode(), (ROBOT_IP, JSON_PORT))
    print(f"📤 Sent JSON: {json_str}")


# 2. 43901로 JSON 전송 (추적 요청)
send_json(target_id=1, enabled=1)

# 소켓 닫기
sock.close()
