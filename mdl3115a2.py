import smbus
import time
import numpy as np




class MDL3115A2(object):

    scale_h = -7800
    sea_level_pressure = 1011.4

    def __init__(self, busID, slaveAddr):
        self.__i2c = smbus.SMBus(busID)                                 # Set busid equal to user input ID
        self.__slave = slaveAddr                                        # Take given slave address
        
        self.__i2c.write_byte_data(0x60, 0x26, 0xB9)
        self.__i2c.write_byte_data(0x60, 0x13, 0x07)
        self.__i2c.write_byte_data(0x60, 0x26, 0x39)

    def temperature(self):
        self.__i2c.write_byte_data(0x60, 0x26, 0x39)
        data = self.__i2c.read_i2c_block_data(0x60, 0x00, 6)
        temp = (data[4] << 8 | data[5] & 0xF0)/256.0
        cTemp = temp
        fTemp = cTemp * 1.8 + 32
        return cTemp
      
    def pressure(self):
        self.__i2c.write_byte_data(0x60, 0x26, 0x39)
        data = self.__i2c.read_i2c_block_data(0x60, 0x00, 6)
        pres = (data[1] << 16 | data[2] << 8 | data[3] & 0xF0) / 64.0
        pressure = pres / 100.0
        return pressure                         # Pressure in mbar

    def get_barometer_data(self):
        temp_data = self.temperature()
        pressure_data = self.pressure()
        alt = self.scale_h * np.log(pressure_data / self.sea_level_pressure)
        return '{:.2f}'.format(temp_data), '{:.2f}'.format(pressure_data), '{:.2f}'.format(alt)