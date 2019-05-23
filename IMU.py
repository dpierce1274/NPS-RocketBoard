"""
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

IMU is the Python object for the LSM9DS1 inertial measurement unit. The sensor communicates with the RPi via i2c.

Source Authors: Mark Williams and Peter Peck
Modified by: Dillon Pierce
Name of File: mpl3115a2.py
File Location: https://github.com/dpierce1274/NPS-RocketBoard.git
Date Last Modified: 23 May 2019

Inputs: None
Outputs: Acceleration-Gs (x,y,z), Rotation-deg/s (x,y,z)
"""

import smbus
import time

bus = smbus.SMBus(1)
from LSM9DS1 import *


LSM9DS0 = 1
gain = 0.07         # Gyro Gain based on init setting

def detectIMU():
    try:
        # Check for LSM9DS1
        # If no LSM9DS1 is connected, there will be an I2C bus error and the program will exit.
        # This section of code stops this from happening.
        LSM9DS1_WHO_XG_response = (bus.read_byte_data(LSM9DS1_GYR_ADDRESS, LSM9DS1_WHO_AM_I_XG))
        LSM9DS1_WHO_M_response = (bus.read_byte_data(LSM9DS1_MAG_ADDRESS, LSM9DS1_WHO_AM_I_M))

    except IOError as f:
        print('')  # need to do something here, so we just print a space
    else:
        if (LSM9DS1_WHO_XG_response == 0x68) and (LSM9DS1_WHO_M_response == 0x3d):
            print("Found LSM9DS1")

    time.sleep(1)


def writeACC(register, value):
    bus.write_byte_data(LSM9DS1_ACC_ADDRESS, register, value)
    return -1


def writeMAG(register, value):
    bus.write_byte_data(LSM9DS1_MAG_ADDRESS, register, value)
    return -1


def writeGRY(register, value):
    bus.write_byte_data(LSM9DS1_GYR_ADDRESS, register, value)
    return -1


def readACCx():
    acc_l = bus.read_byte_data(LSM9DS1_ACC_ADDRESS, LSM9DS1_OUT_X_L_XL)
    acc_h = bus.read_byte_data(LSM9DS1_ACC_ADDRESS, LSM9DS1_OUT_X_H_XL)
    acc_combined = (acc_l | acc_h << 8)
    return acc_combined if acc_combined < 32768 else acc_combined - 65536


def readACCy():
    acc_l = bus.read_byte_data(LSM9DS1_ACC_ADDRESS, LSM9DS1_OUT_Y_L_XL)
    acc_h = bus.read_byte_data(LSM9DS1_ACC_ADDRESS, LSM9DS1_OUT_Y_H_XL)
    acc_combined = (acc_l | acc_h << 8)
    return acc_combined if acc_combined < 32768 else acc_combined - 65536


def readACCz():
    acc_l = bus.read_byte_data(LSM9DS1_ACC_ADDRESS, LSM9DS1_OUT_Z_L_XL)
    acc_h = bus.read_byte_data(LSM9DS1_ACC_ADDRESS, LSM9DS1_OUT_Z_H_XL)
    acc_combined = (acc_l | acc_h << 8)
    return acc_combined if acc_combined < 32768 else acc_combined - 65536


def readMAGx():
    mag_l = bus.read_byte_data(LSM9DS1_MAG_ADDRESS, LSM9DS1_OUT_X_L_M)
    mag_h = bus.read_byte_data(LSM9DS1_MAG_ADDRESS, LSM9DS1_OUT_X_H_M)
    mag_combined = (mag_l | mag_h << 8)
    return mag_combined if mag_combined < 32768 else mag_combined - 65536


def readMAGy():
    mag_l = bus.read_byte_data(LSM9DS1_MAG_ADDRESS, LSM9DS1_OUT_Y_L_M)
    mag_h = bus.read_byte_data(LSM9DS1_MAG_ADDRESS, LSM9DS1_OUT_Y_H_M)
    mag_combined = (mag_l | mag_h << 8)
    return mag_combined if mag_combined < 32768 else mag_combined - 65536


def readMAGz():
    mag_l = bus.read_byte_data(LSM9DS1_MAG_ADDRESS, LSM9DS1_OUT_Z_L_M)
    mag_h = bus.read_byte_data(LSM9DS1_MAG_ADDRESS, LSM9DS1_OUT_Z_H_M)
    mag_combined = (mag_l | mag_h << 8)
    return mag_combined if mag_combined < 32768 else mag_combined - 65536


def readGYRx():
    gyr_l = bus.read_byte_data(LSM9DS1_GYR_ADDRESS, LSM9DS1_OUT_X_L_G)
    gyr_h = bus.read_byte_data(LSM9DS1_GYR_ADDRESS, LSM9DS1_OUT_X_H_G)
    gyr_combined = (gyr_l | gyr_h << 8)
    return gyr_combined if gyr_combined < 32768 else gyr_combined - 65536


def readGYRy():
    gyr_l = bus.read_byte_data(LSM9DS1_GYR_ADDRESS, LSM9DS1_OUT_Y_L_G)
    gyr_h = bus.read_byte_data(LSM9DS1_GYR_ADDRESS, LSM9DS1_OUT_Y_H_G)
    gyr_combined = (gyr_l | gyr_h << 8)
    return gyr_combined if gyr_combined < 32768 else gyr_combined - 65536


def readGYRz():
    gyr_l = bus.read_byte_data(LSM9DS1_GYR_ADDRESS, LSM9DS1_OUT_Z_L_G)
    gyr_h = bus.read_byte_data(LSM9DS1_GYR_ADDRESS, LSM9DS1_OUT_Z_H_G)
    gyr_combined = (gyr_l | gyr_h << 8)
    return gyr_combined if gyr_combined < 32768 else gyr_combined - 65536


def initIMU():

        # initialise the gyroscope
        writeGRY(LSM9DS1_CTRL_REG4, 0b00111000)  # z, y, x axis enabled for gyro
        writeGRY(LSM9DS1_CTRL_REG1_G, 0b10111000)  # Gyro ODR = 476Hz, 2000 dps
        writeGRY(LSM9DS1_ORIENT_CFG_G, 0b10111000)  # Swap orientation

        # initialise the accelerometer
        writeACC(LSM9DS1_CTRL_REG5_XL, 0b00111000)  # z, y, x axis enabled for accelerometer
        writeACC(LSM9DS1_CTRL_REG6_XL, 0b00111000)  # +/- 8g

        # initialise the magnetometer
        writeMAG(LSM9DS1_CTRL_REG1_M, 0b10011100)  # Temp compensation enabled,Low power mode mode,80Hz ODR
        writeMAG(LSM9DS1_CTRL_REG2_M, 0b01000000)  # +/-12gauss
        writeMAG(LSM9DS1_CTRL_REG3_M, 0b00000000)  # continuous update
        writeMAG(LSM9DS1_CTRL_REG4_M, 0b00000000)  # lower power mode for Z axis


def get_IMU_data():
    ACCx = '{:.2f}'.format(readACCx()*0.244/1000)
    ACCy = '{:.2f}'.format(readACCy()*0.244/1000)
    ACCz = '{:.2f}'.format(readACCz()*0.244/1000)
    GRYx = '{:.2f}'.format(readGYRx()*gain)
    GRYy = '{:.2f}'.format(readGYRy()*gain)
    GRYz = '{:.2f}'.format(readGYRz()*gain)
    MAGx = '{:.2f}'.format(readMAGx())
    MAGy = '{:.2f}'.format(readMAGy())
    MAGz = '{:.2f}'.format(readMAGz())

    return ACCx, ACCy, ACCz, GRYx, GRYy, GRYz, MAGx, MAGy, MAGz
