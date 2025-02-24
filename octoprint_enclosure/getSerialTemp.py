import serial
import sys
import time
import os

class SerialError(Exception):
    """ Base class for exception """

pin = sys.argv[2]
# Write the pin value to a file for debugging
with open(os.path.expanduser('~/scripts/pin_value.txt'), 'w') as f:
    f.write(pin)

ser = serial.Serial('/dev/'+pin, 115200, timeout=5)  # Changed port to '/dev/ttyACM2' and timeout to 5 seconds for consistency
ser.flush()
#time.sleep(1)

def get_serial_value():
    start_time = time.time()
    valid_line_count = 0

    while time.time() - start_time < 5 and valid_line_count < 7:  # poll for 5 seconds
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            try:              
                valid_line_count += 1
                if valid_line_count == 7:
                    temperature, humidity = line.split(',')
                    temperature_float = float(temperature)
                    humidity_float = float(humidity)
                    return temperature_float, humidity_float
            except ValueError:
                print(f"Unable to process line: {line}")

    raise SerialError('No valid 5th line received in 5 seconds')

def main():
    try:
        temperature, humidity = get_serial_value()
        print('{0:0.1f} | {1:0.1f}'.format(temperature, humidity))
    except SerialError as e:
        print(f"Error: {e}")
        print('-1 | -1')
    except Exception as e:
        print(f"Error: {e}")
        print('-1 | -1')

if __name__ == "__main__":
    main()

