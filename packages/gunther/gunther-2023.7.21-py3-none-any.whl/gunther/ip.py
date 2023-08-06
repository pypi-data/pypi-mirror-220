##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################
import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        n = socket.gethostname()
        # make sure it has a zeroconfig .local or you end up
        # with 127.0.0.1 as your address
        if n.find('.local') < 0:
            n += '.local'
        hostname = n

        # doesn't even have to be reachable
        s.connect(('8.8.8.8', 10000))
        IP = s.getsockname()[0]
    except:
        try:
            IP = socket.gethostbyname(n)
        except:
            IP = '127.0.0.1'
    finally:
        s.close()

    return (IP, hostname,)
