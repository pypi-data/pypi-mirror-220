##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################
import socket
import struct


IN6ADDR_ANY = "::" # ipv6 version of inaddr_any

class Socket6(socket.socket):
    mcast_addr = "ff02::fb"
    mcast_port = 5353

    def __init__(self, grp=None, ttl=1, loopback=1):
        super().__init__(socket.AF_INET6,socket.SOCK_DGRAM)

        ttl_bin = struct.pack('@i', 1)
        self.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl)
        self.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, loopback)

        if grp is None:
            grp = (self.mcast_addr, self.mcast_port)
        self.group = grp

        # Loopback interface always has ifindex == 1.
        ifindex = 0
        packed_ifindex = struct.pack("I", ifindex)
        # self.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_IF, packed_ifindex)

        # allow multiple connections
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    def mbind(self):
        # setup service socket
        try:
            self.bind(('::', self.mcast_port))
        except OSError as e:
            raise Exception("*** {} ***".format(e))

        # mreq = socket.inet_pton(socket.AF_INET6, self.mcast_addr) + struct.pack("@I", 0)
        # inaddr = socket.inet_pton(socket.AF_INET6, IN6ADDR_ANY)
        # mreq = struct.pack("=16si", socket.inet_pton(socket.AF_INET6, self.mcast_addr), inaddr)
        mreq = socket.inet_pton(socket.AF_INET6, self.mcast_addr)
        self.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)
        # self.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_ADD_MEMBERSHIP, mreq)

    def mclose(self):
        # mreq = socket.inet_pton(socket.AF_INET6, self.mcast_addr)
        # self.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_LEAVE_GROUP, mreq)
        self.close()

