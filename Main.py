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


import os
import platform
import datetime
import spidev
import time
import argparse
import sys
import math
import mdl3115a2
import serial
import subprocess
import shlex
import traceback
import IMU
from gpiozero import LED

g_counter = 0


def main():

    # Declare global variables
    global g_counter

    # Configure Status LEDs
    cal_led = LED(26)
    check_led = LED(19)
    cal_led.on()

    # I. Program initialization
    # Define initialization variables
    # ubl = navio.ublox.UBlox("spi:0.0", baudrate=5000000, timeout=0)
    baro = mdl3115a2.MDL3115A2(busID=1, slaveAddr=0x60)

    # Initialize the sensors
    IMU.initIMU()
    baro.initialize()

    # Configure the GPS messages
    # ubl.configure_solution_rate(rate_ms=500)
    # ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_POSLLH, 1)
    # ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_STATUS, 1)
    # ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_VELNED, 1)

    # Create data file and write header #
    tstr = time.strftime('%Y-%m-%d_%H-%M-%S-%Z.txt')
    filename = str('Flight Data ') + tstr
    header_1 = str('Counter, Time, ACCx, ACCy, ACCz, GRYx, GRYy, GRYz, MAGx, MAGy, MAGz, Temp(F), Pres \n')
    fp = open(filename, 'w+')
    fp.write(header_1)
    fp.close()

    cal_led.off()
    # II. Main Loop

    while True:
        g_counter += 1
        status_led(check_led)                       # Flash status LED
        flt_params = read_flt_params(baro, IMU)     # Get the flight parameters
        write_to_file(filename,flt_params)          # Append parameters to file


def read_flt_params(baro, IMU):
    global g_counter

    baro_data = baro.get_barodata()
    imu_data = IMU.get_IMU_data()
    t = time.time()
    output = [g_counter,t,imu_data,baro_data]
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
    fp.write(str(flt_params) + str('\n'))
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

    if g_counter % 10 == 0:
        check_led.on()
    elif g_counter % 20 == 0:
        check_led.off()


start = time.time()
# Execute `main()` function
if __name__ == '__main__':
    main()
    sys.exit()
    try:
        main()
    except KeyboardInterrupt:
        print "Program Terminating..."
        stop = time.time()
        time.sleep(1)
        print('Data Rate: %.1f samples/second' % (G_counter/(stop-start)))
    except:                                                     # Pass and log all other errors
        s = traceback.format_exc()
        fp = open("Traceback_Log.txt", "a")
        fp.write(s + "\n")
        fp.close()


print('EOF -------------------------\n')
