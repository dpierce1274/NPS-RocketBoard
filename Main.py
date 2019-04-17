'''

MIT License

Copyright (c) 2019 dpierce1274

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

import time
import sys
import mpl3115a2
import adxl377
import traceback
import IMU
from gpiozero import LED

g_counter = 0


def main():

    # Declare global variables
    global g_counter
    launch_indicator = False

    # Configure Status LEDs
    cal_led = LED(26)
    check_led = LED(19)
    cal_led.on()

    # I. Program initialization
    # Define initialization variables
    # ubl = navio.ublox.UBlox("spi:0.0", baudrate=5000000, timeout=0)
    baro = mpl3115a2.MPL3115A2(busID=1, slaveAddr=0x60, sea_level_pressure=1012.0)
    acc = adxl377.ADXL377(busID=1, slaveAddr=0x48)
    ser = serial.Serial(port='/dev/ttyAMA0', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=0.01)
    # Initialize the sensors
    IMU.initIMU()

    # Configure the GPS messages
    # ubl.configure_solution_rate(rate_ms=500)
    # ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_POSLLH, 1)
    # ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_STATUS, 1)
    # ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_VELNED, 1)

    # Create data file and write header #
    tstr = time.strftime('%Y-%m-%d_%H-%M-%S-%Z.txt')
    filename = str('Flight Data ') + tstr
    header_1 = str('Counter, Time, ACCx, ACCy, ACCz, accx, accy, accz, GRYx, GRYy, GRYz, MAGx, MAGy, MAGz, '
                   'Temp(C), Pres(mbar), Alt (m) \n')
    fp = open(filename, 'a')
    fp.write(header_1)
    fp.close()

    time.sleep(1)
    cal_led.off()
    # II. Main Loop

    while True:
        g_counter += 1
        status_led(check_led)                       # Flash status LED
        flt_params = read_flt_params(baro, IMU, acc)     # Get the flight parameters

        launch_indicator = check_launch(launch_indicator, flt_params, cal_led)

        if launch_indicator:
            #flt_params.append(str('launch'))
            launch_indicator = False

        write_to_file(filename, flt_params)  # Append parameters to file


def read_flt_params(baro, IMU, acc):
    global g_counter

    baro_data = baro.get_barometer_data()
    imu_data = IMU.get_IMU_data()
    acc_data = acc.get_accel_values()
    ACCx = float(imu_data[0])
    ACCy = float(imu_data[1])
    ACCz = float(imu_data[2])
    accx = float(acc_data[0])
    accy = float(acc_data[1])
    accz = float(acc_data[2])
    GRYx = float(imu_data[3])
    GRYy = float(imu_data[4])
    GRYz = float(imu_data[5])
    MAGx = float(imu_data[6])
    MAGy = float(imu_data[7])
    MAGz = float(imu_data[8])
    temp = float(baro_data[0])
    pres = float(baro_data[1])
    alt = int(baro_data[2])

    t = float('{:.2f}'.format(time.time()))
    output = [g_counter, t, ACCx, ACCy, ACCz, accx, accy, accz, GRYx, GRYy, GRYz, MAGx, MAGy, MAGz, temp, pres, alt]
    return output


def read_line(ser, line):
    # This is a function that samples characters from the serial port one at a time if there are characters waiting.
    # It continues to build the line and returns it to the main script
    # Input: line
    # Output: line
    if ser.inWaiting() > 0:
        c = ser.read(1)     # read one character (or timeout)
        line = line + c     # add character to the line
    return line             # returns message to main loop


def write_to_file(filename, flt_params):
    # This function writes the flight parameters array to a .txt file on the SD Card
    # Input: flight parameters
    # Output: none
    fp = open(filename, 'a+')
    fp.write(str(flt_params) + '\n')
    fp.close()


def str_to_num(input):
    # This function converts a GPS string out value with equals sign to a float value
    # Inputs: String value with =
    # Outputs: Float value

    # Find the index of the equals sign
    index = input.find('=')

    # Remove all characters up to and including the equals sign
    output = input[index + 1:]

    output = float(output)

    return output


def status_led(check_led):
    global g_counter

    if g_counter % 200 == 0:
        check_led.on()
        print('Main enabled')
    elif g_counter % 100 == 0:
        check_led.off()


def check_launch(launch_indicator, flt_params, led):

    if (abs(flt_params[2]) or abs(flt_params[3]) or abs(flt_params[4])) > 4:
        print(abs(flt_params[2]), abs(flt_params[3]), abs(flt_params[4]))
        launch = True
        led.on()
    elif launch_indicator:
        launch = True
    else:
        launch = False
    return launch


def send_message(ser, message):
    # This function formats and sends a telemetry message to the ground radio
    # Inputs: message
    # Outputs: none

    ser.write('{:<100s}'.format('16 %d %s\r' % (int(time.time()), message)))
    print('{:<100s}'.format('16 %d %s\n' % (int(time.time()), message)))


def send_gps(ser, data):
    # This function formats and sends a GPS telemetry message to the ground radio
    # Inputs: GPS
    # Outputs: none
    msg = "{:>10d} {:>6s} {:>10d} {:>+9.5f} {:>+10.5f} deg {:>5d} m".format(data[0], data[1], int(data[2]), data[3],
                                                                            data[4], int(data[5]))
    ser.write('{:<100s}'.format('12 %s\r' % msg))
    print('{:<100s}'.format('12 %s\n' % msg))


start = time.time()

# Execute `main()` function
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Program Terminating...")
        time.sleep(1)
        sys.exit()
    except:                                                     # Pass and log all other errors
        s = traceback.format_exc()
        fp = open("Traceback_Log.txt", "a")
        fp.write(s + "\n")
        fp.close()