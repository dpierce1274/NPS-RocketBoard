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

adxl377 is the Python object for the adxl377 "high-g" accelerometer. The sensor is analog, so the script is designed for
communication with the analog-to-digital converter (TI ADS7828). The TI ADS7828 communicates with the RPi via i2c.
Currently, channels 3-7 are unused on the TI ADS7828. Future iterations of the rocket board could make use of these
excess channels.

Source Author: Dillon Pierce
Name of File: adxl377.py
File Location: https://github.com/dpierce1274/NPS-RocketBoard.git
Date Last Modified: 23 May 2019

Inputs: BusID, Slave Address
Outputs: Acceleration-Gs (x,y,z)
'''

from smbus import SMBus
import struct

# Analog Channel Input
channel_0 = 0b000
channel_1 = 0b100
channel_2 = 0b001
channel_3 = 0b101
channel_4 = 0b010
channel_5 = 0b110
channel_6 = 0b011
channel_7 = 0b111

# Voltage Reference
v_ref = 2.5

# Command Byte Values
# Format: SD C2 C1 C0 PD1 PD0 X X
# C2 C1 C0 = Channel Address
sd = 1       # Single-ended input
pd1 = 1      # Internal reference ON
pd0 = 1      # A/D Converter ON
g_value = 0  # Initial G reading

# Accelerometer calibration values
x_min = 1.4368
y_min = 1.5399
z_min = 1.4178
x_max = 1.4642
y_max = 1.6296
z_max = 1.4746

x_mean = (x_max+x_min)/2
y_mean = (y_max+y_min)/2
z_mean = (z_max+z_min)/2

x_step = (x_max-x_min)/2
y_step = (y_max-y_min)/2
z_step = (z_max-z_min)/2

general_step = 0.0065           # volts/g per documentation

class ADXL377(object):

    def __init__(self, busID, slaveAddr):
        self.__i2c = SMBus(busID)
        self.__slave = slaveAddr

    Max_AD = 4096.0                                 # 12-bit ADC

    def read_channel(self, channel):
        command = self.format_cmd_byte(channel)
        data = self.__i2c.read_i2c_block_data(self.__slave, command, 2)
        raw_value = struct.unpack('>H', struct.pack('>BB', data[0], data[1]))[0]
        voltage = (raw_value / self.Max_AD) * v_ref
        if channel == channel_0:
            g_value = (voltage - x_mean)/general_step
        if channel == channel_1:
            g_value = (voltage - y_mean)/general_step
        if channel == channel_2:
            g_value = (voltage - z_mean)/general_step

        return g_value

    def format_cmd_byte(self, channel):
        command = channel << 4 | 0x8C
        return command

    def get_accel_values(self):
        x_axis = self.read_channel(channel_0)
        y_axis = self.read_channel(channel_1)
        z_axis = self.read_channel(channel_2)
        return '{:.6f}'.format(x_axis), '{:.6f}'.format(y_axis), '{:.6f}'.format(z_axis)
