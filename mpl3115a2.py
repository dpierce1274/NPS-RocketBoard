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

mpl3115a2 is the Python object for the mpl3115a2 barometric sensor. The sensor communicates with the RPi via i2c.
Altitude is computed using an equation provided in the sensor's documentation.

Source Author: Dillon Pierce
Name of File: mpl3115a2.py
File Location: https://github.com/dpierce1274/NPS-RocketBoard.git
Date Last Modified: 23 May 2019

Inputs: BusID, Slave Address, Sea level pressure (mbar)
Outputs: temperature (deg C), pressure (mbar), altitude (m)
'''

import smbus
import time

# Register Address Map
STATUS          = 0x00
OUT_P_MSB       = 0x01
OUT_P_CSB       = 0x02
OUT_P_LSB       = 0x03
OUT_T_MSB       = 0x04
OUT_T_LSB       = 0x05
DR_STATUS       = 0x06
OUT_P_DELTA_MSB = 0x07
OUT_P_DELTA_CSB = 0x08
OUT_P_DELTA_LSB = 0x09
OUT_T_DELTA_MSB = 0x0A
OUT_T_DELTA_LSB = 0x0B
WHO_AM_I        = 0x0C
F_STATUS        = 0x0D
F_DATA          = 0x0E
F_SETUP         = 0x0F
TIME_DLY        = 0x10
SYSMOD          = 0x11
INT_SOURCE      = 0x12
PT_DATA_CFG     = 0x13
BAR_IN_MSB      = 0x14
BAR_IN_LSB      = 0x15
P_TGT_MSB       = 0x16
P_TGT_LSB       = 0x17
T_TGT           = 0x18
P_WND_MSB       = 0x19
P_WND_LSB       = 0x1A
T_WND           = 0x1B
P_MIN_MSB       = 0x1C
P_MIN_CSB       = 0x1D
P_MIN_LSB       = 0x1E
T_MIN_MSB       = 0x1F
T_MIN_LSB       = 0x20
P_MAX_MSB       = 0x21
P_MAX_CSB       = 0x22
P_MAX_LSB       = 0x23
T_MAX_MSB       = 0x24
T_MAX_LSB       = 0x25

# Control Registers
CTRL_REG1 = 0x26
CTRL_REG2 = 0x27
CTRL_REG3 = 0x28
CTRL_REG4 = 0x29
CTRL_REG5 = 0x2A

# Data Offsets
OFF_P = 0x2B
OFF_T = 0x2C
OFF_H = 0x2D



class MPL3115A2(object):

    def __init__(self, busID, slaveAddr, sea_level_pressure):
        self.__i2c = smbus.SMBus(busID)                                 # Set busid equal to user input ID
        self.__slave = slaveAddr                                        # Take given slave address
        self.__sea_level_pressure = sea_level_pressure                  # Updated sea_level_pressure value (mbar)

        # No FIFO setup (Polling)
        self.__i2c.write_byte_data(self.__slave, CTRL_REG1, 0x38)       # Set Barometer standby mode with OSR 128
        self.__i2c.write_byte_data(self.__slave, PT_DATA_CFG, 0x07)     # Enable Data Flags
        self.__i2c.write_byte_data(self.__slave, CTRL_REG1, 0x39)       # Set Barometer active mode with OSR 128
        time.sleep(1)                                                   # Allow sensor to enter active mode

    def get_barometer_data(self):
        # Read Registers
        out_p_msb = self.__i2c.read_byte_data(self.__slave, OUT_P_MSB)
        out_p_csb = self.__i2c.read_byte_data(self.__slave, OUT_P_CSB)
        out_p_lsb = self.__i2c.read_byte_data(self.__slave, OUT_P_LSB)
        out_t_msb = self.__i2c.read_byte_data(self.__slave, OUT_T_MSB)
        out_t_lsb = self.__i2c.read_byte_data(self.__slave, OUT_T_MSB)
        # Format Data
        pres = (out_p_msb << 16 | out_p_csb << 8 | out_p_lsb & 0xF0) / 64.0   # Convert pres data to 20-bit unsigned
        pres_mbar = pres / 100.0                                              # Convert pressure value to mbar
        temp = (out_t_msb << 8 | out_t_lsb & 0xF0) / 256.0      # Convert temp data to 12-bit two's complement
        # Compute Altitude
        alt = 44330.77*(1-(pres_mbar/
                           self.__sea_level_pressure)**0.1902632)       # Compute altitude from documentation formula

        # Return Values
        return '{:.2f}'.format(temp), '{:.2f}'.format(pres_mbar), '{:.0f}'.format(alt)