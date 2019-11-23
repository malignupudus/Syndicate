#!/usr/bin/env python3

import sys

from modules.Ciphers import db_hash
from modules.UI import argprogrammer

from utils.Wrappers import wrap
from utils.sys_utils import pos_convert
from utils.Shows import show_user_admins

from conf import global_conf

no_delete = ['username', 'passphrase', 'uniqkey', 'lastuniqkey', 'profile', 'keys', 'max_bot', 'root']

_passphrase_is = False

default_iter = global_conf.hashing['iterations']
default_security_number = global_conf.hashing['security_number']
default_decrement_number = global_conf.hashing['decrement_number']
default_chars = global_conf.hashing['chars']
default_limits = 1
default_agent = 'bot'

group_edit = 'Editar'
group_delete = 'Borrar'
group_security = 'Seguridad'
group_optionals = 'Opcionales'

parser = argprogrammer.Parser()

parser.set_head('''
       Syndicate Project - Editar datos del almacén de los bot\'s o administradores
       -----------------   -------------------------------------------------------''')

parser.add(['-h', '--help'], 'help', help='Mostrar la ayuda y sale', group=group_optionals)
parser.add(['-t', '--data-type'], 'data_type', help='El tipo de dato. Pre-determinado: "str"', default='str', group=group_optionals)

parser.add(['-a', '--agent'], 'agent', help='EL tipo de agente a utilizar. BOT:"En caso de editar el bot" y ADMIN:"En caso de editar el administrador"', default=default_agent, uniqval=['BOT', 'ADMIN'])

parser.add(['-sn', '--security-number'], 'security_number', help='El número de seguridad para aumentar la seguridad en el hash. Pre-determinado: "%s"' % (default_security_number), type=int, default=default_security_number, group=group_security)
parser.add(['-i', '--iterations'], 'iterations', help='Las repeticiones de operación hash. Pre-determinado: "%s"' % (default_iter), default=default_iter, type=int, group=group_security)
parser.add(['-c', '--security-chars'], 'security_chars', help='Agrega caracteres antes de hacer el proceso de hash. Pre-determinado: "%s"' % (default_chars), default=default_chars, group=group_security)
parser.add(['-d', '--decrement-number'], 'decrement_number', help='Número de disminución del número de seguridad durante las iteraciones. Pre-determinado: "%s"' % (default_decrement_number), default=default_decrement_number, type=int, group=group_security)

parser.add(['-id', '--identifier'], 'identifier', help='El identificador del usuario', require=True, type=str)
parser.add(['-k', '--key'], 'key', help='La clave a editar. Claves permitidas: "%s"' % (', '.join(global_conf.keys)), require=True, type=str, group=group_edit, uniqval=global_conf.keys)
parser.add(['-v', '--value'], 'value', help='El valor para la clave', require=True, group=group_edit)

parser.add(['-delete'], 'delete', help='Borrar en vez de agregar', type=bool, action=True, group=group_delete)
parser.add(['-limit'], 'limit', help='El limite de coincidencias en caso de ser un arreglo. Pre-determinado: "%s"' % (default_limits), type=int, default=default_limits, group=group_delete)

args = parser.parse_args()

agent = args.agent.lower()
identifier = args.identifier
key = args.key
value = args.value
delete = args.delete
limits = args.limit
iterations = pos_convert.convert(args.iterations)
security_number = pos_convert.convert(args.security_number)
security_chars = args.security_chars
decrement_number = pos_convert.convert(args.decrement_number)
data_type = args.data_type

wrapper_instance = wrap.read(identifier, key, separate=True) if (agent.lower() == 'bot') else wrap.read(identifier, key, agent=wrap.USE_ADMIN, separate=True)

if (data_type == 'int'):

    try:

        value = int(value)

    except ValueError:

        print('El valor no es númerico')
        sys.exit(1)

elif (data_type == 'bool'):

    if (value.lower() == 'false'):

        value = False

    else:

        value = True

elif (data_type == 'str'):

    pass

else:

    print('El tipo de dato aún no está disponible ...')
    sys.exit(1)

if (agent == 'bot'):

    wrapper_instance = wrap.read(identifier, key, separate=True)

elif (agent == 'admin'):

    wrapper_instance = wrap.read(identifier, key, agent=wrap.USE_ADMIN, separate=True)

else:

    print('No se reconocio al agente.')
    sys.exit(1)

if (delete == True):

    for _ in no_delete:

        if (_ == key.lower()):

            print('No está permitido la eliminación de "%s"' % (_))
            sys.exit(1)

if (wrapper_instance == False):
    
    print('Ocurrio un error, no se puede seguir operando.')
    sys.exit(1)

else:

    try:
    
        if (isinstance(wrapper_instance, list)) and (delete == True):

            limit = 0
            count_value = 0

            while not (limit >= limits):

                result = wrap.write(identifier, key, value, target=wrap.TARGET_DELETE, separate=True) if (agent == 'bot') else wrap.write(identifier, key, value, agent=wrap.USE_ADMIN, target=wrap.TARGET_DELETE, separate=True)

                if not (result == False):

                    count_value += 1

                else:

                    print('No se pudo eliminar: %s' % (value))

                limit += 1

            if not (count_value == 0):

                print('Eliminado: %s (%d)' % (value, count_value))

            else:

                print('No hubo valores eliminados ...')

        elif (delete == True) and not (isinstance(wrapper_instance, list)):

            result = wrap.write(identifier, key, None, separate=True) if (agent == 'bot') else wrap.write(identifier, key, None, agent=wrap.USE_ADMIN, separate=True)
            
            if (result == False):

                print('No se pudo eliminar: "%s"' % (key))

            else:

                print('Eliminado ...')

        else:

            if (key == 'passphrase'):

                value = db_hash.hash(value, iterations, security_chars, security_number, decrement_number)
                _passphrase_is = True

            elif (key == 'admins') and (agent == 'bot'):

                if not (value in show_user_admins.show()):

                    print('El administrador "%s" no existe ...' % (value))
                    sys.exit(1)

                else:

                    if (value in wrap.read(identifier, 'admins', separate=True)):

                        print('%s, ya está acargo de %s' % (value, identifier))
                        sys.exit(1)

            elif (key == 'privileges') and (agent == 'admin'):

                privileges_in_admin = wrap.read(identifier, key, agent=wrap.USE_ADMIN, separate=True)

                if ('ALL' in privileges_in_admin):

                    print('No puedes agregar más privilegios, ya tienes todos.')
                    sys.exit(1)

                if (value.lower() == 'all'):

                    if (len(privileges_in_admin) > 0):

                        print('No puedes agregar todos los privilegios cuando se tienen unos especificos. Primero debes eliminarlos para continuar.')
                        sys.exit(1)

                if not (value in global_conf.privileges):

                    print('No existe el privilegio a otorgar.')
                    sys.exit(1)

                if (value in privileges_in_admin):

                    print('El administrador ya tiene otorgado ese privilegio.')
                    sys.exit(1)
            
            result = wrap.write(identifier, key, value, separate=True) if (agent == 'bot') else wrap.write(identifier, key, value, agent=wrap.USE_ADMIN, separate=True)

            if (result == False):

                print('No se pudo agregar: "%s => %s"' % (key, value))

            else:

                print('Agregado: "%s" a "%s"' % (key, value))

                if (_passphrase_is == True):

                    print('Agregando más valores, debido a la frase de contraseña editada ...')

                    for _key, _value in {'iterations':iterations, 'securityNumber':security_number, 'security_chars':security_chars, 'decrementNumber':decrement_number}.items():

                        result = wrap.write(identifier, _key, _value, separate=True) if (agent == 'bot') else wrap.write(identifier, _key, _value, agent=wrap.USE_ADMIN, separate=True)

                        if (result == False):

                            print('Error editando la clave: "%s" con el valor: "%s"' % (_key, _value))

                            sys.exit(1)

                        else:

                            print('Se configuro correctamente: "%s" con el valor: "%s"' % (_key, _value))

                    print('Configuración exitosa.')

    except KeyError:

        #DEBUG
        #raise

        print('No se encontro la clave: "%s"' % (key))

    except Exception as Except:

        #DEBUG
        #raise

        print('Excepción desconocida: "%s"' % (Except))
