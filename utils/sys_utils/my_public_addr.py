from requests import get
from utils.sys_utils import my_addr
import socket

def _validate_ip(addr):

    try:

        socket.inet_aton(addr)

    except OSError:

        return(False)

    else:

        return(addr)

def _getPublicIP():

        try:
            _ip = get('https://ifconfig.me').text
        except:
            try:
                _ip = get('https://api.ipify.org').text
            except:
                try:
                    _ip = get('http://ip-api.com/json').json()['query']
                except:
                    _ip = False

        _ip = _validate_ip(str(_ip))

        if (_ip == False):

            return(my_addr.addr()[1])

        return(_ip)

def addr():

    return(_getPublicIP())
