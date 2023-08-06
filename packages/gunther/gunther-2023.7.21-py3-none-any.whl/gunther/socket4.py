##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################
import socket
import struct


class Socket4(socket.socket):
    mcast_addr = "224.0.0.251"
    mcast_port = 5353

    def __init__(self, grp=None, ttl=1, loopback=1):
        super().__init__(socket.AF_INET,socket.SOCK_DGRAM)

        ttl = struct.pack('b', ttl)
        self.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        self.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_LOOP, loopback)

        if grp is None:
            grp = (self.mcast_addr, self.mcast_port)
        self.group = grp

        # allow multiple connections
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        self.bound = False

    def mbind(self):
        # setup service socket
        try:
            self.bind(('0.0.0.0', self.mcast_port))
            # self.sock.bind(('::', self.mcast_port))
            # self.sock.bind(self.group)
            # self.sock.bind(('', self.mcast_port))
        except OSError as e:
            raise Exception("*** {} ***".format(e))

        mreq = struct.pack("=4sl", socket.inet_aton(self.mcast_addr), socket.INADDR_ANY)
        self.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        self.bound = True

    def mclose(self):
        if self.bound:
            # mreq = socket.inet_aton(self.mcast_port) + socket.inet_aton('0.0.0.0')
            mreq = struct.pack("=4sl", socket.inet_aton(self.mcast_addr), socket.INADDR_ANY)
            self.setsockopt(socket.SOL_IP, socket.IP_DROP_MEMBERSHIP, mreq)
        self.close()

