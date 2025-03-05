import cv2
import mediapipe as mp
import numpy as np

# MediaPipe Hands 초기화
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,  # 한 손만 감지
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# 카메라 열기
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ 카메라를 열 수 없습니다.")
    exit()

# 손 위치 저장 (인사 동작 감지용)
prev_x = None
motion_threshold = 0.05  # X축 이동 감지 기준

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ 프레임을 읽을 수 없습니다.")
        break

    # BGR -> RGB 변환
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 손 감지
    result = hands.process(rgb_frame)

    gesture = "No Gesture"  # 기본값

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmark_list = hand_landmarks.landmark

            thumb_tip = landmark_list[4]   # 엄지 끝
            index_tip = landmark_list[8]   # 검지 끝
            middle_tip = landmark_list[12]  # 중지 끝
            ring_tip = landmark_list[16]    # 약지 끝
            pinky_tip = landmark_list[20]   # 새끼손가락 끝
            palm_center = landmark_list[0]  # 손목(기준점)

            if (
                index_tip.y > landmark_list[6].y and
                middle_tip.y > landmark_list[10].y and
                ring_tip.y > landmark_list[14].y and
                pinky_tip.y > landmark_list[18].y
            ):
                gesture = "sit down"

            elif (
                index_tip.y < landmark_list[6].y and
                middle_tip.y < landmark_list[10].y and
                ring_tip.y < landmark_list[14].y and
                pinky_tip.y < landmark_list[18].y
            ):
                gesture = "stand up"

            if (
                index_tip.y < middle_tip.y and
                index_tip.y < ring_tip.y and
                index_tip.y < pinky_tip.y and
                middle_tip.y > palm_center.y and
                ring_tip.y > palm_center.y and
                pinky_tip.y > palm_center.y
            ):
                gesture = "hi"

            # 결과 출력
            cv2.putText(frame, gesture, (50, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # 화면 출력
    cv2.imshow("Hand Gesture Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
