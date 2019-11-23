import shelve
import sys
from os.path import isfile, basename, isdir
from os import listdir, chmod

from utils.sys_utils import create_folder
from utils.Ciphers import simplycrypt

from modules.Ciphers import obfuscate_passwd
from modules.Ciphers import db_hash
from modules.UI import iInput
from modules.UI import argprogrammer

from conf import global_conf

USE_ADMIN = 1 # Identificador de los Administradores
USE_BOT = 2 # Identificador de los Bot's
USE_CONFIG = 3 # Identificador de la configuración
USE_DEFEND = 4 # Identificador de la defensa
USE_MESSAGE = 5 # Identificador de los mensajes públicos
USE_NODE = 6 # Identificador de los nodos
USE_NODE_INFO = 7 # Identificador de la información de los nodos (Usado por Jacob)
USE_PEER = 8 # Identificador de los puntos
USE_PERSONAL = 9 # Se usa este identificador para un almacén personal (Mayormente usando los complementos)
USE_SECRET_KEY = 10 # Identificador de la clave secreta
USE_SERVER = 11 # Identificador de las claves del servidor
USE_SESSION = 12 # Identificador para las sesiones grabadas
USE_SPAM = 13 # Identificador de los intentos fallidos en los Bot's
USE_SPAM_FOR_ADMINS = 14 # Identificador de los intentos fallidos en los Administradores
USE_TMP = 15 # Identificador de la cache (Hasta el momento, sólo se guardan claves públicas de los nodos servidores para la comunicación de pública)
USE_TOKEN = 16 # Identificador del token de acceso público

TARGET_DELETE = 17  # Borrar un valor
TARGET_ADD = 18  # Agregar un valor
TARGET_DELETE_INDEX = 19  # Borrar un valor en un array por su indíce
TARGET_SUBINDEX_UPDATE = 20  # Actualizar un valor por sub indíce -> array[index][subindex]
TARGET_INSERT = 21  # Agregar un valor a un array estilo -> array.insert(index, data)
TARGET_UNSET = 22 # En el caso de que el tipo de dato a tratar sea un «str» sería igual a TARGET_DELETE, pero en cambio con un «list» se borraría todo o basicamente se colocaría "[]"

ARRAY_INIT = 23  # Comenzar a iterar desde el comienzo hasta el final
ARRAY_END = 24  # Comenzar a iteral desde el final hasta el comienzo

db_passwd_file = '%s/%s' % (global_conf.conf['conf_dir'], global_conf.conf['db_passwd'])
_verify = lambda filename: len(open(filename, 'rt').read()) > 0 if (isfile(filename)) else False

#sys.setrecursionlimit(limit)

def _input(input_message, error_message, char=None, datatype=str):

    while (True):

        try:

            print(input_message)
            debug = iInput.iInput(char=char, indicator=': ', datatype=datatype)

        except KeyboardInterrupt:

            print()
            print('Saliendo ...')
            sys.exit(1)
    
        else:

            if not debug:

                print(error_message)
                continue

            else:

                return(debug)

_parsers = argprogrammer.Parser()
_parsers.set_head('''
       Syndicate Project - Desencriptar el almacén
       -----------------   -----------------------''')
_parsers.set_footer('''
    Nota: *Si no se definen los parámetros, se le preguntará*
''')

for _ in (dict(param_name=['-db-help'], key='help', help='Mostrar la ayuda y sale'),
        dict(param_name=['-db-iterations'], key='iterations', help='Número de iteraciones', type=int),
        dict(param_name=['-db-security-number'], key='security_number', help='Número de seguridad', type=int),
        dict(param_name=['-db-decrement-number'], key='decrement_number', help='Número de disminución', type=int),
        dict(param_name=['-db-passphrase'], key='passphrase', help='Frase de contraseña'),
        dict(param_name=['-db-chars'], key='security_chars', help='Caracteres de seguridad'),
        dict(param_name=['-db-check'], key='force', help='Verificar los parámetros (Sólo para desorrollo)', action=True, type=bool)):

    _parsers.add(**_)

_args = _parsers.parse_args(show_error=False)

force = _args.force

if (force == True):

    _args = _parsers.parse_args()
    sys.exit(0)

passphrase = _args.passphrase

try:
    iterations = _args.iterations
    if (iterations == 0):
        raise TypeError
except ValueError:
    print('El tipo de valor de la iteraciones no es númerico!')
    sys.exit(1)
except TypeError:
    iterations = None

try:
    security_number = _args.security_number
    if (security_number == 0):
        raise TypeError
except ValueError:
    print('El tipo de valor de él número de seguridad no es númerico!')
    sys.exit(1)
except TypeError:
    security_number = None

try:
    decrement_number = _args.decrement_number
    if (decrement_number == 0):
        raise TypeError
except ValueError:
    print('El tipo de valor de él número de disminución no es númerico!')
    sys.exit(1)
except TypeError:
    decrement_number = None

security_chars = _args.security_chars

_init = None in [passphrase, iterations, security_number, decrement_number]

if (_init == True):

    print('* Datos para desencriptar la frase de contraseña *')
    print('  %s' % (''.join(['-' for x in range(46)])))
    print()

    passphrase = _input('Ingrese la frase de contraseña:', 'No ingreso la frase de contraseña!', char='*')
    security_chars = _input('Ingrese los caracteres de seguridad:', 'No ingreso los caracteres de seguridad')
    iterations = _input('Ingrese el número de iteraciones:', 'No ingreso ningún número de iteraciones!', datatype=int)
    security_number = _input('Ingrese el número de seguridad:', 'No ingreso el número de seguridad', datatype=int)
    decrement_number = _input('Ingrese el número de disminución:', 'No ingreso el número de disminución', datatype=int)

    _new_passwd = obfuscate_passwd.obfuscate('%s%s%s%s%s' % (passphrase, security_chars, iterations, security_number, decrement_number))

    if not (_verify(db_passwd_file) == True):

        _hash = db_hash.hash(_new_passwd, iterations, security_chars, security_number, decrement_number)

        try:

            with open(db_passwd_file, 'wt') as _obj:

                _obj.write(_hash)

        except Exception as Except:

            print('Hubo un error guardando el hash de la frase de contraseña: "%s"' % (Except))
            sys.exit(1)

        else:

            print('Se guardo satisfactoriamente en -> %s' % (db_passwd_file))

    else:

        try:

            with open(db_passwd_file, 'rt') as _obj:

                _hash = _obj.read().rstrip()

        except Exception as Except:

            print('Ocurrió un error leyendo el hash de la frase de contraseña. Excepción: "%s"' % (Except))
            sys.exit(1)

        if (db_hash.compare(_new_passwd, _hash, iterations, security_chars, security_number, decrement_number) == True):

            print('Correcto, se puede leer el almacén con tranquilidad ...')

        else:

            print('Incorrecto, no se puede leer el almacén con tranquilidad, debido a que los datos introducidos son incorrectos ...')
            sys.exit(1)

else:

    _new_passwd = obfuscate_passwd.obfuscate('%s%s%s%s%s' % (passphrase, security_chars, iterations, security_number, decrement_number))

    if (_verify(db_passwd_file)):

        with open(db_passwd_file, 'rt') as _obj:

            _hash = _obj.read().rstrip()

    else:

        _hash = db_hash.hash(_new_passwd, iterations, security_chars, security_number, decrement_number)

        with open(db_passwd_file, 'wt') as _obj:

            _obj.write(_hash)
        
chmod(db_passwd_file, 0o644)

class agentNotExists(Exception):

    """
    Cuando el agente no existe
    """

class values_is_not_defined(Exception):

    """
    Cuando algún valor no está definido
    """

class incorrect_passphrase(Exception):

    """
    Cuando la frase de contraseña es incorrecta
    """

class databaseIsNotDefined(Exception):

    """
    Cuando la ruta del almacén no está definida
    """

if not (db_hash.compare(_new_passwd, _hash, iterations, security_chars, security_number, decrement_number) == True):

    raise incorrect_passphrase('Frase de contraseña incorrecta ...')

def __agentDetect(agent, username=None, separate=False, ignore=False, personal=None):

    database = global_conf.databases
    conf = global_conf.conf

    db_root = str(database['database'])
    db_conf = str(conf['conf_dir'])

    if (agent == USE_BOT):

        db = '%s/%s' % (db_root, database['credentials'])

    elif (agent == USE_ADMIN):

        db = '%s/%s' % (db_root, database['admins'])

    elif (agent == USE_NODE):

        db = '%s/%s' % (db_root, database['nodes'])

    elif (agent == USE_SPAM):
        
        db = '%s/%s' % (db_root, database['spam'])

    elif (agent == USE_SPAM_FOR_ADMINS):

        db = '%s/%s' % (db_root, database['spam_for_admins'])

    elif (agent == USE_DEFEND):
        
        db = '%s/%s' % (db_root, database['defend'])

    elif (agent == USE_PEER):

        db = '%s/%s' % (db_root, database['peers'])

    elif (agent == USE_TMP):

        db = '%s/%s' % (db_root, database['tmp'])

    elif (agent == USE_TOKEN):

        db = '%s/%s' % (db_conf, conf['token'])

    elif (agent == USE_SECRET_KEY):

        db = '%s/%s' % (db_conf, conf['secret_key'])

    elif (agent == USE_SERVER):

        db = '%s/%s' % (db_conf, conf['keys'])

    elif (agent == USE_CONFIG):

        db = '%s/%s' % (db_conf, conf['conf_file'])

    elif (agent == USE_NODE_INFO):

        db = '%s/%s' % (db_conf, conf['node_info'])

    elif (agent == USE_MESSAGE):

        db = '%s/%s' % (db_root, database['messages'])

    elif (agent == USE_SESSION):

        db = '%s/%s' % (db_root, database['session'])

    elif (agent == USE_PERSONAL):

        if not (isinstance(personal, str)):

            raise databaseIsNotDefined('La ruta del almacén no está definida')

        db = personal

    else:

        raise agentNotExists('El agente no existe ...')

    if (basename(db) == ''):

        raise RuntimeError('El nombre del almacén no es correcto')

    if not (separate == False) and (isinstance(username, str)):

        create_folder.create(db)

        db = '{}/{}'.format(db, username)

    else:

        if not (ignore == True):

            if (isdir(db) == True):

                raise OSError('¡No puede abrir "%s" como si fuera un archivo!' % (db))

            with shelve.open(db):

                pass

            try:

                chmod('{}.db'.format(db), 0o644)

            except:

                pass

    return(db)

_encrypt = lambda data: simplycrypt.encrypt(_new_passwd, data)
_decrypt = lambda data: simplycrypt.decrypt(_new_passwd, data)

def getDB(agent=USE_DEFEND, personal=None):

    db = __agentDetect(agent, None, False, True, personal)

    return(db)

def raw(agent=USE_BOT, username=None, separate=False, personal=None):

    db = __agentDetect(agent, username, separate, personal=personal)

    try:

        return(shelve.open(db, writeback=True))

    except Exception:

        #DEBUG
        #raise

        return(False)

def getall(agent=USE_BOT, username=None, separate=False, personal=None):

    db = __agentDetect(agent, username, separate, personal=personal)

    _result = {}

    try:

        with shelve.open(db, flag='r') as obj:

            for _ in obj:

                _result[_] = _decrypt(obj[_])

            return(_result)

    except Exception:

        #DEBUG
        #raise

        return(False)

def add(key, data, agent=USE_BOT, username=None, separate=False, personal=None):

    db = __agentDetect(agent, username, separate, personal=personal)

    with shelve.open(db, writeback=True) as obj:

        obj[key] = _encrypt(data)

    return(True)

def delete(key, agent=USE_NODE, username=None, separate=False, personal=None):

    db = __agentDetect(agent, username, separate, personal=personal)

    try:

        with shelve.open(db, writeback=True) as obj:

            del obj[key]

    except KeyError:

        return(False)

    else:

        return(True)

def write(username, key, value, agent=USE_BOT, target=TARGET_ADD, array_iter=ARRAY_END, array_subindex=(0, 0), index_insert=0, separate=False, personal=None):

    db = __agentDetect(agent, username, separate, personal=personal)

    try:

        with shelve.open(db, writeback=True) as obj:

            wrapper = _decrypt(obj[username])

            if (isinstance(wrapper[key], list) == True):

                if (target == TARGET_ADD):

                    wrapper[key].append(value)

                elif (target == TARGET_INSERT):

                    wrapper[key].insert(index_insert, value)

                elif (target == TARGET_SUBINDEX_UPDATE):

                    if not (len(array_subindex) == 2) or not (isinstance(array_subindex, tuple) == True):

                        return(False)

                    wrapper[key][int(array_subindex[0])][array_subindex[1]] = value

                elif (target == TARGET_DELETE_INDEX):

                    wrapper[key].pop(int(value)) 

                elif (target == TARGET_UNSET):

                    wrapper[key] = []

                elif (target == TARGET_DELETE):

                    array = wrapper[key]
                    _limit = 0

                    if not (value in array):

                        return(False)

                    if (array_iter == ARRAY_END):

                        array.reverse()

                    elif (array_iter == ARRAY_INIT):

                        pass

                    else:

                        return(False)

                    for _ in array:

                        if (_ == value):

                            del array[_limit]

                            break

                        _limit += 1

                else:

                    return(False)

            else:

                if (target == TARGET_ADD):
                    
                    wrapper[key] = value

                elif (target == TARGET_DELETE):

                    wrapper[key] = None

            obj[username] = _encrypt(wrapper)

            return(True)

    except:

        # DEBUG
        #raise

        return(False)

def read(username, key=None, agent=USE_BOT, separate=False, personal=None):

    db = __agentDetect(agent, username, separate, personal=personal)

    try:

        with shelve.open(db, flag='r') as obj:

            wrapper = _decrypt(obj[username])

            if not (key == None):

                return(wrapper[key])

            else:

                return(wrapper)

    except:

        # DEBUG
        #raise

        return(False)

    else:

        return(True)
