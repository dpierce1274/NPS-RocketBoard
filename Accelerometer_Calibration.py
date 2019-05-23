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

Accelerometer calibration is the script used to obtain the adxl377 accelerometer calibration values. To use the
calibration script, first place the accelerometer on a relatively level surface. After initiating the script, slowly
rotate the sensor board about all three axes. Once complete, press Ctrl+C to terminate the script. The final maximum and
minimum calibration values for each axis will be displayed on the screen. Place these calibration values into the
adxl377.py object under the '#Accelerometer calibration values' heading for more accurate acceleration values.

Source Author: Dillon Pierce
Name of File: Accelerometer_Calibration.py
File Location: https://github.com/dpierce1274/NPS-RocketBoard.git
Date Last Modified: 23 May 2019

Inputs: None
Outputs: Accelerometer max and min calibration values (x,y,z)
'''

import adxl377
import time
from gpiozero import LED
import sys

acc = adxl377.ADXL377(busID=1, slaveAddr=0x48)
check_led = LED(19)

x_min = 3.0
y_min = 3.0
z_min = 3.0
x_max = 0.0
y_max = 0.0
z_max = 0.0
counter = 0.0


print('Calibration Commencing - Slowly rotate accelerometer about each axis when green light turns on')
time.sleep(2)

while True:
    try:
        counter += 1
        acc_data = acc.get_accel_values()
        x_value = float(acc_data[0])
        y_value = float(acc_data[1])
        z_value = float(acc_data[2])

        if counter > 100:
            print(acc_data)
            check_led.on()
            if x_value > x_max :
                x_max = x_value
            if x_value < x_min:
                x_min = x_value
            if y_value > y_max:
                y_max = y_value
            if y_value < y_min:
                y_min = y_value
            if z_value > z_max:
                z_max = z_value
            if z_value < z_min:
                z_min = z_value

        print('X Max: {:.4f}'.format(x_max), 'Y Max: {:.4f}'.format(y_max), 'Z Max: {:.4f}'.format(z_max))
        print('X Min: {:.4f}'.format(x_min), 'Y Min: {:.4f}'.format(y_min), 'Z Min: {:.4f}'.format(z_min))

    except KeyboardInterrupt:
        print('Final Calibration values:')
        print('X Max: {:.4f}'.format(x_max), 'Y Max: {:.4f}'.format(y_max), 'Z Max: {:.4f}'.format(z_max))
        print('X Min: {:.4f}'.format(x_min), 'Y Min: {:.4f}'.format(y_min), 'Z Min: {:.4f}'.format(z_min))
        sys.exit()

