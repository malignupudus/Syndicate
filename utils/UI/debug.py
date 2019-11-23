import socket

debug = lambda wrapper, message, level: wrapper.log(message, level)

INF = 1
WAR = 2
PER = 3
COM = 4

class log(object):

    def __init__(self, address=None, username=None, log=None, rdns=False, rport=False):

        self.address = address

        (address, port) = address

        address_string = '%s:%s' % (address, port)

        if (rdns == True):

            try:

                _resolve_hostname = socket.getfqdn(socket.gethostbyname(address))

            except:

                _resolve_hostname = 'null'

        else:

            _resolve_hostname = 'null'

        if (rport == True):

            try:

                _resolve_port = socket.getservbyport(int(port))
        
            except:

                _resolve_port = 'null'

        else:

            _resolve_port = 'null'

        if (rdns == True) or (rport == True):

            address_string += ' (%s:%s)' % (_resolve_hostname, _resolve_port)

        if not (username == None):
            
            self.message = '[{0}]: ({1}): %s'.format(address_string, username)
        
        else:
            
            self.message = '[{0}]: %s'.format(address_string)
        
        self.log = log

    def logger(self, text, level):

        debug(self.log, self.message % (text), level)
        return(text)
