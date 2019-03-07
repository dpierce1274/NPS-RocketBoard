from smbus import SMBus
import struct


channel_0 = 0x0
channel_1 = 0x4
channel_2 = 0x1
channel_3 = 0x5
channel_4 = 0x2
channel_5 = 0x6
channel_6 = 0x3
channel_7 = 0x7


class ADXL377(object):

    def __init__(self, busID, slaveAddr):
        self.__i2c = SMBus(busID)
        self.__slave = slaveAddr

    Max_AD = 4096.0                                 # 12-bit ADC
    V_REF = 3.0                                     # 3V Voltage Reference

    def read_channel(self, channel):
        data = self.__i2c.read_i2c_block_data(self.__slave, channel | 0b10001111, 2)
        N = struct.unpack('>H', struct.pack('>BB', data[0], data[1]))[0]
        V = (N / self.Max_AD) * self.__V_REF
        return V

    def read_channel5(self):
        data = self.__i2c.read_i2c_block_data(self.__slave, (6 << 4) | (0b10001111), 2)
        N = struct.unpack('>H', struct.pack('>BB', data[0], data[1]))[0]
        V = (N / self.Max_AD) * self.__V_REF
        return V

    def read_channel2(self):
        data = self.__i2c.read_i2c_block_data(self.__slave, (1 << 4) | (0b10001111), 2)
        N = struct.unpack('>H', struct.pack('>BB', data[0], data[1]))[0]
        V = (N / self.Max_AD) * self.__V_REF
        return V