import mraa
import time
import sys
from math import *

# serial port
port = "/dev/ttyS5"
u = mraa.Uart(port)

u.setBaudRate(19200)
u.setMode(8, mraa.UART_PARITY_NONE, 1)
u.setFlowcontrol(False, False)

def parse_data(data):
    splited_data = data.split(',')
    lat = 0
    lon = 0
    speed = 0
    if splited_data[3] and splited_data[5] and splited_data[7] != '':
        lat = float(splited_data[3])
        lon = float(splited_data[5])
        speed = float(splited_data[7]) * 1.68781
    else:
        print(splited_data)
    return lat, lon, speed

def convert_DDMM_to_DD(lat, lon):
    if lat == 0 or lon == 0:
        print("ERROR: GPS is not fixed yet!")
        return 0, 0
    lat = (lat - 3000) / 60
    lon = (lon - 9600) / 60
    return lat + 30, lon + 96


def degree_to_radians(degree):
    return degree * pi / 180

def dis_in_meter(lat1, lon1, lat2, lon2):
    earth_radius = 6371000
    dlat = degree_to_radians(lat2 - lat1)
    dlon = degree_to_radians(lon2 - lon1)
    lat1 = degree_to_radians(lat1)
    lat2 = degree_to_radians(lat2)
    a = sin(dlat/2) * sin(dlat/2) + sin(dlon/2) * sin(dlon/2) * cos(lat1) * cos(lat2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return earth_radius * c

def log_data(filename, lat, lon):
    with open(filename, 'a') as f:
        f.write('lat: ' + str(lat) +'\n')
        f.write('lon: ' + str(lon) +'\n')

def acc_mean(cur_m_lat, cur_m_lon, lat, lon, n):
    res_lat = cur_m_lat * (n / (n + 1.0)) + lat / (n + 1)
    res_lon = cur_m_lon * (n / (n + 1.0)) + lon / (n + 1)
    return res_lat, res_lon

def run():
    count = 0
    NUM_FILES = 5
    file_index = 0
    FILE_CAP = 10000
    while True:
        if u.dataAvailable():
            # We are doing 60-byte reads here
            data = u.readStr(60)
            if data.startswith('$GNRMC'):
                lat, lon, speed = parse_data(data)
                lat, lon = convert_DDMM_to_DD(lat, lon)

                log_data('logfile' + file_index + '.txt', lat, lon)
                count += 1
                if count == FILE_CAP:
                    file_index += 1  #Every file record just 10 thousand pieces of data
                    file_index %= NUM_FILES
        

if __name__ == '__main__':
    run()




        
