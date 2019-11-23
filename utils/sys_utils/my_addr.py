import socket

def addr():

    hostname = socket.gethostname()
    address = socket.gethostbyname(hostname)

    return((hostname, address))
