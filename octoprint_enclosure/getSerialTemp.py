import serial
import sys
import time

class SerialError(Exception):
    """ Bast class for exception """

pin = sys.argv[2]

# Assuming your device appears as /dev/ttyUSB0 on the Raspberry Pi
# Adjust the port and baud rate as necessary
ser = serial.Serial('/dev/'+ pin, 115200, timeout=1)
ser.flush()

def get_serial_value():
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        temperature, humidity = map(float, line.split(','))
        return temperature, humidity
    else:
        raise SerialError('No serial data available')

def main():
    try:
        temperature, humidity = get_serial_value()
        print('{0:0.1f} | {1:0.1f}'.format(temperature, humidity))
    except:
        print('-1 | -1')

if __name__ == "__main__":
    main()
