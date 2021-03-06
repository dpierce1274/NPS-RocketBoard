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

The Main flight software is the primary software script for the NPS SSAG Rocketboard.
The software is manually initiated (and back grounded!) via a WiFi SSH terminal. The
script captures the rocket's various flight sensor data and stores the data in a .txt file.
The script also initiates a subprocess (Telemetry.py) that is responsible for capturing and
sending GPS telemetry data via the MHX radio.

Source Author: Dillon Pierce
Name of File: Main.py
File Location: https://github.com/dpierce1274/NPS-RocketBoard.git
Date Last Modified: 23 May 2019




'''

import time
import sys
import mpl3115a2
import adxl377
import traceback
import IMU
from gpiozero import LED
import subprocess
import shlex

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
    baro = mpl3115a2.MPL3115A2(busID=1, slaveAddr=0x60, sea_level_pressure=1012.0)
    acc = adxl377.ADXL377(busID=1, slaveAddr=0x48)

    # Initialize the sensors
    IMU.initIMU()

    # Begin Telemetry Process
    p_name = '/usr/bin/python Telemetry.py'
    process = subprocess.Popen(shlex.split(p_name), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
        g_counter += 1                                  # Iterate Counter
        status_led(check_led)                           # Flash status LED
        flt_params = read_flt_params(baro, IMU, acc)    # Get the flight parameters

        write_to_file(filename, flt_params)             # Append parameters to file


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


def write_to_file(filename, flt_params):
    # This function writes the flight parameters array to a .txt file on the SD Card
    # Input: flight parameters
    # Output: none
    fp = open(filename, 'a+')
    fp.write(str(flt_params) + '\n')
    fp.close()


def status_led(check_led):
    global g_counter

    if g_counter % 200 == 0:
        check_led.on()
        print('Main enabled')
    elif g_counter % 100 == 0:
        check_led.off()


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
