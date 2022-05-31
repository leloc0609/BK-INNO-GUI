# RELAY
# - Lấy trạng thái
# Request:  ID 03 00 00 00 01 CRCL CRCH
# Response: ID 03 02 00 xx CRCL CRCH (xx: 0xFF: ON, 0x00: OFF)
# - Gắn trạng thái
# Request:  ID 06 00 00 00 xx CRCL CRCH (xx: 0xFF: ON, 0x00: OFF)
# Response: ID 06 00 00 00 xx CRCL CRCH

import time

import serial.tools.list_ports
from modbus485 import *



def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range (0, N):
        port = ports[i]
        strPort = str(port)

    if "CH340" in strPort:
        splitPort = strPort.split(" ")
        commPort = (splitPort[0])
        print("Connected to", commPort)


    return commPort

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

def control_relay(serial,lockID):
    relay_on = [lockID, 0x06, 0x00, 0x00, 0x00, 0xFF] #0x01 dau tien la id cai relay
    relay_off = [lockID, 0x06, 0x00, 0x00, 0x00, 0x00]
    print("ON")
    serial.write(addCRC16(relay_on))
    result = serial_read_data(serial, 100)
    print(result)
    time.sleep(1)
    print("OFF")
    serial.write(addCRC16(relay_off))
    result = serial_read_data(serial, 100)
    print(result)




