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

LSM9DS1 contains the device registers for the LSM9DS1 inertial measurement unit.

Source Authors: Mark Williams and Peter Peck 
Name of File: mpl3115a2.py
File Location: https://github.com/dpierce1274/NPS-RocketBoard.git
Date Last Modified: 7 Jan 2018

Inputs: None
Outputs: None

'''

LSM9DS1_MAG_ADDRESS	= 0x1E
LSM9DS1_ACC_ADDRESS	= 0x6B
LSM9DS1_GYR_ADDRESS = 0x6B


#////////////////////////////////////////
#// LSM9DS1 Accel/Gyro (XL/G) Registers /
#////////////////////////////////////////
LSM9DS1_ACT_THS				= 0x04
LSM9DS1_ACT_DUR				= 0x05
LSM9DS1_INT_GEN_CFG_XL		= 0x06
LSM9DS1_INT_GEN_THS_X_XL	= 0x07
LSM9DS1_INT_GEN_THS_Y_XL	= 0x08
LSM9DS1_INT_GEN_THS_Z_XL	= 0x09
LSM9DS1_INT_GEN_DUR_XL		= 0x0A
LSM9DS1_REFERENCE_G			= 0x0B
LSM9DS1_INT1_CTRL			= 0x0C
LSM9DS1_INT2_CTRL			= 0x0D
LSM9DS1_WHO_AM_I_XG			= 0x0F
LSM9DS1_CTRL_REG1_G			= 0x10
LSM9DS1_CTRL_REG2_G			= 0x11
LSM9DS1_CTRL_REG3_G			= 0x12
LSM9DS1_ORIENT_CFG_G		= 0x13
LSM9DS1_INT_GEN_SRC_G		= 0x14
LSM9DS1_OUT_TEMP_L			= 0x15
LSM9DS1_OUT_TEMP_H			= 0x16
LSM9DS1_STATUS_REG_0		= 0x17
LSM9DS1_OUT_X_L_G			= 0x18
LSM9DS1_OUT_X_H_G			= 0x19
LSM9DS1_OUT_Y_L_G			= 0x1A
LSM9DS1_OUT_Y_H_G			= 0x1B
LSM9DS1_OUT_Z_L_G			= 0x1C
LSM9DS1_OUT_Z_H_G			= 0x1D
LSM9DS1_CTRL_REG4			= 0x1E
LSM9DS1_CTRL_REG5_XL		= 0x1F
LSM9DS1_CTRL_REG6_XL		= 0x20
LSM9DS1_CTRL_REG7_XL		= 0x21
LSM9DS1_CTRL_REG8			= 0x22
LSM9DS1_CTRL_REG9			= 0x23
LSM9DS1_CTRL_REG10			= 0x24
LSM9DS1_INT_GEN_SRC_XL		= 0x26
LSM9DS1_STATUS_REG_1		= 0x27
LSM9DS1_OUT_X_L_XL			= 0x28
LSM9DS1_OUT_X_H_XL			= 0x29
LSM9DS1_OUT_Y_L_XL			= 0x2A
LSM9DS1_OUT_Y_H_XL			= 0x2B
LSM9DS1_OUT_Z_L_XL			= 0x2C
LSM9DS1_OUT_Z_H_XL			= 0x2D
LSM9DS1_FIFO_CTRL			= 0x2E
LSM9DS1_FIFO_SRC			= 0x2F
LSM9DS1_INT_GEN_CFG_G		= 0x30
LSM9DS1_INT_GEN_THS_XH_G	= 0x31
LSM9DS1_INT_GEN_THS_XL_G	= 0x32
LSM9DS1_INT_GEN_THS_YH_G	= 0x33
LSM9DS1_INT_GEN_THS_YL_G	= 0x34
LSM9DS1_INT_GEN_THS_ZH_G	= 0x35
LSM9DS1_INT_GEN_THS_ZL_G	= 0x36
LSM9DS1_INT_GEN_DUR_G		= 0x37

#///////////////////////////////
#// LSM9DS1 Magneto Registers //
#///////////////////////////////
LSM9DS1_OFFSET_X_REG_L_M	= 0x05
LSM9DS1_OFFSET_X_REG_H_M	= 0x06
LSM9DS1_OFFSET_Y_REG_L_M	= 0x07
LSM9DS1_OFFSET_Y_REG_H_M	= 0x08
LSM9DS1_OFFSET_Z_REG_L_M	= 0x09
LSM9DS1_OFFSET_Z_REG_H_M	= 0x0A
LSM9DS1_WHO_AM_I_M			= 0x0F
LSM9DS1_CTRL_REG1_M			= 0x20
LSM9DS1_CTRL_REG2_M			= 0x21
LSM9DS1_CTRL_REG3_M			= 0x22
LSM9DS1_CTRL_REG4_M			= 0x23
LSM9DS1_CTRL_REG5_M			= 0x24
LSM9DS1_STATUS_REG_M		= 0x27
LSM9DS1_OUT_X_L_M			= 0x28
LSM9DS1_OUT_X_H_M			= 0x29
LSM9DS1_OUT_Y_L_M			= 0x2A
LSM9DS1_OUT_Y_H_M			= 0x2B
LSM9DS1_OUT_Z_L_M			= 0x2C
LSM9DS1_OUT_Z_H_M			= 0x2D
LSM9DS1_INT_CFG_M			= 0x30
LSM9DS1_INT_SRC_M			= 0x30
LSM9DS1_INT_THS_L_M			= 0x32
LSM9DS1_INT_THS_H_M			= 0x33

#////////////////////////////////
#// LSM9DS1 WHO_AM_I Responses //
#////////////////////////////////
LSM9DS1_WHO_AM_I_AG_RSP		= 0x68
LSM9DS1_WHO_AM_I_M_RSP		= 0x3D
