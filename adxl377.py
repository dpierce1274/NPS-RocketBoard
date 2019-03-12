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
        g_value = voltage - (v_ref/2)
        return voltage

    def format_cmd_byte(self, channel):
        command = channel << 4 | 0x8C
        return command

    def get_accel_values(self):
        x_axis = self.read_channel(channel_0)
        y_axis = self.read_channel(channel_1)
        z_axis = self.read_channel(channel_2)
        return '{:.6f}'.format(x_axis), '{:.6f}'.format(y_axis), '{:.6f}'.format(z_axis)
