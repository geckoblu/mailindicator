"""-"""
# From http://code.activestate.com/recipes/439093-get-names-of-all-up-network-interfaces-linux-only/
import array
import fcntl
import socket
import struct


def _all_interfaces():
    max_possible = 128  # arbitrary. raise if needed.
    bytez = max_possible * 32
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    names = array.array('B', '\0' * bytez)
    outbytes = struct.unpack('iL', fcntl.ioctl(
        sock.fileno(),
        0x8912,  # SIOCGIFCONF
        struct.pack('iL', bytez, names.buffer_info()[0])
    ))[0]
    namestr = names.tostring()
    return [namestr[i:i + 32].split('\0', 1)[0] for i in range(0, outbytes, 32)]


def network_available():
    """Check if a network connection is available"""
    for interf in _all_interfaces():
        if interf != 'lo':
            return True
    return False
