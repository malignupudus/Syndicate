#!/usr/bin/env python3

import sys

if (sys.version_info.major != 3):

    print('\033[1;37m¡Debes usar la versión \033[4;33m3\033[37;0;1m de \033[33;4mPython\033[37;0;1m para poder ejecutarme!\033[0m')
    sys.exit(1)

import threading
import re
import ssl
import random
import importlib
import inspect
import socks
import subprocess
from pager import getchars
from urllib.parse import urlparse
from hashlib import sha1
from time import strftime, sleep
from os import makedirs, getpid, kill, listdir, name as get_os_name
from os.path import isdir, isfile
from uuid import uuid4
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from base64 import b64encode, b64decode
from secrets import token_urlsafe

# Configuration

from conf import global_conf

# Custom modules

from modules.UI import argprogrammer
from modules.UI import simplelogging as logging
from modules.Connections import convex
from modules.Ciphers import POO_RSA

# Utilities

try:
    from utils.Wrappers import wrap
except Exception as Except:
    print(str(Except))
    sys.exit(1)

from utils.Executes import execute_command
from utils.Checks import check_credentials
from utils.UI import return_log
from utils.Checks import key_check_in_dict
from utils.Extracts import extract_http_post_data
from utils.Ciphers import hibrid
from utils.Checks import check_administrators
from utils.Executes import execute_command_to_admin
from utils.Ciphers import generate_uniqkey
from utils.Executes import execute_public_command
from utils.UI import debug
from utils.Ciphers import _decrypt_rsa_private_key
from utils.Ciphers import simplycrypt
from utils.Connections import connector
from utils.sys_utils import separate_space
from utils.Shows import show_user_admins
from utils.Shows import show_user_rooks
from utils.Checks import is_complement
from utils.sys_utils import convert
from utils.sys_utils import freplace

# Defend's

from defend import defend

# Configuration

root = global_conf.conf['conf_dir']
confilename = '%s/%s' % (root, global_conf.conf['conf_file'])
group_name = global_conf.conf['group_name']
complement_path = global_conf.databases['complements']
list_complements = listdir(complement_path)

key_not_found_message = 'La clave "%s" no existe por favor configurala para continuar ...'

# Variables globales

init = False
conf_hash = None
new_conf = True
log_error_bool = False
token = None
new_token = False
secret_key = None
new_secret_key = False
use_keys = True
request_count = 0
request_count_safe = {
        
                        'GET':0,
                        'POST':0,
                        'AUTH':0,
                        'HEAD':0,
                        'user_agent_BLOCK':0,
                        'address_BLOCK':0
        
                    }

def exit_force(message=None):
    
    if not (message == None):
        
        print(message)

    kill(getpid(), 15)

evalue = lambda value: not value == None # Función para evaluar si un resultado es True
key_detect = lambda dict_, keys: [exit_force(key_not_found_message % (x)) for x in keys if (key_check_in_dict.check(dict_, x) == False)]

# Complements

complements_info = {}

for _ in list_complements:

    complement_file = '{}/{}/evie/params.py'.format(complement_path, _)

    if (isfile(complement_file)):

        complement_name = complement_file.replace('/', '.')

        try:

            mod = importlib.import_module(complement_name[:-3])

        except Exception as Except:

            print('Exception in file "{}": {}'.format(complement_file, Except))
            sys.exit(1)

        else:

            if (hasattr(mod, 'communicate')):

                if (isfunction(getattr(mod, 'communicate'))):

                    try:

                        complements_info[_] = getattr(mod, 'communicate')()

                    except Exception as Except:

                        print('RuntimeError in file "{}": {}'.format())
                        sys.exit(1)

# Log codes

INF = debug.INF
WAR = debug.WAR
PER = debug.PER
COM = debug.COM

# Args

group_optionals = 'Opcionales'

parser = argprogrammer.Parser()

parser.set_head('''
       Syndicate Project - Servidor principal
       -----------------   ------------------''')

parser.add(['-h', '--help'], 'help', 'Mostrar la ayuda y sale', group=group_optionals)
parser.add(['-P', '--rsa-passphrase'], 'rsa_passphrase', 'La frase de contraseña para desencriptar la clave privada', group='Parámetros requeridos')
parser.add(['-s', '--show-complements'], 'show_complements', 'Mostrar los complementos de syndicate', type=bool, action=True, group=group_optionals)

args = parser.parse_args()

rsa_passphrase = args.rsa_passphrase
show_complements = args.show_complements

if (show_complements == True):

    if (list_complements == []):

        print('No hay complementos actualmente ...')

    else:

        for i, _ in enumerate(list_complements):

            if (is_complement.check(_)):

                print('\033[1;32m{}\033[0m \033[37m~\033[0m \033[1;37m{}\033[0m'.format(i, _))

    sys.exit(0)

else:

    if (rsa_passphrase == None):

        print('No has definido la frase de contraseña de la clave privada ...')
        sys.exit(1)

    for _ in list_complements:

        folder_name = '{}/{}'.format(complement_path, _)

        if (isdir(folder_name)):

            if not (is_complement.check(_)) and not (re.match(r'_{2,}.+_{2,}', _)):

                print('{} no es un complemento válido'.format(_))
                sys.exit(1)

try:

    if (show_user_admins.show() == []) or (show_user_rooks == []):

        print('Necesitas por lo menos un ROOK y un ADMINISTRADOR, para poder continuar ...')
        sys.exit(1)

except wrap.incorrect_passphrase:

    print('La frase de contraseña del almacén es incorrecta!')
    sys.exit(1)

def generate_keys(size):

    rsa = POO_RSA.main()
    rsa.generate(size, rsa_passphrase)
    (pub_key, priv_key) = rsa.export()

    return({'public_key':pub_key, 'private_key':priv_key})

def loop_config(close=False):

        # Globals vars

        # Globals

        global conf_hash, new_conf, use_keys, init

        # Server

        global realm, LHOST, LPORT, RPATH, public_key, private_key, resolve_dns, resolve_port

        # Login

        global false_username, false_passphrase, recover, max_retry, retry_seconds, denied_method

        # honeypot

        global blacklist, honeypot_list, tools, user_agent_list, regular_expression_for_address, regular_expression_for_userAgent, re_options

        # style

        global time, logger, logs

        # templates

        global TEMPLATE_FOLDER, TEMPLATE_ERROR404, TEMPLATE_ERROR511, TEMPLATE_ERROR400, TEMPLATE_ERROR403, TEMPLATE_CREDENTIALS, webmaster_email, TEMPLATE_ERROR500

        # TOKEN SYSTEM:
        ###############
        
        global token, new_token

        # SECRET KEY SYSTEM:
        ####################

        global secret_key, new_secret_key
        
        while (True):
 
            try:

                # Configuration

                conf_file = wrap.getall(wrap.USE_CONFIG)

                if (conf_file == {}):

                    exit_force('Aún no se escriben datos en el archivos de configuración ...')

                else:

                    # check config

                    key_detect(dict(conf_file), [group_name])
                    conf = dict(conf_file[group_name])
                    new_conf_hash = sha1(str(conf).encode()).hexdigest() 

                    if (new_conf_hash != conf_hash):

                        conf_hash = new_conf_hash

                        # Check global config

                        key_detect(conf, ['proxy', 'login', 'server', 'templates', 'honeypot', 'style'])

                        # Style configuration

                        style = conf['style']

                        # Check Style

                        key_detect(style, ['time', 'log'])

                        time = str(style['time'])
                        style_log = 'logs/%s' % (strftime('%H.%m.%S.%d-%m-%Y.log')) if (convert.convert_bool(style['log']) == True) else False
                        logger = logging.logger(output=style_log, time_format=time)

                        # Server configuration

                        server = conf['server']

                        # Check Server

                        key_detect(server, ['sys_version', 'server_version', 'realm', 'lhost', 'lport', 'rpath', 'rdns', 'rport', 'public_service', 'user_agent', 'nodes_rule', 'cipher_file'])

                        realm = str(server['realm'])
                        LHOST = str(server['lhost'])
                        LPORT = convert.convert_int(server['lport'])
                        BaseHTTPRequestHandler.sys_version = str(server['sys_version'])
                        BaseHTTPRequestHandler.server_version = str(server['server_version'])
                        RPATH = str(server['rpath'])
                        bit_size = convert.convert_int(server['bit_size']) 
                        resolve_dns = convert.convert_int(server['rdns'])
                        resolve_port = convert.convert_int(server['rport'])
                        cipher_file = convert.convert_bool(server['cipher_file'])

                        # Comunicación
                        
                        execute_command_to_admin.RULE = str(server['nodes_rule'])
                        execute_command_to_admin.cipher_file = cipher_file
                        execute_command.cipher_file = cipher_file
                        execute_command.parse_args = complements_info

                        if (re.match(r'(?!(RANDOM|STRICT))', execute_command_to_admin.RULE)):

                            execute_command_to_admin.RULE = random.choice(['STRICT', 'RANDOM'])
                            logger.log('Regla inválida; Usando "{}" como regla...'.format(execute_command_to_admin.RULE), WAR)

                        execute_public_command.public_service = [x.strip() for x in str(server['public_service']).split(',')] if not (convert.convert_bool(server['public_service']) == True) else False
                        execute_public_command.user_agent = str(server['user_agent'])

                        # Proxy configuration

                        proxy = conf['proxy']

                        # Check proxy

                        key_detect(proxy, ['proxy_list'])
                        proxy_list = proxy['proxy_list']

                        if (convert.convert_bool(proxy_list)):

                            try:

                                proxy_list = convert.convert_dict(proxy_list)

                            except Exception as Except:

                                logger.log('Error parseando los datos. Excepción: {}'.format(Except), COM)
                                logger.log('No se usara un proxy :/ ...', WAR)

                            else:

                                if (proxy_list.get('proxy') == None):

                                    logger.log('No configuró correctamente los valores de los proxy\'s...', WAR)

                                else:

                                    current_proxy = random.choice(proxy_list['proxy'])

                                    for _ in ['proxy_type', 'proxy_addr', 'proxy_port', 'rds', 'username', 'password']:

                                        if (key_check_in_dict.check(current_proxy, _) == False):

                                            current_proxy = False
                                            logger.log('{} no está definido...', WAR)
                                            break

                                    if not (current_proxy == False):

                                        proxy_requirement_type = (isinstance(current_proxy['proxy_type'], str) and current_proxy['proxy_type'] in ['SOCKS4', 'SOCKS5', 'HTTP'])
                                        proxy_requirement_addr = isinstance(current_proxy['proxy_addr'], str)
                                        proxy_requirement_port = isinstance(current_proxy['proxy_port'], int)
                                        proxy_requirement_rds = isinstance(current_proxy['rds'], bool)
                                        proxy_requirement_username = (isinstance(current_proxy['username'], str) or current_proxy['username'] == None)
                                        proxy_requirement_password = isinstance(current_proxy['password'], str) or current_proxy['password'] == None

                                        if (proxy_requirement_addr) and (proxy_requirement_port) and (proxy_requirement_rds) and (proxy_requirement_username) and (proxy_requirement_password):

                                            try:

                                                convex.transfor(proxy_type=socks.PROXY_TYPES.get(current_proxy['proxy_type']), proxy_addr='{}:{}'.format(current_proxy['proxy_addr'], current_proxy['proxy_port']), rdns=current_proxy['rds'], username=current_proxy['username'], password=current_proxy['password'])
                                                
                                            except Exception as Except:

                                                logger.log('No se pudo configurar el proxy. Excepcion: {}'.format(Except))

                                            else:

                                                logger.log('Proxy: {}://{}:{}'.format(current_proxy['proxy_type'], current_proxy['proxy_addr'], current_proxy['proxy_port']), PER)

                                        else:

                                            logger.log('Algunos tipos de datos no son correctos, por lo tanto no se puede configurar el proxy')

                                    else:

                                        logger.log('No se puede usar un proxy, porque no está siguiendo la especificación acordada', WAR)

                        else:

                            convex.restruct()

                        # Log in configuration

                        login = conf['login']

                        # Check Log in

                        key_detect(login, ['false_username', 'false_passphrase', 'recover', 'max_retry', 'retry_seconds', 'denied_method'])
                        
                        max_retry = convert.convert_int(login['max_retry'])
                        retry_seconds = convert.convert_int(login['retry_seconds'])
                        denied_method = str(login['denied_method'])
                        false_username = str(login['false_username'])
                        false_passphrase = str(login['false_passphrase'])
                        recover = convert.convert_bool(login['recover'])

                        # Simple Honeypot configuration

                        simpleHoneypot = conf['honeypot']

                        # Check Simple Honeypot

                        key_detect(simpleHoneypot, ['blacklist', 'honeypot_list', 'tools', 'user_agent_black_list', 'regular_expression_for_address', 'regular_expression_for_userAgent', 're_options'])

                        re_options = convert.convert_int(simpleHoneypot['re_options'])
                        regular_expression_for_address = str(simpleHoneypot['regular_expression_for_address'])
                        regular_expression_for_userAgent = str(simpleHoneypot['regular_expression_for_userAgent'])
                        blacklist = str(simpleHoneypot['blacklist'])
                        honeypot_list = str(simpleHoneypot['honeypot_list'])
                        tools = str(simpleHoneypot['tools'])
                        user_agent_list = str(simpleHoneypot['user_agent_black_list'])

                        # Server keys

                        _server_keys = wrap.read('keys', agent=wrap.USE_SERVER)

                        if (_server_keys == False):

                            logger.log('El par de claves aún no son son generados ... generando ...', WAR)
                            logger.log('Tamaño a generar: "%d"' % (bit_size), PER)

                            _keys = generate_keys(bit_size)
                            (public_key, private_key) = (_keys['public_key'], _keys['private_key'])

                            if (wrap.add('keys', _keys, agent=wrap.USE_SERVER) == True):

                                logger.log('El par de claves fueron generadas ...')
                                logger.log('Desencriptando ...')

                                try:

                                    private_key = _decrypt_rsa_private_key._decrypt(private_key, rsa_passphrase)

                                except ValueError:

                                    logger.log('Error desencriptado la clave privada ...', COM)
                                    exit_force()

                                else:

                                    logger.log('¡Clave desencriptada!')

                            else:

                                logger.log('Error escribiendo las claves en el almacén ...', COM)
                                exit_force()

                        else:

                            if (use_keys == True):

                                use_keys = False

                                (public_key, private_key) = (_server_keys['public_key'], _server_keys['private_key'])

                                logger.log('Desencriptando clave privada ...')

                                try:

                                    private_key = _decrypt_rsa_private_key._decrypt(private_key, rsa_passphrase)

                                except ValueError:

                                    logger.log('Error desencriptado la clave privada ...', COM)
                                    exit_force()

                                else:

                                    logger.log('Clave desencriptada con éxito.')

                        # Local information

                        templates = conf['templates']

                        # Check Local information

                        key_detect(templates, ['folder', 'error400', 'error404', 'error403', 'error511', 'credentials', 'webmaster_email', 'error500'])

                        TEMPLATE_FOLDER = str(templates['folder'])
                        TEMPLATE_ERROR400 = '%s/%s' % (TEMPLATE_FOLDER, templates['error400'])
                        TEMPLATE_ERROR404 = '%s/%s' % (TEMPLATE_FOLDER, templates['error404'])
                        TEMPLATE_ERROR403 = '%s/%s' % (TEMPLATE_FOLDER, templates['error403'])
                        TEMPLATE_ERROR511 = '%s/%s' % (TEMPLATE_FOLDER, templates['error511'])
                        TEMPLATE_ERROR500 = '%s/%s' % (TEMPLATE_FOLDER, templates['error500'])
                        TEMPLATE_CREDENTIALS = '%s/%s' % (TEMPLATE_FOLDER, templates['credentials'])
                        webmaster_email = templates['webmaster_email']

                        # Server information

                        if (RPATH == 'RANDOM'):

                            RPATH = token_urlsafe(convert.convert_int(global_conf.token['path_max_length']))

                        if not (new_conf == True):
                            
                            logger.log('Se actualizo la configuración!')

                        else:

                            new_conf = False

                    _secret_key = wrap.read('secret_key', 'secret_key', agent=wrap.USE_SECRET_KEY)

                    if (_secret_key == False):

                        logger.log('Generando clave secreta ...')

                        secret_key = separate_space.separate(generate_uniqkey.generate())
                        new_secret_key = True

                        if (wrap.add('secret_key', {'secret_key':secret_key}, agent=wrap.USE_SECRET_KEY)):

                            logger.log(f'Clave secreta generada -> {secret_key}', PER)

                        else:

                            logger.log('Error generando la clave secreta ...', COM)
                            exit_force()

                    else:

                        if (_secret_key != secret_key):

                            if (new_secret_key == False):

                                logger.log(f'Clave secreta -> {_secret_key}', PER)

                                new_secret_key = True
                    
                            else:

                                logger.log(f'Clave secreta actualizado -> {_secret_key}', PER)

                            secret_key = _secret_key

                    _token = wrap.read('token', 'token', agent=wrap.USE_TOKEN)

                    if (_token == False):

                        logger.log('Generando un nuevo token de acceso ...')

                        token = generate_uniqkey.generate()
                        new_token = True

                        if (wrap.add('token', {'token':token}, agent=wrap.USE_TOKEN)):

                            logger.log(f'Token de acceso generado -> {token}', PER)

                        else:

                            logger.log('Error generando el token de acceso ...', COM)
                            exit_force()

                    else:

                        if (_token != token):

                            if (new_token == False):

                                logger.log(f'Token de acceso -> {_token}', PER)

                                new_token = True
                    
                            else:

                                logger.log(f'Token actualizado -> {_token}', PER)

                            token = _token

                if (close == True):

                    break

                else:

                    init = True

                sleep(1)

            except Exception as Except:

                exit_force('Error en la configuración: "{}"'.format(Except))

def get_info():

    while (True):

        try:

            key = getchars()

        except KeyboardInterrupt:

            break

        else:

            if (init == True):

                key = ''.join(key)

                if (key == '\n'): # ENTER

                    logger.log('Escuchando en :: %s://%s:%d/%s' % (proto, LHOST, LPORT, RPATH), PER)

                elif (key == '\x12'): # CTRL-R

                    logger.log('Total de peticiones hechas: %d' % (request_count))

                elif (key == '\x0e'): # CTRL-N

                    logger.log('GET:%d ~ POST:%d ~ HEAD:%d ~ AUTH:%d ~ Address:(BLOCK:%d) ~ User-Agent:(BLOCK:%d)' % (
                                                                            request_count_safe.get('GET'),
                                                                            request_count_safe.get('POST'),
                                                                            request_count_safe.get('HEAD'),
                                                                            request_count_safe.get('AUTH'),
                                                                            request_count_safe.get('address_BLOCK'),
                                                                            request_count_safe.get('user_agent_BLOCK')
                                                                            
                                                                        ))
                else:

                    logger.log('{} es una tecla inválida, presiona otra vez...'.format(repr(key)), COM)


loop_config(True) # Ajustamos los valores de forma sincronizada

loop_config_thread = threading.Thread(target=loop_config)
loop_config_thread.setDaemon(True)
loop_config_thread.start()

get_info_thread = threading.Thread(target=get_info)
get_info_thread.setDaemon(True)
get_info_thread.start()

class handler(BaseHTTPRequestHandler):

    def imprint(self, message, code):

        log = debug.log(address=self.client_address, log=logger, rdns=resolve_dns, rport=resolve_port)

        log.logger(message, code)

    @staticmethod
    def get_contrary(string):

        return(True if (string[0] == '!') else False)

    def get_real_list(self, string):

        return(string[1:] if (self.get_contrary(string) == True) else string)

    @staticmethod
    def get_pattern(string, regular_expression, log):

        if (convert.convert_bool(regular_expression) == True):

            try:

                pattern = re.search(regular_expression, string, re_options)

            except Exception as Except:

                pattern = False
                log('Excepción en la expresión regular: "{}". Excepción: "{}"'.format(repr(regular_expression), Except), WAR)

            else:

                if (pattern):

                    log('Coincidencia {} en {}'.format(regular_expression, string), PER)

        else:

            pattern = False

        return(pattern)

    def eject_to(self, blacklist, string, regular_expression, log):

        contrary = self.get_contrary(blacklist)
        blacklist = self.get_real_list(blacklist)

        pattern = self.get_pattern(string, regular_expression, log)
        cmp_data = (pattern) or (string in [x.strip() for x in blacklist.split(',') if (convert.convert_bool(x))])

        return(contrary != cmp_data)

    def honeypot(self, honeypot_list, client_address, log):

        if (self.eject_to(honeypot_list, client_address, regular_expression_for_address, log) == True):

            if (convert.convert_boool(tools) == True):

                thread = threading.Thread(target=defend.defend, args=(tools, self.client_address, LHOST, LPORT, log))
                thread.start()

            else:

                self.imprint('¡No has configurado una lista de herramientas!', WAR)

    def eject(self):

        if (convert.convert_bool(blacklist) == True) or (convert.convert_bool(regular_expression_for_address)):

            if (self.eject_to(blacklist, self.client_address[0], regular_expression_for_address, self.imprint) == True):

                self.imprint('¡No tiene permiso para ingresar a Evie!. Coincidencia: "{}" en la lista negra de direcciones'.format(self.client_address[0]), WAR)
                self.error403()

                request_count_safe['address_BLOCK'] += 1

                return(True)

        elif (convert.convert_bool(user_agent_list) == True) or (convert.convert_bool(regular_expression_for_userAgent)):

            if (self.eject_to(user_agent_list, self.headers['User-Agent'], regular_expression_for_userAgent, self.imprint) == True):

                self.imprint('¡No tiene permiso para ingresar a Evie!. Coincidencia: "{}" en la lista negra de agentes de usuario'.format(self.headers['User-Agent']), WAR)
                self.error403()

                request_count_safe['user_agent_BLOCK'] += 1

                return(True)

        elif (convert.convert_bool(honeypot_list) == True) or (convert.convert_bool(regular_expression_for_address) == True):

            self.honeypot(honeypot_list, self.client_address[0], self.imprint)

        else:

            self.imprint('¡El sistema de prevención de intrusos no está habilitado!', WAR)

    def replace_commands(self, text):
        
        try:

            _path = self.path

        except AttributeError:

            _path = '/'

        return(
                freplace.replace(text, [
                    ('{lhost}', LHOST),
                    ('{lport}', LPORT),
                    ('{server_version}', BaseHTTPRequestHandler.server_version),
                    ('{sys_version}', BaseHTTPRequestHandler.sys_version),
                    ('{webmaster_email}', webmaster_email),
                    ('{cpath}', _path),
                    ('{rhost}', self.client_address[0]),
                    ('{rport}', self.client_address[1])]
                    )
                )

    def error400(self):

        self.send_response(400, 'Bad Request')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(TEMPLATE_ERROR400, 'rt') as obj:
            self.wfile.write(self.replace_commands(obj.read()).encode())

    def error403(self):

        self.send_response(403, 'Forbidden')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(TEMPLATE_ERROR403, 'rt') as obj:
            self.wfile.write(self.replace_commands(obj.read()).encode())
    
    def error404(self):

        self.send_response(404, 'Not Found')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(TEMPLATE_ERROR404, 'rt') as obj:
            self.wfile.write(self.replace_commands(obj.read()).encode())

    def error511(self):

        self.send_response(511, 'Network Authentication Required')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(TEMPLATE_ERROR511, 'rt') as obj:
            self.wfile.write(self.replace_commands(obj.read()).encode())

    def error500(self):

        self.send_response(500)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        with open(TEMPLATE_ERROR500, 'rt') as obj:
            self.wfile.write(self.replace_commands(obj.read()).encode())

    def error411(self):

        self.send_response(411, 'Length Required')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def found200(self):

        self.send_response(200, 'OK')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def handle(self):

        global request_count

        request_count += 1

        try:

            self.close_connection = True

            self.handle_one_request()
            while not self.close_connection:
                self.handle_one_request()

        except BrokenPipeError:

            self.imprint('Error de tuberia. El cliente puede estár conectandose y desconectandose para lograr que el servidor obtenga una anomalía', COM)

            self.do_AUTHHEAD()

        except ConnectionResetError as Except:

            self.imprint('Error por parte del cliente u ocurrio un error por no seguir el protocolo especifico. Excepción: "%s"' % (Except), WAR)

            self.do_AUTHHEAD()

        except Exception as Except:

            self.imprint('Ocurrio una excepción desconocida: "{}". Sí la culpa fue por un error de código, favor de notificar al administrador del proyecto.'.format(Except), COM)

            self.error500()

    def do_GET(self):

        global request_count_safe

        request_count_safe['GET'] += 1

        if (self.eject() == True): return

        # Si tratan de hacer un ataque de fuerza bruta para averiguar
        # las rutas de los directorios/archivos siempre dará un error 404

        if not (urlparse(self.path).path == '/'):

            self.error404()

            self.imprint('Está accediendo a una ruta "desconocida"', WAR)

        else:

            if (self.headers['Authorization'] == None) or (str(self.headers['Authorization'])[:5] != 'Basic'):

                self.do_AUTHHEAD()

            else:

                credentials = "%s:%s" % (false_username, false_passphrase)
                
                try:
                
                    credentials_cmp = b64decode(self.headers['Authorization'][6:]).decode()

                except:

                    self.imprint('¡Error descodificando las credenciales!', WAR)
                    self.do_AUTHHEAD()

                else:

                    self.imprint('Credenciales: {} == {}'.format(credentials, credentials_cmp), PER)

                    if (self.headers['Authorization'] == "Basic %s" % (b64encode(credentials.encode()).decode())):

                        self.found200()
                        self.imprint('Accedió a el panel de control (Web) de distracción', INF)
                        self.imprint('Abriendo plantilla de distracción', INF)
                        with open(TEMPLATE_CREDENTIALS, 'rb') as templates_credentials_obj:
                            self.wfile.write(templates_credentials_obj.read())
                        self.imprint('Se abrio la plantilla ...', INF)

                    else:

                        self.imprint('¡Ingreso incorrectamente las credenciales falsas!', WAR)
                        # Podría colocar un error403, pero así se distrae un poco más 3:)
                        self.do_AUTHHEAD()

    def do_POST(self):

        global request_count_safe

        share = False
        request_count_safe['POST'] += 1

        if (self.eject() == True): return

        content_length = self.headers['Content-Length']

        if (content_length == None):

            self.do_AUTHHEAD()
            return

        content_length = int(content_length)

        if (content_length <= 0):

            self.do_AUTHHEAD()
            return
        
        post_data = self.rfile.read(content_length)

        if (len(post_data) <= 0):

            self.do_AUTHHEAD()
            return

        try:

            _extract_post_data = extract_http_post_data.extract(post_data)

        except Exception as Except:

            _extract_post_data = False

        else:

            rusername = _extract_post_data.get('username')
            rpassword = _extract_post_data.get('passphrase')
            data_ = _extract_post_data.get('data')
            runiqkey = _extract_post_data.get('uniqkey')
            security_chars = _extract_post_data.get('chars')
            security_number = _extract_post_data.get('security_number')
            security_decrement_number = _extract_post_data.get('decrement_number')
            security_iterations = _extract_post_data.get('iterations')
            reply = _extract_post_data.get('reply')

            if (None in [rusername, rpassword, data_, runiqkey, security_chars, security_number, security_decrement_number, security_iterations]):

                _extract_post_data = False
                evalue_exp = None

            else:

                _decipher = lambda dat: hibrid.decrypt(dat, private_key)

                try:

                    rusername = _decipher(rusername)
                    rpassword = _decipher(rpassword)
                    data_ = _decipher(data_)
                    runiqkey = _decipher(runiqkey)
                    security_chars = _decipher(security_chars)
                    security_number = _decipher(security_number)
                    security_decrement_number = _decipher(security_decrement_number)
                    security_iterations = _decipher(security_iterations)
                    reply = _decipher(reply)

                except:

                    self.imprint('No se pudo desencriptar los datos por parámetros ...', WAR)

                    _extract_post_data = False

                else:

                    evalue_exp = [True, True, True, True, False, True, True, True, True]

        if (_extract_post_data == False):

            try:

                data = hibrid.decrypt(post_data, private_key)

            except Exception as Except:

                self.imprint('Error desencriptando datos. Intentando con el cifrado simetrico ...', WAR)

                try:

                    data = simplycrypt.decrypt(token, post_data)

                    if (data == None):

                        raise

                except Exception as Except:

                    self.imprint('No se desencriptaron los datos ni con el cifrado simetrico ...', COM)
                    self.do_AUTHHEAD()
                    return

                else:

                    self.imprint('Los datos fueron desencriptados, por lo tanto, se usarán en el acceso público ...', INF)
                    share = True
                    evalue_exp = None

            else:

                # Credentials

                rusername = data.get('username')
                rpassword = data.get('passphrase')
                data_ = data.get('data')
                bot_id = data.get('id')
                runiqkey = data.get('uniqkey')
                security_chars = data.get('chars')
                security_number = data.get('security_number')
                security_decrement_number = data.get('decrement_number')
                security_iterations = data.get('iterations')
                reply = data.get('reply')

                # Evaluamos

                evalue_exp = list(map(evalue, [rusername, rpassword, runiqkey, data_, bot_id, security_chars, security_number, security_decrement_number, security_iterations]))

        if not (urlparse(self.path).path == '/' + RPATH): 

            if (evalue_exp == [False, True, False, True, True, True, True, True, True]):

                if (check_credentials.check(rpassword, bot_id, logger, self.client_address, max_retry, retry_seconds, denied_method, resolve_dns, iterations=security_iterations, chars=security_chars, decrement_number=security_decrement_number, security_number=security_number)):

                    self.found200()

                    bot_information = wrap.read(bot_id, separate=True)
                    _username = bot_information['username']
                    command = hibrid.encrypt(execute_command.execute(data_, bot_id, log=debug.log(self.client_address, '%s:(%s)' % (_username, bot_id), logger, resolve_dns, resolve_port)), bot_information['keys'][0])

                    self.wfile.write(command)

                else:

                    self.error403()
                    self.imprint('Quiere acceder como un bot!', COM)

            else:

                self.do_AUTHHEAD()

        else:

            if (evalue_exp == [True, True, True, True, False, True, True, True, True]):

                self.imprint('Verificando si las credenciales de "%s" son correctas ...' % (rusername), WAR)

                if (check_administrators.check(username=rusername, passphrase=rpassword, uniqkey=runiqkey, recover=recover, log=debug.log(self.client_address, rusername, logger, resolve_dns), address=self.client_address, max_retry=max_retry, retry_seconds=retry_seconds, denied_method=denied_method, iterations=security_iterations, chars=security_chars, decrement_number=security_decrement_number, security_number=security_number)):

                    self.found200()

                    admin_information = wrap.read(rusername, agent=wrap.USE_ADMIN, separate=True)
                    self.imprint('(%s): Actualizada la clave única de "%s" ...' % (rusername, runiqkey), PER)
                    uniqkey_updated = generate_uniqkey.generate()
                    
                    if not (wrap.write(rusername, 'uniqkey', uniqkey_updated, agent=wrap.USE_ADMIN, separate=True) == True):
                    
                        self.error500()

                        log.logger('¡No se pudo actualizar la clave única!', debug.COM)

                        return

                    self.imprint('(%s): ... A: "%s"' % (rusername, uniqkey_updated), PER)
                    command = execute_command_to_admin.execute(data_, rusername, debug.log(self.client_address, rusername, logger, resolve_dns), evalue(reply))

                    if (command == False):

                        self.imprint('Ejecuto un comando erroneo', COM)

                        command = hibrid.encrypt((False, None, uniqkey_updated), admin_information['keys'][0])

                        self.wfile.write(command)

                        return

                    command = hibrid.encrypt((True, command, uniqkey_updated), admin_information['keys'][0])

                    self.wfile.write(command)

                else:

                    self.error403()
                    self.imprint('Ingreso credenciales incorrectas!', WAR)

            elif (share == True):

                self.found200()
                command = execute_public_command.execute(data, debug.log(self.client_address, 'Public', logger, resolve_dns))

                if (command == False):

                    self.imprint('Ejecuto un comando erroneo o hubo un error en la entrada de datos ...', COM)

                self.wfile.write(simplycrypt.encrypt(token, command))

            else:

                self.error511()

    def do_HEAD(self):

        request_count_safe['HEAD'] += 1

        if (self.eject() == True): return

        if not (urlparse(self.path).path == '/'):

            self.error404()

        else:

            self.found200()

    def do_AUTHHEAD(self):

        request_count_safe['AUTH'] += 1

        self.send_response(401, 'Unauthorized')
        self.send_header('Content-Type', 'text/html')
        self.send_header('WWW-Authenticate', 'Basic realm=\"%s\"' % (realm))
        self.end_headers()

        self.imprint('Trata de ingresar en el panel de control (Web) falso', INF)
    
    def log_error(self, *args):

        code = int(args[1])

        if (code == 400):

            self.error400()

        return

    def log_message(self, *args):

        method = args[1]
        response = args[2]
        address = self.client_address
        
        return_log.imprint(debug.log(address=self.client_address, log=logger, rdns=resolve_dns, rport=resolve_port), method, response)

try:

    httpd = ThreadingHTTPServer((LHOST, LPORT), handler)

except OSError:

    logger.log('La dirección proporcionada ya está en uso!', WAR)

else:

    try:
    
        httpd.socket = ssl.wrap_socket(httpd.socket, certfile=global_conf.ssl['cert'], keyfile=global_conf.ssl['key'], server_side=True)

    except ssl.SSLError as Except:

        logger.log('Ocurrió una Excepción con el certificado/clave. Excepción: "{}"'.format(Except), debug.COM)

        sys.exit(1)

    except OSError:

        logger.log('Error ingresando la frase de contraseña del certificado/clave.', debug.COM)
        
        sys.exit(1)

    except (FileNotFoundError, ValueError):

        logger.log('No se encontraron los requerimientos necesarios para usar el protocolo de forma (más) segura. Usando HTTP ...', WAR)
        
        proto = 'http'

    else:
        
        logger.log('Usando CERT:("%s") y KEY:("%s") para usar el protocolo HTTPS ...' % (global_conf.ssl['cert'], global_conf.ssl['key']), PER)

        proto = 'https'

    logger.log('Escuchando en :: %s://%s:%d/%s' % (proto, LHOST, LPORT, RPATH), PER)

    try:

        httpd.serve_forever()

    except KeyboardInterrupt:

        pass

    httpd.shutdown()

if (get_os_name == 'posix'):

    try:

        subprocess.call(['reset', '-w'])

    except:

        pass

logger.log('Saliendo ...', debug.INF)
