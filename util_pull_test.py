# Assuming it's a stream (TCP) socket, you need to implement your own message 
# framing mechanism (or use an existing higher level protocol that does so). 
# One straightforward way is to define each message as a 32-bit integer length 
# field, followed by that many bytes of data.
# 
# Sender: take the length of the JSON packet, pack it into 4 bytes with the 
# struct module, send it on the socket, then send the JSON packet.
# 
# Receiver: Repeatedly read from the socket until you have at least 4 bytes of 
# data, use struct.unpack to unpack the length. Read from the socket until you 
# have at least that much data and that's your JSON packet; anything left over 
# is the length for the next message.
# 
# If at some point you're going to want to send messages that consist of 
# something other than JSON over the same socket, you may want to send a message
# type code between the length and the data payload; congratulations, you've 
# invented yet another protocol.
# 
# Another, slightly more standard, method is DJB's Netstrings protocol; it's 
# very similar to the system proposed above, but with text-encoded lengths 
# instead of binary; it's directly supported by frameworks such as Twisted.

from enum import Enum, unique
import struct, binascii, socket
import json


PROTOCOL_VERSION = 2


@unique
class PKT_TYPE(Enum):
    PUSH_DATA = 0
    PUSH_ACK  = 1
    PULL_DATA = 2
    PULL_RESP = 3
    PULL_ACK  = 4
    TX_ACK    = 5


class FrameHead():

    def __init__(self, ver=PROTOCOL_VERSION, token=0, plt_type=PKT_TYPE.PUSH_DATA.value):
        self.structs = struct.Struct("<BHB")
        self.ver = ver
        self.token = token
        self.plt_type = plt_type
        self.data = self.structs.pack(self.ver, self.token, self.plt_type)
        self._len = len(self.data)

    @property
    def len(self):
        return self._len

    @classmethod
    def parse(cls, data):
        cls = FrameHead()
        cls.data = data
        cls.ver, cls.token, cls.plt_type = cls.structs.unpack(cls.data[:cls._len])
        return cls



class FrameMac():
    def __init__(self, address):
        self.structs = struct.Struct("<q")
        if isinstance(address, int):
            self.address = address
        elif isinstance(address, str):
            self.address = int(address, 16)
        else:
            raise "frameHead init() input 'address' is error"

        self.data = self.structs.pack(self.address)


class Node():
    def __init__(self):
        pass


class FramePayload():
    def __init__(self, pld):
        self.structs = struct.Struct("%ds" % len(pld))
        self.pld = pld
        self.data = json.dumps(self.pld)


node = {
    'time': '2013-03-31T16:21:17.532038Z',
    'tmst': 3316387610,
    'chan': 0,
    'rfch': 0,
    'freq': 863.00981,
    'stat': 1,
    'modu': 'LORA',
    'datr': 'SF10BW125',
    'codr': '4/7',
    'rssi': -38,
    'lsnr': 5.5,
    'size': 32,
    'data': 'ysgRl452xNLep9S1NTIg2lomKDxUgn3DJ7DE+b00Ass'
}

packet = {
    'rxpk': []
}

packet['rxpk'].append(node)

# head = FrameHead(2, 65535, PKT_TYPE.PULL_DATA.value)
# test = FrameHead.parse(head.data)

def udpclient():

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = ("localhost", 1680)
    # pull data
    print("-----PULL DATA-----")
    head = FrameHead(PROTOCOL_VERSION, 65535, PKT_TYPE.PULL_DATA.value)
    macaddr = FrameMac(11)
    send_data = head.data + macaddr.data
    sdl = client_sock.sendto(send_data, addr)
    print("send data %s" % (send_data))

    recv_data, recv_addr = client_sock.recvfrom(1024)
    print("recv data: %s" % (recv_data))

    recv_head = FrameHead.parse(recv_data)

    # push data
    print("-----PUSH DATA-----")
    head = FrameHead(2, 65535, PKT_TYPE.PUSH_DATA.value)
    macaddr = FrameMac(11)
    payload = FramePayload(packet)
    print(payload.data)
    sdl = client_sock.sendto(head.data+macaddr.data+payload.data.encode(), addr)

    client_sock.close()


if __name__ == "__main__":
    print("call...")
    udpclient()
