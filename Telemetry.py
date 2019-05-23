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

Telemetry.py is a sub process that runs under Main.py that is responsible for capturing, sending, and
storing GPS data. Telemetry data is sent via serial communications with the MHX radio to the ground station. Currently,
the software is only configured for sending data. Adding a serial read capability to this script would enable ground
station up link to the rocket.

Source Author: Dillon Pierce
Name of File: Telemetry.py
File Location: https://github.com/dpierce1274/NPS-RocketBoard.git
Date Last Modified: 23 May 2019
'''


import traceback
import serial
import ublox
import time
import sys


def main():

    ser = serial.Serial(port='/dev/ttyS0', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=0.01)
 
    # Create data file and write header #
    tstr = time.strftime('%Y-%m-%d_%H-%M-%S-%Z.txt')
    filename = str('Telemetry Data ') + tstr
    
    ubl = ublox.UBlox("spi:0.0", baudrate=5000000, timeout=2)

    ubl.set_preferred_dynamic_model(None)
    ubl.set_preferred_usePPP(None)
    
    # Configure the GPS messages
    ubl.configure_solution_rate(rate_ms=1000)
    ubl.configure_message_rate(ublox.CLASS_NAV, ublox.MSG_NAV_POSLLH, 1)
    ubl.configure_message_rate(ublox.CLASS_NAV, ublox.MSG_NAV_STATUS, 1)
    ubl.configure_message_rate(ublox.CLASS_NAV, ublox.MSG_NAV_VELNED, 1)
    ubl.configure_message_rate(ublox.CLASS_NAV, ublox.MSG_NAV_PVT, 1)

    message_names = ['NAV_POSLLH', 'NAV_STATUS', 'NAV_VELNED', 'NAV_PVT']

    check_msg = []

    while True:
        msg = ubl.receive_message()
        print(msg)
        if msg is None:
            if opts.reopen:
                ubl.close()
                ubl = ublox.UBlox("spi:0.0", baudrate=5000000, timeout=2)
                continue
            print(empty)
            break
        if msg.name() == "NAV_STATUS":
            outstr = str(msg).split(",")
            fix_id = int(str_to_num(outstr[1]))  # GPS fix - from UBX-NAV-STATUS function
            fix_ok = int(str_to_num(outstr[3]))  # gpsFixOk (1 =  position and velocity valid and within DOP and ACC)
            write_to_file(filename, outstr)
            check_msg.append(msg.name())
            print(outstr)
        if msg.name() == "NAV_POSLLH":
            outstr = str(msg).split(",")
            lon = float('%.7f' % (str_to_num(outstr[1])*10**-7))        # GPS longitude (deg)
            lat = float('%.7f' % (str_to_num(outstr[2])*10**-7))        # GPS latitude (deg)
            h_msl = float('%.1f' % (int(str_to_num(outstr[4])/1000)))   # GPS height MSL (m)
            write_to_file(filename, outstr)
            check_msg.append(msg.name())
        if msg.name() == "NAV_VELNED":
            outstr = str(msg).split(",")
            gps_hdg = float('%.1f' % (str_to_num(outstr[6])*10**-5))    # GPS heading (deg)
            gps_gspd = int(str_to_num(outstr[5])/100)                   # GPS ground speed (m/s)
            write_to_file(filename, outstr)
            check_msg.append(msg.name())
        if msg.name() == "NAV_PVT":
            outstr = str(msg).split(",")
            hour = outstr[4]
            min = outstr[5]
            sec = outstr[6]
            gps_time = '{}{}{}'.format(hour,min,sec)
            write_to_file(filename, outstr)
            check_msg.append(msg.name())

        if all(elem in check_msg for elem in message_names):
            data = [gps_time, 'NAVMSG', int(time.time()), lat, lon, h_msl]
            write_to_file(filename, data)
            send_gps(ser, data)
            check_msg = []


def send_gps(ser, data):
    # This function formats and sends a GPS telemetry message to the ground radio
    # Inputs: GPS
    # Outputs: none
    msg = "{:>10s} {:>6s} {:>10d} {:>+9.5f} {:>+10.5f} deg {:>5d} m".format(data[0], data[1], int(data[2]), data[3],
                                                                            data[4], int(data[5]))
    ser.write('{:<100s}'.format('12 %s\r' % msg))
    print('{:<100s}'.format('12 %s\n' % msg))


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


def write_to_file(filename, flt_params):
    # This function writes the flight parameters array to a .txt file on the SD Card
    # Input: flight parameters
    # Output: none
    fp = open(filename, 'a')
    fp.write(str(flt_params) + '\n')
    fp.close()


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
        fp = open("GPS_Traceback_Log.txt", "a")
        fp.write(s + "\n")
        fp.close()