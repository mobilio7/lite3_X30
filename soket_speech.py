import socket
import time
import speech_recognition as sr

# target_ip = "192.168.2.1"  # 로봇 IP lite3
target_ip = "192.168.1.103"  # 로봇 IP

target_port = 43893  # 로봇 수신 포트

# 음성 인식을 위한 Recognizer 객체 생성
recognizer = sr.Recognizer()

# 📌 그리팅 패킷 (12바이트)
go = b"\x30\x01\x01\x21\x00\x00\xff\x00\x00\x00"
back = b"\x30\x01\x01\x21\x00\x00\xff\xff\x00\x00"
left = b"\x31\x01\x01\x21\x00\x00\xf0\xff\x00\x00"
right = b"\x31\x01\x01\x21\x00\x00\x10\x00\x00\x00"
turnL = b"\x35\x01\x01\x21\x00\x00\xf0\xff\x00\x00"
turnR = b"\x35\x01\x01\x21\x00\x00\x10\x00\x00\x00"

sit_or_stand = b"\x02\x02\x01\x21\x00\x00\x00\x00\x00\x00"
moonwolkStop = b"\x0b\x0c\x01\x21\x00\x00\x00\x00\x00\x00"
greeting = b"\x06\x05\x01\x21\x00\x00\x00\x00\x00\x00"
dance = b"\x04\x02\x01\x21\x00\x00\x00\x00\x00\x00"
TurnJump = b"\x0d\x02\x01\x21\x00\x00\x00\x00\x00\x00"
moonwolk = b"\x0c\x03\x01\x21\x00\x00\x00\x00\x00\x00"
jump = b"\x0b\x05\x01\x21\x00\x00\x00\x00\x00\x00"

emergencyStop = b"\x0e\x0c\x01\x21\x00\x00\x00\x00\x00\x00"
reset = b"\x05\x0c\x01\x21\x00\x00\x00\x00\x00\x00"

# UDP 소켓 생성 및 바인딩
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


with sr.Microphone() as source:
    print("명령어를 말하세요 (예: '앉아' 또는 '일어서'):")
    audio = recognizer.listen(source)

try:
    # 음성을 텍스트로 변환 (한국어)
    command_text = recognizer.recognize_google(audio, language="ko-KR")
    print("인식된 명령어:", command_text)
    
    # 인식된 명령어에 "앉아" 또는 "일어서"가 포함되었으면 패킷 전송
    if "앉아" in command_text or "일어서" or "일어나" in command_text:
        sock.sendto(sit_or_stand, (target_ip, target_port))
    elif "손" in command_text or "인사" or "안녕" in command_text:
        sock.sendto(greeting, (target_ip, target_port))
    elif "댄스" in command_text or "문워크" in command_text:
        sock.sendto(moonwolk, (target_ip, target_port))
        time.sleep(5)
        sock.sendto(moonwolkStop, (target_ip, target_port))
    elif "뛰어" in command_text or "점프" in command_text:
        sock.sendto(jump, (target_ip, target_port))
    elif "춤" in command_text or "트위스트" in command_text:
        sock.sendto(dance, (target_ip, target_port))
    elif "돌아" in command_text or "트위스트 점프" in command_text:
        sock.sendto(TurnJump, (target_ip, target_port))
    elif "앞으로 가" in command_text or "앞으로" or "전진" in command_text:
        sock.sendto(go, (target_ip, target_port))
        time.sleep(0.5)
        sock.sendto(go, (target_ip, target_port))
    elif "뒤로 가" in command_text or "뒤로" or "후진" in command_text:
        sock.sendto(back, (target_ip, target_port))
        time.sleep(0.5)
        sock.sendto(back, (target_ip, target_port))
    elif "왼쪽으로 가" in command_text or "왼쪽" in command_text:
        sock.sendto(left, (target_ip, target_port))
        time.sleep(0.5)
        sock.sendto(left, (target_ip, target_port))
    elif "오른쪽으로 가" in command_text or "오른쪽" in command_text:
        sock.sendto(right, (target_ip, target_port))
        time.sleep(0.5)
        sock.sendto(right, (target_ip, target_port))
    elif "오른쪽으로 돌아" in command_text or "우향우" in command_text:
        sock.sendto(turnR, (target_ip, target_port))
        time.sleep(0.5)
        sock.sendto(turnR, (target_ip, target_port))
    elif "왼쪽으로 돌아" in command_text or "좌향좌" in command_text:
        sock.sendto(turnL, (target_ip, target_port))
        time.sleep(0.5)
        sock.sendto(turnL, (target_ip, target_port))
    else:
        print("명령어가 없습니다.")
except Exception as e:
    print("음성 인식 에러:", e)



