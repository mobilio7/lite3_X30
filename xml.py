import socket
import struct
import time
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
            asdu = self.create_query_xml(code, val)
            header = self.create_header(len(asdu))
            self.sock.send(header + asdu)
            
            response = self.sock.recv(1024)
            if len(response) < 16:
                return None
                
            asdu_response = response[16:]
            try:
                root = ET.fromstring(asdu_response)
                error_code_elem = root.find('.//ErrorCode')
                value_elem = root.find('.//Value')
                if error_code_elem is None or value_elem is None:
                    print("필요한 XML 태그를 찾을 수 없습니다.")
                    return None

                error_code = float(error_code_elem.text)
                value = float(value_elem.text)
                return {'status': error_code, 'value': value}
            except Exception as e:
                print(f"Error parsing XML: {e}")
                return None
        except Exception as e:
            print(f"Error status: {e}")
            return None
        
def go():
    nav_status = robot.test(1,0.6)
    time.sleep(0.5)
    robot.test(1,0.6)
    time.sleep(0.5)
    if nav_status:
        current_value = nav_status.get('value', None)
        status = nav_status.get('status', None)
        print(f"Value: {current_value}, Status: {status}")

def back():
    nav_status = robot.test(2,0.5)
    time.sleep(0.5)
    robot.test(2,0.5)
    time.sleep(0.5)
    if nav_status:
        current_value = nav_status.get('value', None)
        status = nav_status.get('status', None)
        print(f"Value: {current_value}, Status: {status}")

def left():
    nav_status = robot.test(11,0.15)
    time.sleep(0.5)
    robot.test(11,0.15)
    time.sleep(0.5)
    if nav_status:
        current_value = nav_status.get('value', None)
        status = nav_status.get('status', None)
        print(f"Value: {current_value}, Status: {status}")

def right():
    nav_status = robot.test(12,0.15)
    time.sleep(0.5)
    robot.test(12,0.15)
    time.sleep(0.5)
    if nav_status:
        current_value = nav_status.get('value', None)
        status = nav_status.get('status', None)
        print(f"Value: {current_value}, Status: {status}")

def TurnL():
    nav_status = robot.test(3,0.3)
    time.sleep(0.5)
    robot.test(3,0.3)
    time.sleep(0.5)
    if nav_status:
        current_value = nav_status.get('value', None)
        status = nav_status.get('status', None)
        print(f"Value: {current_value}, Status: {status}")

def Turnr():
    nav_status = robot.test(4,0.3)
    time.sleep(0.5)
    robot.test(4,0.3)
    time.sleep(0.5)
    if nav_status:
        current_value = nav_status.get('value', None)
        status = nav_status.get('status', None)
        print(f"Value: {current_value}, Status: {status}")

def stop():
    robot.test(14,0)

robot = RobotProtocol()
go()