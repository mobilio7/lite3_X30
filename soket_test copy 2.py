import socket
import time

target_ip = "192.168.1.103"  #X30 3001
target_port = 43893  # 로봇 수신 포트

sit_or_stand = b"\x02\x02\x01\x21\x00\x00\x00\x00\x00\x00\x00\x00"
Low = b"\x06\x04\x01\x21\x00\x00\x00\x00\x00\x00\x00\x00"
Std = b"\x06\x04\x01\x21\x02\x00\x00\x00\x00\x00\x00\x00"
Step_or_stop = b"\x01\x02\x01\x21\x00\x00\x00\x00\x00\x00\x00\x00"
go = b"\x30\x01\x01\x21\x60\x42\x00\x00\x00\x00\x00\x00"
back = b"\x30\x01\x01\x21\x60\x42\xff\xff\x00\x00\x00\x00"
right_or_left = b"\x31\x01\x01\x21\x60\x42\x00\x00\x00\x00\x00\x00"
TurnR_or_TurnL = b"\x35\x01\x01\x21\xe2\x6b\x00\x00\x00\x00\x00\x00"
                                                                                                                
# UDP 소켓 생성 및 바인딩
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(right_or_left, (target_ip, target_port))
sock.sendto(right_or_left, (target_ip, target_port))
sock.sendto(right_or_left, (target_ip, target_port))
sock.sendto(right_or_left, (target_ip, target_port))
sock.sendto(right_or_left, (target_ip, target_port))
sock.sendto(right_or_left, (target_ip, target_port))
sock.sendto(right_or_left, (target_ip, target_port))