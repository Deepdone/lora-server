from enum import Enum, unique
from data_record import data_record_fl

SHORT_ADDRESS_BYTES = 4
FULL_ADDRESS_BYTES = 8

AUTHENTICATION_KEY_BYTES = 16
AUTHENTICAITON_BLOCK_BYTES = 16

ENCRYPTION_KEY_BYTES = 16
ENCRYPTION_BLOCK_BYTES = 16

NODE_WINDOWS_TIME_MS = 1000
NODE_WINDOWS_TIME_US = 1000000
MAX_TRANSMIT_DELAY_FROM_NODE2SERVER_MS = 450


INVALID_SNR = -157
ASSUMED_SNR_OF_MISSING_FRAMES_CB = -250
SNR_MARGIN_CB = 100

MAX_DATA_RAGE = 100000000

DEFAULT_GATEWAY_TRANSMIT_POWER_DBM = 14
DEFAULT_GATEWAY_TRANSMIT_BW_KHZ = 125
DEAULT_GATEWAY_TRANSMIT_ANTENNA = 0

GATEWAY_KEEP_ALIVE_PERIOD_MS = (3*24*60*60*1000)
GATEWAY_TIMEOUT_MULTIPLE = 6

MAC_HEADER_LENGTH = 1
MIN_DATA_HEADER_LENGTH = 7
MAX_HEADER_OPTION_LENGTH = 15  # 0x0f
MAX_OPTION_RECORD_LENGTH = 8
PORT_LENGTH = 1
MIC_BYTES = 4  # message intergrity code
MAX_FRAME_LENGTH = 64

MAX_DATA_BYTES = MAX_FRAME_LENGTH - \
    (MAC_HEADER_LENGTH+MIN_DATA_HEADER_LENGTH+PORT_LENGTH+MIC_BYTES)


NUMBER_OF_SPREADING_FACTORS = 6

default_keys = [b'\x11', b'\x22', b'\x33', b'\x44',
                b'\x55', b'\x66', b'\x77', b'\x88',
                b'\x99', b'\xAA', b'\xBB', b'\xCC',
                b'\xDD', b'\xEE', b'\xFF', b'\x00']


@unique
class FrameType(Enum):
    JOIN_REQUEST_FRAME = 0
    JOIN_ACCEPT_FRAME = 1
    DATA_UNCONFIRMED_FRAME_UP = 2
    DATA_UNCONFIRMED_FRAME_DOWN = 3
    DATA_CONFIRMED_FRAME_UP = 4
    DATA_CONFIRMED_FRAME_DOWN = 5
    NUMBER_OF_FRAME_TYPES = 6


@unique
class OptionID(Enum):
    LINK_CHECK = 2
    LINK_ADDR = 3
    DEV_STATUS = 6


@unique
class ModeType(Enum):
    LORA_MODE = 0
    FSK_MODE = 1


@unique
class SpreadingFactor(Enum):
    MIN_SPREADING_FACTOR = 7
    MAX_SPREADING_FACTOR = MIN_SPREADING_FACTOR + NUMBER_OF_SPREADING_FACTORS - 1
    # DEFAULT_SPREADING_FACTOR = MAX_SPREADING_FACTOR
    UNKNOWN_SPREADING_FACTOR = 256


class CypherKey(data_record_fl):

    def __init__(self, mydata=[]):
        super(CypherKey, self).__init__(int(), ENCRYPTION_KEY_BYTES, mydata)
        if len(mydata) == 0:
            self.initialise(256)


auth_entication_key_default = CypherKey(default_keys)
encryption_key_default = CypherKey(default_keys)


## 小端模式存储数据
def read_byte_value(input, length):
    if len(input) >= length:
        return sum([input[i]*256**i for i in range(length)])
    else:
        raise IndexError("input data len less than %d" % length)


def write_byte_value(input, output, length):
    if not isinstance(output, list):
        raise ValueError("output must be list.")
    else:
        for i in range(length):
            output.append(input[length-1-i])

def encrypt():
    pass

def decrypt():
    pass

class data_rate:

    def __init__(self, bw_khz=DEFAULT_GATEWAY_TRANSMIT_BW_KHZ, sp_f = SpreadingFactor.MAX_SPREADING_FACTOR):
        self.modulation_bw_khz = bw_khz
        self.spreading_factor = sp_f

    def valid(self):
        return self.modulation_bw_khz != 0 and self.spreading_factor != 0

class coding_rate:
    def __init__(self, numerator=0, denominator=0):
        self.numerator = numerator
        self.denominator = denominator

    def valid(self):
        return self.numerator != 0 and self.denominator != 0


if __name__ == '__main__':
    ckey = CypherKey()
    print(ckey.data)
    input = [1,2,3,4]
    val = read_byte_value(input, 4)
    print('%d' % val)
    output = []
    write_byte_value(input, output, 4)
    print(output)

