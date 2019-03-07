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
v_ref = 3.0

# Command Byte Values
# Format: SD C2 C1 C0 PD1 PD0 X X
# C2 C1 C0 = Channel Address
sd = 1       # Single-ended input
pd1 = 0      # Internal reference OFF
pd0 = 1      # A/D Converter ON


class ADXL377(object):

    def __init__(self, busID, slaveAddr):
        self.__i2c = SMBus(busID)
        self.__slave = slaveAddr

    Max_AD = 4096.0                                 # 12-bit ADC
    V_REF = 3.0                                     # 3V Voltage Reference

    def read_channel(self, channel):
        command = self.format_cmd_byte(channel)
        data = self.__i2c.read_i2c_block_data(self.__slave, command, 2)
        raw_value = data[1] << 8 | (data[0] & 0xF0)
        voltage = (raw_value / self.Max_AD) * v_ref
        g_value = voltage - (v_ref/2)
        return g_value

    def format_cmd_byte(self, channel):
        command = sd << 8 | channel << 4 | pd1 << 3 | pd0 << 2 | 0b00
        return command

    def get_accel_values(self):
        x_axis = self.read_channel(0)
        y_axis = self.read_channel(1)
        z_axis = self.read_channel(2)

        return '{:.1f}'.format(x_axis), '{:.1f}'.format(y_axis), '{:.1f}'.format(z_axis)