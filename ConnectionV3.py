# This code is for python 3 and above
# You would need to install http.client with pip3 install http.client

import time
from GPS_API import *
import serial
import json
import requests


#list serial port: ls /dev/tty.*
ser = None
try:
    ser = serial.Serial('/dev/tty.EMTACBTGPS22222215077F-') #("/dev/ttyAMA0")  # Select your Serial Port
except Exception as ex:
    print(ex)
    sys.exit(0)

ser.baudrate = 9600 #38400  # Baud rate
ser.timeout = 0.5
sleep = 2  # how many seconds to sleep between posts to the channel

write_api_key = '3Y79CZWQ7OUSQE52'  # Thingspeak Write API Key
channel_id = '1707859'
msgdata = Message()  # Creates a Message Instance
url = "https://api.thingspeak.com/update"
message_buffer = []


def upload_cloud():
    try:
        lat = get_latitude(msgdata)
        if lat == 0.00:
            return

        lon = get_longitude(msgdata)
        alt = get_altitude(msgdata)
        sats = get_num_satellite(msgdata)
        fix = get_gps_fix(msgdata)
        # speed = get_speed(msgdata)

        params = json.dumps(
            {'api_key': write_api_key, 'field1': lat, 'field2': lon, 'field3': alt, 'field4': 10, 'field5': 20,
             'field6': fix, 'field7': sats})
        header = {"USER-Agent": "mw.doc.bulk-update (Raspberry Pi)", "Content-Type": "application/json",
                  "Content-Length": str(len(params))}
        response = requests.post(url, headers=header, data=params)
        print(response)
        print('Lat: %s' % lat)
        print('Lon: %s' % lon)
        print('Alt: %s' % alt)
        print('Sats: %s' % sats)
        print('Fix: %s' % fix)
        # print('Speed: %s' % speed)
        # conn.close()
    except Exception as ex:
        print("Upload Cloud error: %s" % ex)


if __name__ == "__main__":
    start_gps_receiver(ser, msgdata)
    time.sleep(1)
    ready_gps_receiver(msgdata)
    while True:
        upload_cloud()
        time.sleep(sleep)
