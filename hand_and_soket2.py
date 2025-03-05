import cv2
import mediapipe as mp
import numpy as np
import socket
import time

# ========== 🔹 UDP 소켓 설정 ==========
target_ip = "192.168.2.1"  # 로봇 IP
target_port = 43893  # 로봇 수신 포트

# 손동작별 패킷 정의
PACKETS = {
    "sit and down": b"\x02\x02\x01\x21\x00\x00\x00\x00\x00\x00", # 앞 손바닥(앉았다 일어났다)
    "stop": b"\x0b\x0c\x01\x21\x00\x00\x00\x00\x00\x00", #주먹(문워크 스탑)
    "greeting": b"\x06\x05\x01\x21\x00\x00\x00\x00\x00\x00", #손(인사)
    "dance": b"\x04\x02\x01\x21\x00\x00\x00\x00\x00\x00", # 뒷 손바닥(춤)
    "Turn": b"\x0d\x02\x01\x21\x00\x00\x00\x00\x00\x00", # 엄지 피고 왼쪽 방향(왼쪽으로 턴 점프)
    "Thumbs Up": b"\x0c\x03\x01\x21\x00\x00\x00\x00\x00\x00", # 따봉(문워크)
    "Point": b"\x03\x0c\x01\x21\x00\x00\x00\x00\x00\x00", # 검지 피고 아래(추적)
    "Point Stop": b"\x02\x0c\x01\x21\x00\x00\x00\x00\x00\x00", # 검지 끝만 접고 아래(추적 종료)
    # "jump": b"\x0b\x05\x01\x21\x00\x00\x00\x00\x00\x00" # 검지 피고 하늘로(점프)
}



# UDP 소켓 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ========== 🔹 MediaPipe Hands 설정 ==========
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# 카메라 열기
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ 카메라를 열 수 없습니다.")
    exit()

last_sent_time = 0  # 마지막으로 패킷을 보낸 시간 (초 단위)

gesture = None  # 기본값 (제스처 감지 안됨)
gesture_start_time = time.time()  # 기본값을 현재 시간으로 설정
current_gesture = None  # 현재 인식된 제스처
latest_gesture = None

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ 프레임을 읽을 수 없습니다.")
        break

    # BGR -> RGB 변환
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 손 감지
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmark_list = hand_landmarks.landmark

            index_tip = landmark_list[8]   # 검지 끝
            middle_tip = landmark_list[12]  # 중지 끝
            ring_tip = landmark_list[16]    # 약지 끝
            pinky_tip = landmark_list[20]   # 새끼손가락 끝
            palm_center = landmark_list[0]  # 손목(기준점)


            if (
                index_tip.y > landmark_list[5].y and
                middle_tip.y > landmark_list[9].y and
                ring_tip.y > landmark_list[13].y and
                pinky_tip.y > landmark_list[17].y and
                pinky_tip.y < landmark_list[0].y
            ):
                current_gesture = "stop"

            if (
                index_tip.y < landmark_list[6].y and
                middle_tip.y < landmark_list[10].y and
                ring_tip.y < landmark_list[14].y and
                pinky_tip.y < landmark_list[18].y
            ):
                thumb_tip = landmark_list[4]  
                thumb_ip = landmark_list[3]  
                palm_center = landmark_list[0]  


                if thumb_tip.x > thumb_ip.x and thumb_tip.z < palm_center.z and landmark_list[9].x > landmark_list[13].x:
                    current_gesture = "sit and down"
                else:
                    current_gesture = "dance"


            if (
                index_tip.y > landmark_list[0].y and
                middle_tip.y > landmark_list[0].y and
                ring_tip.y > landmark_list[0].y and
                pinky_tip.y > landmark_list[0].y
            ):
                current_gesture = "greeting"

            if (
                landmark_list[4].y < landmark_list[1].y and
                landmark_list[18].y > landmark_list[14].y and  
                landmark_list[14].y > landmark_list[10].y and  
                landmark_list[10].y > landmark_list[6].y and 
                landmark_list[6].y > landmark_list[4].y and
                landmark_list[20].x > landmark_list[17].x
            ):
                current_gesture = "Thumbs Up"

            if (
                landmark_list[20].x > landmark_list[17].x and
                landmark_list[8].x < landmark_list[5].x and  
                landmark_list[18].y > landmark_list[14].y and  
                landmark_list[14].y > landmark_list[10].y and  
                landmark_list[10].y > landmark_list[6].y and  
                landmark_list[6].y > landmark_list[4].y  
            ):
                current_gesture = "Turn"
            
            if (
                landmark_list[5].y < landmark_list[8].y and
                landmark_list[17].x < landmark_list[13].x and  
                landmark_list[13].x < landmark_list[9].x and  
                landmark_list[9].x < landmark_list[5].x and 
                landmark_list[5].x < landmark_list[1].x  
            ):
                current_gesture = "Point"
            
            if (
                landmark_list[8].y > landmark_list[0].y and
                landmark_list[6].y > landmark_list[8].y and
                landmark_list[17].x < landmark_list[13].x and  
                landmark_list[13].x < landmark_list[9].x and  
                landmark_list[9].x < landmark_list[5].x and 
                landmark_list[5].x < landmark_list[1].x  
            ):
                current_gesture = "Point Stop"
            
                        
            if (
                landmark_list[5].y > landmark_list[8].y and
                landmark_list[17].x < landmark_list[13].x and  
                landmark_list[13].x < landmark_list[9].x and  
                landmark_list[9].x < landmark_list[5].x and 
                landmark_list[5].x < landmark_list[1].x and
                middle_tip.y > landmark_list[9].y and
                ring_tip.y > landmark_list[13].y and
                pinky_tip.y > landmark_list[17].y and
                pinky_tip.y < landmark_list[0].y 
            ):
                current_gesture = "jump"

            

            
            if latest_gesture != current_gesture:  # 새로운 제스처가 감지되었을 때만 타이머 시작
                gesture_start_time = time.time()
                latest_gesture = current_gesture
            else:
                elapsed_time = time.time() - gesture_start_time
                if elapsed_time >= 2:
                    gesture = latest_gesture


            # 📌 **10초마다 UDP 패킷 전송**
            current_time = time.time()
            if gesture and current_time - last_sent_time >= 5:  # 10초마다 전송
                packet = PACKETS.get(gesture)
                if packet:
                    sock.sendto(packet, (target_ip, target_port))
                    print(f"✅ Sent '{gesture}' Packet ({len(packet)} bytes) to {target_ip}:{target_port}")
                    last_sent_time = current_time  # 마지막 전송 시간 업데이트
                    gesture = None

            # 화면에 제스처 표시
            cv2.putText(frame, gesture if gesture else "No Gesture", (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            if gesture: gesture = None

    # 화면 출력
    cv2.imshow("Hand Gesture Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
sock.close()
cv2.destroyAllWindows()
