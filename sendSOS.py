#!/usr/bin/env python3

while(1):

    try:

        from utils.sys_utils import no_terminate

    except KeyboardInterrupt:

        continue

    else:

        break

import requests
import sys
import os

from utils.Checks import check_headers
from utils.Checks import check_url
from utils.Ciphers import simplycrypt

from modules.UI import iInput
from modules.UI import argprogrammer

from conf import global_conf

slack = {}
slack['files'] = []
verbose = lambda string: print(f'[SOS] - {string}')

required_group = 'Parámetros requeridos'
optionals = 'Opcionales'

parser = argprogrammer.Parser()

parser.set_head('''
       Syndicate Project - Enviar mensajes a un Evie
       -----------------   -------------------------''')

parser.add(['-h', '--help'], 'help', 'Mostrar la ayuda qué estás viendo', group=optionals)
parser.add(['-u', '--url'], 'url', 'La dirección del servidor', require=True, group=required_group)
parser.add(['-t', '--token'], 'token', 'Token de acceso público', require=True, group=required_group)

parser.add(['-n', '--nickname'], 'nickname', 'El apodo que quieres tener', default='Anonymous', group=optionals)
parser.add(['-s', '--subject'], 'subject', 'El asunto del mensaje', default='Sin Asunto', group=optionals)
parser.add(['-m', '--message'], 'message', 'El cuerpo del mensaje', require=True, group=required_group)
parser.add(['-f', '--file'], 'file', 'El archivo del mensaje. Sintaxis: <filename>:<path>', group=optionals)
parser.add(['-H', '--headers'], 'headers', 'Los encabezados a usar. Sintaxis: key=value&key2=value2', group=optionals, type=dict)

args = parser.parse_args()

url = args.url
token = args.token
nickname = args.nickname
subject = args.subject
message = args.message
files_ = args.file
headers = args.headers

try:

    check_headers.check(headers)

except Exception as Except:

    print('Ocurrio una excepción con los encabezados: {}'.format(Except))
    sys.exit(1)

if (check_url.check(url, None, False) == True):

    verbose(f'{url}, No es una URL válida; Recuerde definir el esquema, la dirección, el puerto y la ruta')
    sys.exit(1)

else:

    verbose(f'¡La url: "{url}" es válida para está operación!')

try:

    if not (files_ == None):

        for file_ in [x.strip() for x in files_.split(',')]:
        
            if not (file_ == None) and (file_.count(':') != 1):

                verbose('Sí desea agregar un archivo debe seguir la siguiente sintaxis: <filename>:<path>')
                sys.exit(1)

            elif not (file_ == None):

                (filename, path) = file_.split(':')

                verbose(f'Leyendo: {path} ...')

                if (os.path.isfile(path)):

                    try:

                        with open(path, 'rb') as _file_object:

                            slack['files'].append((filename, _file_object.read()))

                    except Exception as Except:

                        verbose('No se pudo leer el archivo "{}" porque ocurrio una excepción: {}'.format(filename, Except))

                    else:

                        verbose('El archivo se mandara como: "{}"'.format(filename))

                else:

                    verbose('¡El archivo "{}", no existe!'.format(filename))

    if (len(subject) > 98):

        verbose('¡El asunto supera el limite estandar: 98!')
        print('\n')
        verbose('Así es como se veria el asunto: {}'.format(subject[:98]))
        print('\n')
        verbose('¿Enviar igualmente? [0-1]')

        while (True):
            
            debug = iInput.iInput(char_limit=1, indicator='> ', datatype=int)

            if not (debug):

                continue

            if (debug == 1):

                break

            elif (debug == 0):

                print()
                sys.exit(0)

            else:

                verbose('¡Debe ingresar: 0 o 1!') 

    subject = subject[:98]
    formated = ''

    slack['nickname'] = nickname
    slack['subject'] = subject
    slack['message'] = message

    print('De: {}'.format(nickname))
    print('Asunto: {}'.format(subject))
    print('Mensaje:')
    
    for _ in message.splitlines():

        print('\t{}'.format(_))

    if (len(slack['files']) > 0):

        print('\n' + 'Incrustado: {}'.format(', '.join([x[0] for x in slack['files']])))

    print()

    debug = iInput.iInput(char_limit=1, indicator='¿Enviar? - [default:0]/1:', datatype=int)

    if not (debug) or (debug == 0):

        print()
        sys.exit(0)

    verbose('Enviando a: "{}"'.format(url))

    response = requests.post(url, data=simplycrypt.encrypt(token, {'token':token, 'command':('sendSOS', slack)}), headers=headers)

    status_code = response.status_code

    if (status_code == 200):

        response_decrypted = simplycrypt.decrypt(token, response.content)

        if (response_decrypted == True):

            verbose('¡Enviado!')

        else:

            verbose('¡Error enviando el mensaje!')

    elif (status_code == 411):

        verbose('Evie, no permitio qué accedas, debido a un error por tú parte')

    elif (status_code == 403):

        verbose('¡Acceso Denegado!')

    elif (status_code == 511):

        verbose('Ejecutaste un comando erroneo o ocurrio un error en Evie')

    elif (status_code == 500):

        verbose('¡Ocurrio un error en Evie!')

    else:

        verbose('%d, Es un código de estado desconocido ...' % (status_code))

except KeyboardInterrupt:

    sys.exit(0)

except Exception as Except:

    verbose('Ocurrio una excepción: "{}"'.format(Except))
