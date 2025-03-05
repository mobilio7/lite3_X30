import cv2
import mediapipe as mp
import socket
import time

# ========== 🔹 MediaPipe Hands 모델 초기화 ==========
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# 손 인식 모델 생성
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# ========== 🔹 UDP 소켓 설정 ==========
target_ip = "192.168.2.1"  # 로봇 IP
target_port = 43893  # 로봇 수신 포트

# UDP 소켓 생성 및 바인딩
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 📌 그리팅 패킷 (12바이트)
greeting_packet = b"\x06\x05\x01\x21\x00\x00\x00\x00\x00\x00"

# 손 감지 후 일정 시간 내 추가 전송 방지 (초 단위)
last_sent_time = 0
send_interval = 10  # 5초마다 한 번만 전송

# ========== 🔹 USB 카메라 열기 ==========
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ USB 카메라를 열 수 없습니다. 장치를 확인하세요.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ 프레임을 읽을 수 없습니다. 카메라 연결을 확인하세요.")
        break

    # BGR -> RGB 변환 (MediaPipe는 RGB 이미지를 사용)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 손 감지
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        print("✅ Hand Detected!")  # 손이 감지되면 출력
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # 📌 손이 감지되었을 때 UDP 패킷 전송 (5초마다 한 번만)
        current_time = time.time()
        if current_time - last_sent_time > send_interval:
            sock.sendto(greeting_packet, (target_ip, target_port))
            print(f"✅ Sent Greeting Packet ({len(greeting_packet)} bytes) to {target_ip}:{target_port}")
            last_sent_time = current_time

    # 화면에 표시
    cv2.imshow("USB Camera Hand Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 종료 처리
cap.release()
cv2.destroyAllWindows()
sock.close()
