#!/usr/bin/python3

import time
from datetime import datetime
import argparse
import json
import sys
import serial

ser = serial.Serial()
ser.baudrate = 115200
ser.bytesize=serial.SEVENBITS
ser.parity=serial.PARITY_EVEN
ser.stopbits=serial.STOPBITS_ONE
ser.xonxoff=0
ser.rtscts=0
ser.timeout=20
ser.port="/dev/ttyUSB0"

try:
    ser.open()
except:
    sys.exit ("Error opening %s. Program stopped."  % ser.name)

p1_counter =0
stack=[]

while p1_counter < 36:
    p1_line=''
    try:
        p1_raw = ser.readline()
    except:
        sys.exit ("Serial port %s can't be read. Program stopped." % ser.name )
    p1_str=str(p1_raw)
    p1_line=p1_str.strip()
    stack.append(p1_line)
    p1_counter = p1_counter +1

# print stack

# Send data to azure queue for further processing
from azure.storage.queue import QueueClient
queue = QueueClient.from_connection_string(conn_str="xxxxxxxx", queue_name="readings")
queue.send_message(stack)

try:
    ser.close()
except:
    sys.exit ("Ohoh %s. Program stopped." % ser.name )
