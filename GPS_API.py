# This File consists of API calls for the GPS Parsing Functionality.This section parse the GPS values from the GPS Module.
# pynmea2 is Python library for parsing the NMEA 0183 protocol (GPS). To get that thing : pip install pynmea2

import threading
import pynmea2
import sys

class Message:
    def __init__(self):
        self.msg = ''

# Gps Receiver thread funcion, check gps value for infinte times
def get_gps_data(serial, dmesg):
    print("Initializing GPS\n")
    while True:
        strRead = serial.readline()
        if sys.version_info[0] == 3:
            strRead = strRead.decode("utf-8", "ignore")
            if strRead[0:6] == '$GPGGA':
                dmesg.msg = pynmea2.parse(strRead)
            #if strRead[0:6] == '$GPRMC':
            #    dmesg.msg = pynmea2.parse(strRead)
        else:
            if strRead.find('GGA') > 0:
                dmesg.msg = pynmea2.parse(strRead)

# API to call start the GPS Receiver
def start_gps_receiver(serial, dmesg):
    t2 = threading.Thread(target=get_gps_data, args=(serial, dmesg))
    t2.start()
    print("GPS Receiver started")

# API to fix the GPS Revceiver
def ready_gps_receiver(msg):
    print("Please wait for solid GPS fix .....")
    dmesg = msg.msg
    print('DMESG: %s ' % dmesg)
    if dmesg == '':
        return

    while (dmesg.gps_qual < 1):
        print('GPS Fix: %s' % dmesg.gps_qual)
        pass

    print("GPS Fix available")

def get_altitude(msg):
    dmesg = msg.msg
    return dmesg.altitude

# API to get Number of Satellites from the GPS Receiver
def get_num_satellite(msg):
    dmesg = msg.msg
    return dmesg.num_sats

def get_speed(msg):
    dmesg = msg.msg
    return dmesg.speed

# API to check the status of GPS Fix
def get_gps_fix(msg):
    dmesg = msg.msg
    return dmesg.gps_qual

# API to get the HDOP
def get_HDOP(msg):
    dmesg = msg.msg
    return dmesg.horizontal_dil

# API to get latitude from the GPS Receiver
def get_latitude(msg):
    dmesg = msg.msg
    return dmesg.latitude

# API to get longitude from the GPS Receiver
def get_longitude(msg):
    dmesg = msg.msg
    return dmesg.longitude
