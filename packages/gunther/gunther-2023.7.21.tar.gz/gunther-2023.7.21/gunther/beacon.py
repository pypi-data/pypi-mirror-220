##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################
import time
from .transport import Ascii, Json, Raw
from .socket4 import Socket4
from .socket6 import Socket6
from socket import AF_INET, AF_INET6
import socket # need for exception

class Beacon:
    # family: af_net[6]
    # type: dgram
    # proto: 0?
    def __init__(self, group=None, loopback=1, handler=Json, ttl=1, family=AF_INET):
        if family not in [AF_INET,AF_INET6]:
            raise "invalide faily"
        if family == AF_INET:
            self.sock = Socket4()
        elif family == AF_INET6:
            self.sock = Socket6()
        else:
            raise Exception("Invalid addressing:", type)

        self.handler = handler()


    def __del__(self):
        self.close()

    def close(self):
        self.sock.mclose()

    def broadcast(self, msgs, delay=1.0):
        while True:
            for msg in msgs:
                msg = self.handler.dumps(msg)
                self.sock.sendto(msg, self.sock.group)
            time.sleep(delay)
            print(".", end="",flush=True)

    def listen(self, wait):
        self.sock.mbind()

        self.sock.setblocking(1)
        # self.sock.settimeout(1.0)

        epoch = time.time()
        ret = []

        while (time.time()-epoch) < wait:
            # time.sleep(0.1)
            try:
                data, address = self.sock.recvfrom(64)
                data = self.handler.loads(data)
                # print(f">> {address}: {data}")
                # m = (address, data)
                m = data
                if m not in ret:
                    ret.append(m)

            except socket.timeout:
                # print("e")
                continue
            except Exception as e:
                print(f"{e}")
                break
                ret = []
                # continue
        return ret

    def stream(self, func=print, nbytes=128):
        self.sock.mbind()
        self.sock.setblocking(1)
        # self.sock.settimeout(1.0)

        while True:
            try:
                data, address = self.sock.recvfrom(nbytes)
                data = self.handler.loads(data)
                # print(f">> {address}: {data}")
                func(data)

            except socket.timeout:
                continue
            except Exception as e:
                print(f"{e}")