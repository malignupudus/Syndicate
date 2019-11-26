#!/usr/bin/env python3

while(1):

    try:

        from utils.sys_utils import no_terminate

    except KeyboardInterrupt:

        continue

    else:

        break

import sys
import argparse
import shutil
from uuid import uuid4
from os.path import dirname, isdir, splitext, isfile
from os import getcwd, remove

from modules.Ciphers import POO_RSA
from modules.Ciphers import db_hash
from modules.UI import argprogrammer

from utils.sys_utils import create_folder
from utils.sys_utils import pos_convert
from utils.Ciphers import generate_uniqkey
try:
    from utils.Wrappers import wrap
except Exception as Except:
    print(str(Except))
    sys.exit(1)
from utils.sys_utils import enum_bots
from utils.Checks import rsa_password_check
from utils.Ciphers import decrypt_rsa_private_key
from utils.Shows import show_spec_values
from utils.Shows import show_user_admins
from utils.Shows import show_user_rooks
from utils.Extracts import real_extract_root_administrators
from utils.sys_utils import uniqdata

# Configuration

from conf import global_conf

rsa = POO_RSA.main()
root = global_conf.databases['database']
profile = '%s/%s' % (root, global_conf.databases['profiles'])
cuenta = 0

# Default values

_default_iter = global_conf.hashing['iterations']
_default_security_number = global_conf.hashing['security_number']
_default_decrement_number = global_conf.hashing['decrement_number']
_default_chars = global_conf.hashing['chars']
_default_bot_id = 'RANDOM'
_default_bit_size = global_conf.rsa['bit_size']

admin_id_list = show_user_admins.show()
bot_id_list = show_user_rooks.show()

if (admin_id_list == []):
        
    print('No hay administradores actuales para seguir con las operaciones ...')
    sys.exit(1)

_parser = argprogrammer.Parser()
_parser.set_head('''
       Syndicate Project - Escribir o remplazar credenciales de un Bot
       -----------------   -------------------------------------------''')

_default_parameter = 'Parámetros Opcionales'
_login_group = 'Inicio de Sesión'
_security_group = 'Seguridad'
_profile_group = 'Perfil'

for _ in (dict(param_name=['-h', '--help'], key='help', help='Mostrar la ayuda que estás viendo', group=_default_parameter),
        dict(param_name=['-u', '--user'], key='user', help='Nombre de Usuario', group=_login_group),
        dict(param_name=['-p', '--passphrase'], key='passphrase', help='Frase de Contraseña', group=_login_group),
        dict(param_name=['-P', '--rsa-password'], key='rsa_password', help='La Contraseña para Cifrar con *3DES* la clave privada', group=_security_group),
        dict(param_name=['-a', '--admin'], key='admin', help='El Administrador del Bot', type=list, group=_profile_group),
        dict(param_name=['-id', '--bot-id'], key='bot_id', help='El Identificador del Bot. Pre-determinado: "%s"' % (_default_bot_id), group=_login_group, default=_default_bot_id),
        dict(param_name=['-sn', '--security-number'], key='security_number', help='Número de seguridad. Pre-determinado: "%d"' % (_default_security_number), type=int, group=_security_group, default=_default_security_number),
        dict(param_name=['-i', '--iterations'], key='iterations', help='Las repeticiones de operación Hash. Pre-determinado: "%d"' % (_default_iter), type=int, group=_security_group, default=_default_iter),
        dict(param_name=['-c', '--security-chars'], key='security_chars', help='Agrega caracteres antes de hacer el proceso Hash. Pre-determinado: "%s"' % (_default_chars), group=_security_group, default=_default_chars),
        dict(param_name=['-d', '--decrement-number'], key='decrement_number', help='El número de disminución del número de seguridad durante las iteracions. Pre-determinado: "%d"' % (_default_decrement_number), group=_security_group, default=_default_decrement_number, type=int),
        dict(param_name=['-show'], key='show', help='Mostrar los Bot\'s registrados', group=_default_parameter, action=True, type=bool),
        dict(param_name=['-limit'], key='limit', help='El rango para delimitar la lista de bot\'s. Usé "n-n".', type=range, group=_default_parameter),
        dict(param_name=['-option'], key='option', help='Cuando "-show" y "-option" están activos muestra un valor con una clave especifica en vez de mostrar todos los valores. Las claves permitidas son: "%s"' % (', '.join(global_conf.keys_bot)), uniqval=global_conf.keys_bot, group=_default_parameter),
        dict(param_name=['-del-bot'], key='del_bot', help='Borrar un Bot', group=_default_parameter),
        dict(param_name=['-bit-size'], key='bit_size', help='El tamaño en Bit\'s del par de claves. Pre-determinado: "%d"' % (_default_bit_size), group=_profile_group, default=_default_bit_size, type=int)):

    _parser.add(**_)

args = _parser.parse_args()

user = args.user
passphrase = args.passphrase
rsa_password = args.rsa_password
admin = args.admin
bot_id = args.bot_id
show = args.show
bit_size = pos_convert.convert(args.bit_size)
del_bot = args.del_bot
iterations = pos_convert.convert(args.iterations)
security_number = pos_convert.convert(args.security_number)
security_chars = args.security_chars
decrement_number = pos_convert.convert(args.decrement_number)
option = args.option
limit = args.limit

if (del_bot):

    profile_name = wrap.read(del_bot, 'profile', separate=True)
    _file_to_remove = '{}/{}.db'.format(wrap.getDB(wrap.USE_BOT), del_bot)

    if not (profile_name == False):

        print("Borrando directorio de perfil ...")

        try:

            shutil.rmtree(profile_name)
            print('Borrado, directorio de perfil: "%s"' % (profile_name))

        except FileNotFoundError as Except:

            print("Error borrando el directorio de perfil. Excepción: \"%s\"" % (Except))

    else:

        print('No se pudo obtener el directorio de perfil')

    print('Borrando almacén ...')

    if (isfile(_file_to_remove)):

        try:

            remove(_file_to_remove)

        except Exception as Except:

            print('Error borrando el almacén. Excepción "{}"'.format(Except))
            sys.exit(1)

        else:

            print('Borrado: "%s"' % (del_bot))
            sys.exit(0)

    else:

        print('El almacén del rook no se puede borrar porque no existe ...')
        sys.exit(1)

if (show == True):

    if (len(bot_id_list) == 0):

        print('No se han registrado credenciales para los bot\'s')
        sys.exit(1)

    bot_id_list = bot_id_list if (limit == None) else bot_id_list[limit[0]:limit[1]]
    credentials_list = [wrap.getall(agent=wrap.USE_BOT, username=x, separate=True) for x in bot_id_list]

    for credentials in credentials_list:

        if not (rsa_password == None):

            _evalue_credentials = rsa_password_check.check(rsa_password, bot_id_list)

        else:

            _evalue_credentials = None

        if not (option == None):

            for _ in bot_id_list:

                show_spec_values.show(_, option, wrap.USE_BOT, _evalue_credentials)

            sys.exit(0)
        
        for key, value in credentials.items():

            _servers = []

            for _ in value['servers']:

                _servers.append(_[0])

            tmp_admins = ', '.join(value['admins'])
            tmp_admins = tmp_admins if not (tmp_admins == '') else 'No hay administradores encargados'

            tmp_profile = value['profile']
            tmp_profile = tmp_profile if not (tmp_profile == None) else 'No hay directorio de perfil para este bot'

            secundary_servers = ', '.join(_servers)
            secundary_servers = secundary_servers if not (secundary_servers == '') else 'No hay servidores secundarios agregados'

            peers = wrap.read(key, 'peers', agent=wrap.USE_PEER)
            peers_format = [(x['url'], x['hash']) for x in peers] if not (peers == False) else False

            if not (peers == False):

                peers_formated = '%s (%s)' % (peers_format[0][0], peers_format[0][1])

                for url, hash_ in peers_format[1:]:

                    peers_formated += ', %s (%s)' % (url, hash_)

            else:

                peers_formated = 'No hay puntos disponibles para este bot'

            tmp_priv_key = value['keys'][1]

            if not (rsa_password == None):

                try:

                    tmp_priv_key = decrypt_rsa_private_key.decrypt(tmp_priv_key, _evalue_credentials[key], key)

                except KeyError:

                    print('\033[1;37mNo está definida la contraseña de la clave privada de\033[0m "\033[1;4;37m%s\033[0m"' % (key) + '\n')

            cuenta += 1

            key = '\033[1;4;37m%s\033[0m' % (key)

            try: 

                print('[\033[1;31m%s\033[0m] - \033[4m\033[1;34mID\033[0m: %s\n' % (cuenta, key))
                
                print('\t\033[1;34mNombre de usuario\033[0m: \033[37m%s\033[0m' % (value['username']))
                print('\t\033[1;34mContraseña\033[0m: \033[37m%s\033[0m' % (value['passphrase']))
                print('\t\033[1;34mDirectorio de perfil\033[0m: \033[37m%s\033[0m' % (tmp_profile))
                print('\t\033[1;34mAdministradores\033[0m: \033[37m%s\033[0m' % (tmp_admins))
                print('\t\033[1;34mServidores secundarios\033[0m: \033[37m%s\033[0m' % (secundary_servers))
                print('\t\033[1;34mPuntos de la red\033[0m: \033[37m%s\033[0m' % (peers_formated))
                print('\t\033[1;34mClave Pública\033[0m: \n\n\t\033[37m%s\033[0m\n' % (value['keys'][0]))
                print('\t\033[1;34mClave Privada\033[0m: \n\n\t\033[37m%s\033[0m' % (tmp_priv_key))
                print('\n')
                print('\033[1;37m+ \033[1;31mSeguridad \033[1;37m+\033[0m')
                print('\033[1;37m- --------- -\033[0m')
                print('\n')
                print('\t' + '- \033[1;34mIteraciones\033[0m: \033[37m%s\033[0m' % (value['iterations']))
                print('\t' + '- \033[1;34mNúmero de seguridad\033[0m: \033[37m%s\033[0m' % (value['securityNumber']))
                print('\t' + '- \033[1;34mNúmero de disminución\033[0m: \033[37m%s\033[0m' % (value['decrementNumber']))
                print('\t' + '- \033[1;34mCaracteres de seguridad\033[0m: \033[37m%s\033[0m' % (value['security_chars']))
                print('\n')


            except Exception as Except:

                print('Ocurrio una Excepción, tras leer a: "%s". Excepción: "%s"' % (key, Except))

    sys.exit(0)

if (user == None) or (passphrase == None) or (admin == None) or (rsa_password == None):

    print('No has definido el usuario, la frase de contraseña, el administrador o la contraseña de la clave privada')
    sys.exit(1)

print('Verificando existencia y limites del administrador ...') if (len(admin) == 1) else print('Verificando existencia y limites de los administradores...')

for _ in admin:

    _ = str(_)

    max_bot = wrap.read(_, 'max_bot', agent=wrap.USE_ADMIN, separate=True)

    if (str(max_bot) == 'False'):

        print('Ocurrio un error con el siguiente administrador: "%s", probablemente no existe!' % (_))
        sys.exit(1)

    if (max_bot > 0):

        enums = enum_bots.enum(_)

        if not (enums == -1):

            if (enums >= max_bot):

                print('Limite de creación de bot\'s superados por parte de "%s" ...' % (_))
                sys.exit(1)

        else:

            print('Ocurrio un error analizando el siguiente administrador: "%s"' % (_))
            sys.exit(1)

if (bot_id.lower() == 'random'):

    bot_id = generate_uniqkey.generate()

profile_dirname = '%s/%s' % (profile, bot_id)

if (bot_id in bot_id_list):

    print('Remplazando: %s' % (bot_id))

else:

    print('Creando: %s' % (bot_id))

print('La generación de claves puede tardar un siglo a un milenio, sea paciente ...')

rsa.generate(bit_size, rsa_password)

print('Generado! ...')

print('Creando carpeta de perfil: %s' % (profile_dirname))

create_folder.create(profile_dirname)

print('Creado.')

# Formato: Nombre de usuario, Frase de contraseña, Directorio, Administradora/or/es/as, Claves, Comandos, Datos

wrap.add(bot_id, {
    
                    'username':user,
                    'passphrase':db_hash.hash(passphrase, iterations, security_chars, security_number, decrement_number),
                    'profile':profile_dirname,
                    'admins':uniqdata.uniqdata(admin+real_extract_root_administrators.extract()),
                    'keys':rsa.export(),
                    'commands':[],
                    'data':[],
                    'servers':[],
                    'Queue':[],
                    'iterations':iterations,
                    'securityNumber':security_number,
                    'security_chars':security_chars,
                    'decrementNumber':decrement_number
                    
                }, agent=wrap.USE_BOT, username=bot_id, separate=True)

print('Creado: %s' % (bot_id))
