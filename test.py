# RELAY
# - Lấy trạng thái
# Request:  ID 03 00 00 00 01 CRCL CRCH
# Response: ID 03 02 00 xx CRCL CRCH (xx: 0xFF: ON, 0x00: OFF)
# - Gắn trạng thái
# Request:  ID 06 00 00 00 xx CRCL CRCH (xx: 0xFF: ON, 0x00: OFF)
# Response: ID 06 00 00 00 xx CRCL CRCH

import time
from serial import Serial
from modbus485 import *

def serial_read_data(serial, length):
    out = []
    time.sleep(0.5)

    #read number of bytes in buffer
    byteToRead = serial.inWaiting()

    #read array of bytes from buffer
    if byteToRead > 0:
        out = serial.read(byteToRead)

    #convert data from byte to int
    data_out = [b for b in out]

    return data_out

def test_relay_485(serial):
    relay_on = [0x01, 0x06, 0x00, 0x00, 0x00, 0xFF]
    relay_off = [0x01, 0x06, 0x00, 0x00, 0x00, 0x00]
    print("ON")
    serial.write(addCRC16(relay_on))
    result = serial_read_data(serial, 100)
    print(result)
    time.sleep(2)
    print("OFF")
    serial.write(addCRC16(relay_off))
    result = serial_read_data(serial, 100)
    print(result)
    time.sleep(2)

serialCommunication = Serial(port="COM13", baudrate=9600)

while True:
    test_relay_485(serialCommunication)
    time.sleep(2)