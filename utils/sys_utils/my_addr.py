import socket

def addr(routerip='8.8.8.8'):

    hostname = socket.gethostname()

    try:

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect((routerip, 80))
        
        address = sock.getsockname()[0]

        sock.close()

    except:
        
        address = socket.gethostbyname(hostname)

    return((hostname, address))
