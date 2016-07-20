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

    def __init__(self, ver, token, plt_type):
        self.structs = struct.Struct("<BHB")
        self.ver = ver
        self.token = token
        self.plt_type = plt_type
        self.data = self.structs.pack(self.ver, self.token, self.plt_type)


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


class FramePayload():
    def __init__(self, *args, **kargs):
        pass


def udpclient():
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = ("localhost", 1680)
    head = FrameHead(2, 65535, PKT_TYPE.PULL_DATA.value)
    macaddr = FrameMac(11)
    print(head.data+macaddr.data)
    sdl = client_sock.sendto(head.data+macaddr.data, addr)
    recv_data, recv_addr = client_sock.recvfrom(1024)
    print("send %d data, recv data: %s" % (sdl, recv_data))

    client_sock.close()

if __name__ == "__main__":
    udpclient()