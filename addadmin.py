#!/usr/bin/env python3

while(1):

    try:

        from utils.sys_utils import no_terminate

    except KeyboardInterrupt:

        continue

    else:

        break

import sys
import re
import os

from utils.Ciphers import generate_uniqkey
from utils.sys_utils import pos_convert

try:
    from utils.Wrappers import wrap
except Exception as Except:
    print(str(Except))
    sys.exit(1)

from utils.Shows import show_user_admins
from utils.Checks import rsa_password_check
from utils.Ciphers import decrypt_rsa_private_key
from utils.Shows import show_spec_values
from utils.sys_utils import enum_bots

from modules.UI import argprogrammer
from modules.Ciphers import db_hash
from modules.Ciphers import POO_RSA
from modules.UI import iInput

from conf import global_conf

cuenta = 1

rsa = POO_RSA.main()

# Default values

_default_iter = global_conf.hashing['iterations']
_default_security_number = global_conf.hashing['security_number']
_default_decrement_number = global_conf.hashing['decrement_number']
_default_chars = global_conf.hashing['chars']
_default_bit_size = global_conf.rsa['bit_size']
_default_priv = 'ALL'
_default_max_bot = 0

_default_parameter = 'Parámetros Opcionales'
_login_group = 'Inicio de Sesión'
_security_group = 'Seguridad'
_profile_group = 'Perfil'

parser = argprogrammer.Parser()

parser.set_head('''
       Syndicate Project - Escribir o remplazar credenciales de un Admininistrador
       -----------------   -------------------------------------------------------''')

for _ in [dict(param_name=['-h', '--help'], key='help', help='Mostrar la ayuda que estás viendo', group=_default_parameter),
        dict(param_name=['-no-confirm'], key='no_confirm', help='No mostrar una confirmación antes de agregar el administrador', type=bool, action=False, group=_default_parameter),
        dict(param_name=['-limit'], key='limit', help='El rango para delimitar la lista de administradores. Usé "n-n".', type=range, group=_default_parameter),
        dict(param_name=['-al', '--access-limit'], key='access_limit', help='El rango para delimitar la lista de accesos. Usé la misma sintaxis que \'-limit\'', type=range, group=_default_parameter),
        dict(param_name=['-u', '--username'], key='username', help='Nombre de usuario', group=_login_group),
        dict(param_name=['-p', '--passphrase'], key='passphrase', help='Frase de contraseña', group=_login_group),
        dict(param_name=['-P', '--rsa-password'], key='rsa_password', help='La contraseña para cifrar con *3DES* la clave privada', group=_security_group),
        dict(param_name=['-sn', '--security-number'], key='security_number', help='El número de seguridad. Pre-determinado: "%d"' % (_default_security_number), type=int, group=_security_group, default=_default_security_number),
        dict(param_name=['-i', '--iterations'], key='iterations', help='Las repiticiones del proceso Hash. Pre-determinado: "%d"' % (_default_iter), type=int, group=_security_group, default=_default_iter),
        dict(param_name=['-c', '--security-chars'], key='security_chars', help='Los caracteres que se agregán antes del proceso Hash. Pre-determinado: "%s"' % (_default_chars), group=_security_group, default=_default_chars),
        dict(param_name=['-d', '--decrement-number'], key='decrement_number', help='El número de disminución. Pre-determinado: "%d"' % (_default_decrement_number), type=int, group=_security_group, default=_default_decrement_number),
        dict(param_name=['-privileges'], key='privileges', help='Asigna privilegios al administrador. Pre-determinado: "%s"' % (_default_priv), type=list, group=_profile_group, default=_default_priv),
        dict(param_name=['-max-bot'], key='max_bot', help='El limit de bot\'s que puede tener el usuario. \'0\' para tener bot\'s infinitos. Pre-determinado: "%d"' % (_default_max_bot), type=int, group=_profile_group, default=_default_max_bot),
        dict(param_name=['-bit-size'], key='bit_size', help='El tamaño en *bits* del par de claves. Pre-determinado: "%d"' % (_default_bit_size), type=int, group=_profile_group, default=_default_bit_size),
        dict(param_name=['-del-admin'], key='del_admin', help='Borrar un administrador', group=_default_parameter),
        dict(param_name=['-show'], key='show', help='Mostrar los usuarios registrados', type=bool, action=True, group=_default_parameter),
        dict(param_name=['-option'], key='option', help='Cuando "-show" y "-option" están activos muestra un valor con una clave especifica en vez de mostrar todos los valores. Las claves permitidas son: "%s"' % (', '.join(global_conf.keys_admin)), uniqval=global_conf.keys_admin, group=_default_parameter),
        dict(param_name=['-r', '--root'], key='root', help='Volver root al usuario que se creará', type=bool, action=True, group=_profile_group)]:

    parser.add(**_)

args = parser.parse_args()

username = args.username
passphrase = args.passphrase
rsa_password = args.rsa_password
iterations = pos_convert.convert(args.iterations)
security_number = pos_convert.convert(args.security_number)
security_chars = args.security_chars
decrement_number = pos_convert.convert(args.decrement_number)
privileges = args.privileges
max_bot = pos_convert.convert(args.max_bot)
bit_size = pos_convert.convert(args.bit_size)
show = args.show
del_admin = args.del_admin
no_confirm = args.no_confirm
root = args.root
option = args.option
access_limit = args.access_limit
limit = args.limit

if (del_admin):

    _file_to_remove = '{}/{}.db'.format(wrap.getDB(wrap.USE_ADMIN), del_admin)

    if (os.path.isfile(_file_to_remove)):

        try:

            os.remove(_file_to_remove)

        except Exception as Except:

            print('Error borrando el almacén. Excepción: "{}"'.format(Except))
            sys.exit(1)

        else:

            print('{}, Fue eliminado con éxito'.format(del_admin))
            sys.exit(0)

    else:

        print('El administrador no se puede borrar, porque no existe ...')
        sys.exit(1)

if (show == True):

    admins = show_user_admins.show()
    admins = admins if (limit == None) else admins[limit[0]:limit[1]]
    credentials_list = [x for x in [wrap.getall(wrap.USE_ADMIN, username=x, separate=True) for x in admins] if not (x == False)]

    if (credentials_list == []):

        print('¡No hay información acerca de los administradores!')

    else:

        for credentials in credentials_list:

            if not (rsa_password == None):

                _evalue_credentials = rsa_password_check.check(rsa_password, admins)

            else:

                _evalue_credentials = None
                
            if not (option == None):

                for _ in admins:

                    show_spec_values.show(_, option, wrap.USE_ADMIN, _evalue_credentials)

                sys.exit(0)

            for key, value in credentials.items():

                tmp_bots = enum_bots.enum(key, False)

                if (tmp_bots == -1):

                    print('Ocurrio un error, parece que el administrador "{}" no existe o no se pudo leer el almacén...'.format(key))
                    continue

                if (tmp_bots == []):

                    _formated_bots = 'No está encargado de ningún bot ...'

                else:

                    _formated_bots = '%s (%s)' % (tmp_bots[:1][0][0], tmp_bots[:1][0][1])

                    for _ in tmp_bots[1:]:

                        _formated_bots += ', %s (%s)' % (_[0], _[1])

                tmp_lastlogin = ('\n\t\t\t\t'+(' '*6)).join(value['lastLogin'][access_limit[0]:access_limit[1]] if not (access_limit == None) else value['lastLogin']).replace('&', ' ~ ')
                tmp_lastlogin = tmp_lastlogin if not (tmp_lastlogin == '') else 'No hay intentos de inicio de sesión'
                
                tmp_max_bot = int(value['max_bot'])
                tmp_max_bot = tmp_max_bot if (tmp_max_bot > 0) else '0 (Infinito)'
                
                tmp_lastuniqkey = value['lastUniqkey']
                tmp_lastuniqkey = tmp_lastuniqkey if not (tmp_lastuniqkey == None) else 'Aún no se almacenan viejas claves únicas'

                tmp_privileges = ', '.join(value['privileges'])
                tmp_privileges = tmp_privileges if not (tmp_privileges == '') else 'No tiene privilegios'

                tmp_priv_key = value['keys'][1]
                
                if not (rsa_password == None):

                    try:

                        tmp_priv_key = decrypt_rsa_private_key.decrypt(tmp_priv_key, _evalue_credentials[key], key)

                    except KeyError:

                        print('\033[1;37mNo está definida la contraseña de la clave privada de\033[0m "\033[1;4;37m%s\033[0m"' % (key) + '\n')

                print('\033[1;37m%d\033[34m)\033[0m - \033[1;37m\033[4m%s\033[0m:' % (cuenta, key if not (value['root'] == True) else '\033[0m\033[1m\033[36m*\033[0m\033[1m\033[37m\033[4m%s\033[0m\033[1m\033[36m*\033[0m' % (key)) + '\n')
                print('\t' + '- \033[1;34mContraseña\033[0m: \033[37m%s\033[0m' % (value['passphrase']))
                print('\t' + '- \033[1;34mMax. de bot\'s\033[0m: \033[37m%s\033[0m' % (tmp_max_bot))
                print('\t' + '- \033[1;34mEncargado de\033[0m: \033[37m%s\033[0m' % (_formated_bots))
                print('\t' + '- \033[1;34mPrivilegios\033[0m: \033[37m%s\033[0m' % (tmp_privileges))
                print('\t' + '- \033[1;34mClave única\033[0m: \033[37m%s\033[0m' % (value['uniqkey']))
                print('\t' + '- \033[1;34mUltima Clave única usada\033[0m: \033[37m%s\033[0m' % (tmp_lastuniqkey))
                print('\t' + '- \033[1;34mFechas de inicio de sesión\033[0m: \033[37m%s\033[0m' % (tmp_lastlogin))
                print('\t' + '- \033[1;34mClave Pública\033[0m: \n\n\t\033[37m%s\033[0m\n' % (value['keys'][0]))
                print('\t' + '- \033[1;34mClave Privada\033[0m: \n\n\t\033[37m%s\033[0m' % (tmp_priv_key))
                print('\n')
                print('\033[1;37m+\033[0m \033[1;31mSeguridad\033[0m \033[1;37m+\033[0m')
                print('\033[1;37m- --------- -\033[0m')
                print('\n')
                print('\t' + '- \033[1;34mIteraciones\033[0m: \033[37m%s\033[0m' % (value['iterations']))
                print('\t' + '- \033[1;34mNúmero de seguridad\033[0m: \033[37m%s\033[0m' % (value['securityNumber']))
                print('\t' + '- \033[1;34mNúmero de disminución\033[0m: \033[37m%s\033[0m' % (value['decrementNumber']))
                print('\t' + '- \033[1;34mCaracteres de seguridad\033[0m: \033[37m%s\033[0m' % (value['security_chars']))
                print('\n')

                cuenta += 1

else:

    if (username == None) or (passphrase == None) or (rsa_password == None):

        print('No has definido el usuario, frase de contraseña o la contraseña de la clave privada')
        sys.exit(1) 

    if (no_confirm):

        print('-*- ¿Es correcta la siguiente información? -*-', end='')
        print('\n')
        print('Nombre de usuario       ::   %s' % (username))
        print('Frase de contraseña     ::   %s' % (passphrase))
        print('Contraseña RSA          ::   %s' % (rsa_password))
        print('Iteraciones             ::   %d' % (iterations))
        print('Número de seguridad     ::   %d' % (security_number))
        print('Número de disminución   ::   %d' % (decrement_number))
        print('Caracteres de seguridad ::   %s' % (security_chars))
        print('Privilegios             ::   %s' % (', '.join(privileges)))
        print('Max. de bot\'s           ::   %s' % (max_bot if (max_bot > 0) else '0 (infinito)'))
        print('Tamaño de la clave      ::   %d' % (bit_size))
        print('¿Root?                  ::   %d' % (1 if (root == True) else 0))

        while (True):

            try:

                debug = iInput.iInput(char_limit=1, indicator='-> ')

            except Exception as Except:

                print('Excepción desconocida: "%s"' % (Except))

            if not (debug):

                continue

            if (re.match('^[y|s|1]{1}', debug[0].lower())):

                break

            elif (re.match('^[n|0]{1}', debug[0].lower())):

                sys.exit(0)

            else:

                print('Error, ingrese los siguientes valores para afirmar -> "y/Y, s/S, 1" y para negar -> "0, n/N"') 

    print('Creando ...')

    print('Deberias apostar en una competencia de caracoles mientras se generan las claves ...')

    rsa.generate(bit_size, rsa_password)

    print('Generado! ...')

    print('Verificando privilegios ...')

    if ('ALL' in privileges) and (len(privileges) > 1):

        print('No puedes agregar más privilegios si ya tienes todos')

        sys.exit(1)

    for _ in privileges:

        if not (_ in global_conf.privileges):

            print('Privilegio invalido: "%s"' % (_))

            sys.exit(1)

    if (show_user_admins.show() == []):

        print('Es la primera vez que se creará un administrador ... Convirtiéndolo en *root* ...')
        root = True
    
    print('Configurando valores ...')

    wrap.add(username, {
                            'root':root,
                            'passphrase':db_hash.hash(passphrase, iterations, security_chars, security_number, decrement_number),
                            'uniqkey':generate_uniqkey.generate(),
                            'lastLogin':[],
                            'lastUniqkey':None,
                            'privileges':privileges,
                            'keys':rsa.export(),
                            'max_bot':max_bot,
                            'iterations':iterations,
                            'securityNumber':security_number,
                            'security_chars':security_chars,
                            'decrementNumber':decrement_number
                            
                        }, agent=wrap.USE_ADMIN, username=username, separate=True)

    print('Configurado.')
