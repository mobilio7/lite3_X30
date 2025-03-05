import cv2
import mediapipe as mp
import numpy as np
import socket
import time
import struct
from datetime import datetime
import xml.etree.ElementTree as ET


class RobotProtocol:
    def __init__(self, host='192.168.1.106', port=30000):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.sock.bind(("192.168.1.140", 43897))
        self.sock.connect((host, port))
        self.message_id = 0
        self.target_values = [0]
        self.last_value = None  
        self.at_detection_point = False  

    def create_header(self, asdu_length):
        header = struct.pack('<BBBBHH8s',
            0xeb, 0x90, 0xeb, 0x90,
            asdu_length,
            self.message_id,
            b'\x00' * 8
        )
        self.message_id = (self.message_id + 1) % 65536
        return header

    def create_query_xml(self, type_id, value):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
        <PatrolDevice>
            <Type>2</Type>
            <Command>{type_id}</Command>
            <Time>{current_time}</Time>
            <Items>
                <Value>{value}</Value>
            </Items>
        </PatrolDevice>"""
        return xml.encode('utf-8')
    
    def test(self,code,val):      
        try:
            asdu = self.create_query_xml(code,val)
            header = self.create_header(len(asdu))
            self.sock.send(header + asdu)
        except Exception as e:
            print(f"Error status: {e}")
            return None
        
#robot = RobotProtocol()

# ========== 🔹 UDP 소켓 설정 ==========
target_ip = "192.168.1.103"  # 로봇 IP
target_port = 43893  # 로봇 수신 포트


sit_or_stand = b"\x02\x02\x01\x21\x00\x00\x00\x00\x00\x00\x00\x00"


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


isSit = True
current_time = time.time()
last_sent_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ 프레임을 읽을 수 없습니다.")
        break

    # BGR -> RGB 변환
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 손 감지
    result = hands.process(rgb_frame)

    # 화면 크기 가져오기
    frame_height, frame_width, _ = frame.shape

    # 중앙 인식 범위 설정 (예: 화면 중앙 40% 영역)
    center_x_min = frame_width * 0.4
    center_x_max = frame_width * 0.6
    center_y_min = frame_height * 0.25
    center_y_max = frame_height * 0.45

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # 손목 기준점 (palm_center) 좌표 변환 (0~1 -> 픽셀 좌표)
            palm_x = int(hand_landmarks.landmark[0].x * frame_width)
            palm_y = int(hand_landmarks.landmark[0].y * frame_height)

            if center_x_min <= palm_x <= center_x_max and center_y_min <= palm_y <= center_y_max:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # 기존 손 동작 인식 코드 실행
                landmark_list = hand_landmarks.landmark

                if isSit :
                    current_time = time.time()
                    if(current_time - last_sent_time > 2):
                        print("stand")
                        sock.sendto(sit_or_stand, (target_ip, target_port))
                        last_sent_time = current_time
                        isSit = False                


                index_tip = landmark_list[8]   # 검지 끝
                middle_tip = landmark_list[12]  # 중지 끝
                ring_tip = landmark_list[16]    # 약지 끝
                pinky_tip = landmark_list[20]   # 새끼손가락 끝
                palm_center = landmark_list[0]  # 손목(기준점)

                if(index_tip.y < landmark_list[5].y and
                middle_tip.y < landmark_list[9].y and
                ring_tip.y < landmark_list[13].y and
                pinky_tip.y < landmark_list[17].y and
                landmark_list[2].y > landmark_list[5].y
                ):
                    if(landmark_list[4].x < pinky_tip.x) :
                        current_time = time.time()
                        if(current_time - last_sent_time > 2):
                            print("back")
                            #robot.test(1,0.6)
                            last_sent_time = current_time
                    elif(landmark_list[4].x > pinky_tip.x) :
                        current_time = time.time()
                        if(current_time - last_sent_time > 2):
                            print("front")
                            #robot.test(2,0.5)
                            last_sent_time = current_time
                        

                if(landmark_list[4].y < middle_tip.y):
                    if(index_tip.x > landmark_list[5].x and
                    middle_tip.x > landmark_list[9].x and
                    ring_tip.x > landmark_list[13].x and
                    pinky_tip.x > landmark_list[17].x):
                        current_time = time.time()
                        if(current_time - last_sent_time > 2):
                            print("right")
                            #robot.test(12,0.15)
                            last_sent_time = current_time
                    elif(index_tip.x < landmark_list[5].x and
                    middle_tip.x < landmark_list[9].x and
                    ring_tip.x < landmark_list[13].x and
                    pinky_tip.x < landmark_list[17].x) :
                        current_time = time.time()
                        if(current_time - last_sent_time > 2):
                            print("left")
                            #robot.test(11,0.15)
                            last_sent_time = current_time

                if(landmark_list[4].y < middle_tip.y):
                    if(index_tip.x > landmark_list[5].x and
                    middle_tip.x < landmark_list[9].x and
                    ring_tip.x < landmark_list[13].x and
                    pinky_tip.x < landmark_list[17].x):
                        current_time = time.time()
                        if(current_time - last_sent_time > 2):
                            print("turnR")
                            #robot.test(4,0.3)
                            last_sent_time = current_time
                    elif(index_tip.x < landmark_list[5].x and
                    middle_tip.x > landmark_list[9].x and
                    ring_tip.x > landmark_list[13].x and
                    pinky_tip.x > landmark_list[17].x) :
                        current_time = time.time()
                        if(current_time - last_sent_time > 2):
                            print("turnL")
                            #robot.test(3,0.3)
                            last_sent_time = current_time

                if(index_tip.y > landmark_list[5].y and
                    middle_tip.y < landmark_list[9].y and
                    ring_tip.y < landmark_list[13].y and
                    pinky_tip.y < landmark_list[17].y and
                    landmark_list[0].y < landmark_list[4].y) :
                    if not(isSit):
                        current_time = time.time()
                        if(current_time - last_sent_time > 2):
                            print("Sit")
                            sock.sendto(sit_or_stand, (target_ip, target_port))
                            last_sent_time = current_time
                            isSit = True
                
    else:
        current_time = time.time()
        if(current_time - last_sent_time > 2):
            print("Stop")
            #robot.test(14,0)
            last_sent_time = current_time

            




    # 화면 출력
    cv2.imshow("Hand Gesture Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
sock.close()
cv2.destroyAllWindows()
