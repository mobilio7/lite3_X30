import cv2
import mediapipe as mp

# MediaPipe Hands 모델 초기화
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# 손 인식 모델 생성
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# RTSP 스트림 URL (실제 RTSP 주소로 변경하세요)
rtsp_url = "rtsp://192.168.2.1:8554/test"

# RTSP 스트림 열기
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("❌ RTSP 스트림을 열 수 없습니다. 주소를 확인하세요.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ 프레임을 읽을 수 없습니다. RTSP 연결을 확인하세요.")
        break

    # BGR -> RGB 변환 (MediaPipe는 RGB 이미지를 사용)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 손 감지
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        print("✅ Hand Detected!")  # 손이 감지되면 출력
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # 화면에 표시
    cv2.imshow("RTSP Hand Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
