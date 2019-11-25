import requests
import re
import os
from hashlib import sha1
from urllib.parse import urlparse
from random import shuffle

from utils.Checks import admin_in_bot
from utils.Connections import sharebot
from utils.Wrappers import wrap
from utils.Checks import check_privileges
from utils.UI import debug
from utils.Connections import connector
from utils.Ciphers import generate_uniqkey
from utils.Ciphers import hibrid
from utils.sys_utils import create_folder
from utils.sys_utils import listLimit
from utils.Checks import check_headers
from utils.Checks import check_int
from utils.Checks import check_url
from utils.Checks import check_values
from utils.sys_utils import enum_bots
from utils.Wrappers import wrap_file
from utils.Ciphers import simplycrypt
from utils.sys_utils import bytes_convert

from modules.UI import rename_order

from conf import global_conf

cipher_file = True
RULE = 'STRICT'

nomenclature_error = '¡No está siguiendo la nomenclatura necesaria!'
convert_int_error = '{}, No es un valor númerico correcto ...'
share_folder = global_conf.databases['share']
profile_folder = '%s/%s' % (global_conf.databases['database'], global_conf.databases['profiles'])

def listOrder(id_, key, limit, agent=wrap.USE_BOT):

    _data = wrap.read(str(id_), key, agent=agent, separate=True)

    return(listLimit.list_(_data, int(limit)))

def execute(data, admin, log, reply):

    if not (check_values.check(data, 2) == True):

        log.logger(nomenclature_error, debug.WAR)

        return(False, None)

    else:

        if not (check_values.check(data[0], 2) == True):

            log.logger(nomenclature_error, debug.WAR)

            return(False, None)

    try:

        ((key, value), (use_nodes, node_headers)) = data

    except TypeError:

        ((key, value), use_nodes) = data
        node_headers = None

    if (reply == True):

        use_nodes = False

    admin = str(admin)
    limits = 1
    result = None
    execute = True
    error = False

    if (check_privileges.check(admin, key) == False):

        return(False, (-1, log.logger('No tiene permiso o hace falta el siguiente privilegio: "%s"' % (key), debug.COM)))

    if not (use_nodes == False):

        log.logger('Usará a Evie como el nodo de entrada ...', debug.WAR)

        if (check_privileges.check(admin, 'useNodes') == False):

            return(False, (False, log.logger('No tiene permiso de usar a Evie como el nodo de inicio ...', debug.WAR)))

        # - - - - - - - - - - - - - - - - - - - -  - - -

        try:

            check_headers.check(node_headers)

        except check_headers.InvalidHeader:

            return(False, (False, log.logger('El encabezado no es válido para la petición ...', debug.WAR)))

        nodes = wrap.read(use_nodes, 'list', agent=wrap.USE_NODE)

        if (nodes == False):

            return(False, (False, log.logger('No se encontró nodos disponibles a partir del (id)entificador proporcionado', debug.WAR)))

        wrap_nodes = {}
        end_node = nodes[-1]
        nodes_order = nodes[:-1]
        if (RULE == 'RANDOM'):
            shuffle(nodes_order)
        nodes = nodes_order + [end_node]
        node_rule = 0
        secrets_keys = [x[2] for x in nodes[:-1]]

        for _ in nodes:

            if (_[0] == nodes[0][0]):

                wrap_nodes[None] = [0, None, None]
                _first_node_url = _[0]
                _first_node_token = _[1]

                continue

            secret_key = secrets_keys[node_rule]

            if not (_[0] == end_node[0]):

                wrap_nodes[simplycrypt.encrypt(secret_key, _[0])] = [1, simplycrypt.encrypt(secret_key, _[1]), sha1(_[0].encode()).hexdigest()]
        
            else:
                
                wrap_nodes[simplycrypt.encrypt(secret_key, _[0])] = [1, None, sha1(_[0].encode()).hexdigest()]

            node_rule += 1

        _cipher = lambda string: hibrid.encrypt(string, end_node[4])

        _construct = {}
        _construct['username'] = end_node[1]
        _construct['passphrase'] = end_node[2]
        _construct['uniqkey'] = end_node[3]
        _construct['iterations'] = end_node[5]
        _construct['security_number'] = end_node[6]
        _construct['decrement_number'] = end_node[7]
        _construct['chars'] = end_node[8]
        _construct['data'] = _cipher(((key, value), False))
        _construct['reply'] = _cipher('1')
        
        response = connector.connect(_first_node_url, _first_node_token, 'resend', (wrap_nodes, _construct), log, headers=node_headers)
        response = str(response) if (response == None) else response

        if (response == False):

            log.logger('¡Ocurrio un error con la respuesta!', debug.WAR)

        else:

            log.logger('Recibido (lon:%d) ... mandando respuesta final ...' % (len(response)), debug.INF)
        
        return(response)
    
    if (key == 'listBots'):

        if (check_values.check(value, 2) == False):

            result = log.logger(nomenclature_error, debug.WAR)
            execute = False

        else:

            log.logger('Mandando lista de rook\'s ...', debug.INF)

            users = {}
            end_limit = check_int.check(value[0])
            pattern = str(value[1])

            if not (end_limit == None):

                log.logger('Indexando rook\'s ...', debug.INF)

                for bot_id, bot_name in enum_bots.enum(admin, False):

                    if (re.search(pattern, bot_name, re.IGNORECASE)):

                        users[bot_id] = bot_name
                    
                    if (limits == end_limit):

                        break
                    
                    limits += 1

                if (len(users) == 0):

                    log.logger('¡No se obtuvo ninguna coincidencia!', debug.WAR)

                else:

                    log.logger('Mandando "%d" rook\'s ...' % (len(users)), debug.PER)
                
                result = users

            else:

                result = log.logger(convert_int_error.format(value), debug.WAR)
                execute = False

    elif (key == 'getData'):

        if (check_values.check(value, 2) == False):

            result = log.logger(nomenclature_error, debug.WAR)
            execute = False

        else:

            log.logger('Mandando datos ...', debug.INF)
            
            bot_id = str(value[0])
            end_limit = check_int.check(value[1])

            if not (end_limit == None):

                if (admin_in_bot.check(admin, bot_id)):

                    log.logger('Mandando datos de: "{}" ...'.format(bot_id), debug.PER)

                    result = listOrder(bot_id, 'data', end_limit)

                else:

                    result = log.logger('No tiene permisos para obtener los datos de "{}"'.format(bot_id), debug.WAR)
                    execute = False

            else:

                result = log.logger(convert_int_error.format(value[1]), debug.WAR)
                execute = False

    elif (key == 'getCommands'):

        if (check_values.check(value, 2) == False):

            result = log.logger(nomenclature_error, debug.WAR)
            execute = False

        else:

            log.logger('Mandando comandos ...', debug.INF)

            bot_id = str(value[0])
            end_limit = check_int.check(value[1])

            if not (end_limit == None):

                if (admin_in_bot.check(admin, value[0])):

                    log.logger('Mandando comandos de: "{}"'.format(bot_id), debug.PER)

                    result = listOrder(bot_id, 'commands', end_limit)

                else:

                    result = log.logger('No tiene permisos para obtener los comandos de "{}"'.format(bot_id), debug.WAR)
                    execute = False

            else:

                result = log.logger(convert_int_error.format(value[1]), debug.WAR)
                execute = False

    elif (key == 'executeCommand'):

        if (check_values.check(value, 2) == False):

            result = log.logger(nomenclature_error, debug.WAR)
            execute = False

        else:

            bot_id = str(value[0])
            _cmd = str(value[1])

            log.logger('Agregará un comando a ser ejecutado por: "{}"'.format(bot_id), debug.PER)

            if (admin_in_bot.check(admin, bot_id)):

                # [False, command], donde "False", qué quiere decir que aún no se ejecuta ese comando

                if (wrap.write(bot_id, 'commands', [False, _cmd], separate=True) == True):

                    result = log.logger('Se agrego el comando: "{}"'.format(_cmd), debug.PER)
            
                else:

                    result = log.logger('Error agregando el comando "{}" a "{}"'.format(_cmd, bot_id), debug.COM)
                    execute = False

            else:

                result = log.logger('No tiene permiso de agregarle "{}" a "{}" ...'.format(_cmd, bot_id), debug.WAR)
                execute = False

    elif (key == 'shareBot'):
        
        if (check_values.check(value, 5) == False):

            result = log.logger(nomenclature_error, debug.WAR)
            execute = False

        else:

            bot_id = str(value[0])
            _secundaryServerAddr = str(value[1])
            _api_key = str(value[2])
            _headers = value[3]
            _shareFiles = bool(value[4])

            try:

                check_headers.check(_headers)

            except check_headers.InvalidHeader:

                result = log.logger('El encabezado no es válido para la petición ...', debug.WAR)
                execute = False

            else:

                if (check_url.check(_secundaryServerAddr, log) == False):

                    log.logger('Se va a compartir el rook: "{}" para el siguiente servidor: "{}"'.format(bot_id, _secundaryServerAddr), debug.WAR)

                    if (admin_in_bot.check(admin, bot_id)):
                        
                        response = sharebot.share(bot_id, _secundaryServerAddr, _api_key, _headers, _shareFiles, log)

                        if (response == True):

                            log.logger('Agregando servidor secundario a :: "{}"'.format(bot_id), debug.WAR)

                            _secundaryServers = wrap.read(bot_id, 'servers', separate=True)
                            _server = '%s://%s/' % (urlparse(_secundaryServerAddr).scheme, urlparse(_secundaryServerAddr).netloc)
                           
                            if not (_server in _secundaryServers):

                                _obj = wrap.getall(wrap.USE_TMP)

                                _hash_server = sha1(_secundaryServerAddr.encode()).hexdigest()

                                if not (_obj.get(_hash_server) == None):

                                    if (wrap.write(bot_id, 'servers', [_server, _obj[_hash_server]['pub_key']], separate=True) == True):

                                        result = log.logger('Agregado, servidor secundario: "{}" a "{}"'.format(_server, bot_id), debug.PER)

                                    else:


                                        execute = False
                                        result = log.logger('Error agregando el servidor secundario: "{}"'.format(_server), debug.COM)

                                else:


                                    execute = False
                                    result = log.logger('Hubo un error, no se pudo obtener la clave pública del servidor secundario: "{}"'.format(_server), debug.COM)

                            else:

                                execute = False
                                result = log.logger('¡El servidor secundario ya existe!', debug.WAR)

                        else:

                            result = log.logger('Ocurrio un error enviando el rook: "{}"'.format(response[1]), debug.WAR)
                            execute = False

                    else:

                        result = log.logger('No tiene permisos para compartir el siguiente rook "{}"'.format(bot_id), debug.WAR)
                        execute = False

                else:

                    result = log.logger('La dirección del servidor secundario no es correcta ...', debug.WAR)
                    execute = False

    elif (key == 'getToken'):
        
        log.logger('Compartiendo el token de acceso público ...', debug.INF)
        
        result = wrap.read('token', 'token', agent=wrap.USE_TOKEN)

    elif (key == 'listServers'):

        if (check_values.check(value, 2) == False):

            result = log.logger(nomenclature_error, debug.WAR)
            execute = False

        else:

            log.logger('Mandando lista de servidores secundarios ...', debug.INF)

            bot_id = str(value[0])
            end_limit = check_int.check(value[1])
            
            if not (end_limit == None):

                if (admin_in_bot.check(admin, bot_id)):
                    
                    log.logger('Enviado, lista de servidores secundarios', debug.INF)

                    result = []
                    _dat = listOrder(bot_id, 'servers', end_limit)

                    [result.append(x[0]) for x in _dat]

                else:

                    result = log.logger('No tiene permiso para obtener los servidores secundarios de "{}"'.format(bot_id), debug.WAR)
                    execute = False

            else:

                result = log.logger(convert_int_error.format(value[1]))
                execute = False

    elif (key == 'delServer'):

        if (check_values.check(value, 2) == False):

            result = log.logger(nomenclature_error, debug.WAR)
            execute = False

        else:

            log.logger('Borrara un servidor secundario ...', debug.WAR)
            
            bot_id = str(value[0])
            _index = check_int.check(value[1], False)
            
            if (_index == None):

                result = log.logger('{}, No es un indíce correcto'.format(value[1]), debug.WAR)
                execute = False

            else:

                if (admin_in_bot.check(admin, bot_id)):

                    try:

                        secundaryServer = wrap.read(bot_id, 'servers', separate=True)[_index]

                        if (wrap.write(bot_id, 'servers', _index, target=wrap.TARGET_DELETE_INDEX, separate=True) == True):

                            result = log.logger('Borro el servidor secundario: "{} - (indíce:{})"'.format(secundaryServer[0], _index), debug.COM)

                        else:

                            result = log.logger('No se puede borrar el servidor secundario ...', debug.WAR)
                            execute = False

                    except IndexError:

                        result = log.logger('Es probable que el indíce proporcionado no sea correcta para la operación ...', debug.COM)
                        execute = False

                else:

                    result = log.logger('No tiene permiso para borrar el servidor secundario de "{}"'.format(bot_id), debug.WAR)
                    execute = False

    elif (key == 'writeNodes'):

        log.logger('Escribirá nodos ...', debug.WAR)
        log.logger('Comprobando que siga la especificación acordada ...', debug.WAR)
        log.logger('Comprobando el tipo de dato ...', debug.INF)

        if not (isinstance(value, list)):

            error = True 
            log.logger('El tipo de dato no es correcto ...', debug.WAR)

        else:

            log.logger('El tipo de dato es correcto', debug.INF)

            if (len(value) < 2):

                error = True
                result = log.logger('¡La longitud de los nodos no es correcta!', debug.WAR)

            else:

                log.logger('La longitud de los nodos es correcta', debug.INF)

                _init_node = value[:-1]
                _end_node = value[-1]

                if not (isinstance(_init_node, list)) or not (isinstance(_end_node, list)):

                    error = True
                    log.logger('¡El tipo de dato de los nodos intermedios o del nodo final no es correcta!', debug.WAR)

                else:

                    if not (len(_init_node) >= 1):

                        error = True
                        log.logger('¡La longitud de los nodos intermedios no es correcta!', debug.WAR)

                    else:

                        log.logger('Comprobando longitud de los nodos intermedios individualmente ...', debug.INF)

                        if not ([] == [log.logger('¡La longitud de {} no es correcta!'.format(x), debug.WAR) for x in _init_node if (len(x) != 3)]):

                            error = True
                            result = log.logger('La longitud de un nodo intermedio no es correcta ...', debug.WAR)

                        else:

                            log.logger('La longitud de los nodos intermedios es correcta', debug.INF)
                            log.logger('Comprobando las direcciónes de los nodos intermedios ...', debug.WAR)

                            for i, _ in enumerate(_init_node):

                                log.logger('Comprobando dirección: {}'.format(_[0]), debug.WAR)

                                _url = value[i][0] = str(_[0])
                                value[i][1] = str(_[1]) 

                                error = check_url.check(_url, log)

                                if (error == True):

                                    break

                            if (error == False):

                                log.logger('Comprobando longitud del nodo final  ...', debug.WAR)

                                if not (len(_end_node) == 9):

                                    error = True
                                    result = log.logger('La longitud del nodo final no es correcta ...', debug.WAR)

                                else:

                                    log.logger('La longitud del nodo final es correcta', debug.INF)
                                    log.logger('Comprobando que no haya campos vacios ...', debug.WAR)

                                    if (True in [True for x in _end_node if (x == '')]):

                                        error = True
                                        result = log.logger('Hay campos sin definir ...', debug.WAR)

                                    else:

                                        log.logger('Comprobando la dirección del nodo final: {}'.format(_end_node[0]), debug.WAR)

                                        error = check_url.check(_end_node[0], log)

        if (error == False):

            log.logger('¡Comprobación exitosa!', debug.INF)

            _nodes = []
            log.logger('Generando (id)entificador del nodo ...', debug.INF)
            _node_id = generate_uniqkey.generate()
            log.logger('Generado: %s' % (_node_id), debug.PER)

            [_nodes.append(x[0]) for x in value]

            log.logger('Escribiendo nodos "%s" en el almacén' % (' -> '.join(_nodes)), debug.PER)

            if (wrap.add(_node_id, {'list':value}, agent=wrap.USE_NODE) == True):

                log.logger('Nodos escritos correctamente (ID:{})'.format(_node_id), debug.PER)

                result = _node_id

            else:

                result = log.logger('No se pudo escribir los nuevos nodos (ID:{})'.format(_node_id), debug.WAR)
                execute = False

        else:

            execute = False

    elif (key == 'addNode'):

        if (check_values.check(value, 2) == False):

            result = log.logger(nomenclature_error, debug.WAR)
            execute = False

        else:

            node_id = str(value[0])
            node = value[1]

            if not (isinstance(node, list)):

                result = log.logger('¡El tipo de dato del nodo no es correcto!', debug.WAR)
                execute = False

            else:

                if (len(node) != 3):

                    result = log.logger('La longitud del nodo no es correcta', debug.WAR)
                    execute = False

                else:

                    if (check_url.check(node[0], log) == True):

                        result = log.logger('¡La dirección URL no es válida!', debug.WAR)
                        execute = False

                    else:

                        if (wrap.write(node_id, 'list', node, agent=wrap.USE_NODE, target=wrap.TARGET_INSERT, index_insert=-1) == True):

                            result = log.logger('Nuevo nodo agregado: {} (ID:{})'.format(node[0], node_id), debug.PER)

                        else:

                            result = log.logger(log.logger('No se pudo agregar al nodo: "{}" (ID:{})'.format(node[0], node_id)), debug.COM)
                            execute = False

    elif (key == 'getNodes'):

        action = str(value)

        if (action.lower() == 'all'):

            log.logger('Obteniendo datos de todos los nodos', debug.INF)

            result = wrap.getall(agent=wrap.USE_NODE)

        else:

            log.logger('Obteniendo datos del nodo -> {}'.format(action), debug.PER)

            result = wrap.read(action, 'list', agent=wrap.USE_NODE)

        if not (result == False):

            log.logger('Enviando los datos de los nodos ...', debug.INF)

        else:

            result = log.logger('Error enviando los datos de los nodos', debug.COM)
            execute = False

    elif (key == 'delNodes'): 

        if (check_values.check(value, 2) == False):

            result = log.logger(nomenclature_error, debug.WAR)
            execute = False

        else:

            node = str(value[0])
            action = str(value[1])

            log.logger('Borrara nodos ...', debug.WAR)

            if (str(action).lower() == 'all'):

                log.logger('Borrando los nodos del ID: "{}"'.format(node), debug.COM)

                if (wrap.delete(node) == True):

                    result = log.logger('Borrado, todos los nodos de "{}"'.format(node), debug.WAR)

                else:

                    result = log.logger('Error borrando: "{}"'.format(node), debug.WAR)
                    execute = False
        
            else:

                _index = check_int.check(action, False)

                if not (_index == None):

                    log.logger('Verificando que haya minimo, un nodo intermedio y el nodo final, para evitar un borrado peligroso ...', debug.WAR)

                    _nodes = wrap.read(node, 'list', agent=wrap.USE_NODE)

                    if not (_nodes == False):

                        if (len(_nodes) > 2):
                            
                            if not (_index == -1) and not (_index == len(_nodes)-1):

                                _node_to_delete = _nodes[_index][0]

                                log.logger('Borrando el nodo -> {} (ID:{})'.format(_node_to_delete, node), debug.COM)

                                if (wrap.write(node, 'list', action, agent=wrap.USE_NODE, target=wrap.TARGET_DELETE_INDEX) == True):

                                    result = log.logger('Borrado: "{}" (ID:{})'.format(_node_to_delete, node), debug.WAR)

                                else:

                                    result = log.logger('Error borrando "{}" (ID:{})'.format(_node_to_delete, node), debug.COM)
                                    execute = False

                            else:

                                result = log.logger('¡No se puede borrar el nodo final!', debug.WAR)
                                execute = False

                        else:

                            result = log.logger('No puede borrar nodos, mientras haya solamente un nodo intermedio', debug.WAR)
                            execute = False

                    else:

                        result = log.logger('¡No existe el nodo especificado!', debug.WAR)
                        execute = False

                else:

                    result = log.logger(convert_int_error.format(action), debug.WAR)
                    execute = False

    elif (key == 'updateNode'):
        
        if (check_values.check(value, 4) == False):

            result = log.logger(nomenclature_error, debug.WAR)
            execute = False

        else:

            node_id = str(value[0])
            value_ = str(value[1])
            _index = check_int.check(value[2], False)
            _subindex = check_int.check(value[3], False)

            if (_index == None):

                error = True

                result = log.logger('{}, No es un indíce correcto'.format(_index), debug.WAR)

            if (_subindex == None):

                error = True

                result = log.logger('{}, No es un sub-indíce correcto'.format(_subindex), debug.WAR)

            if (error == False):

                log.logger('Actualizando nodo: "ID:{}"'.format(node_id), debug.PER)

                _get_nodes = wrap.read(node_id, 'list', agent=wrap.USE_NODE)[-1]

                if (_index == -1) or (_index == len(_get_nodes)-1):

                    if (_subindex != 0):

                        return(False, log.logger('No puedes actualizar ningún dato del nodo final al menos que sea la dirección URL', debug.WAR))

                if (_subindex == 0):

                    log.logger('Actualizará la dirección URL de un nodo...', debug.WAR)

                    if (check_url.check(value_, log) == True):

                        return(False, log.logger('La dirección URL no es válida', debug.WAR))

                if (wrap.write(node_id, 'list', value_, agent=wrap.USE_NODE, target=wrap.TARGET_SUBINDEX_UPDATE, array_subindex=(_index, _subindex)) == True):

                    result = log.logger('Nodo (ID:{}) actualizado con éxito'.format(node_id), debug.PER)

                else:

                    result = log.logger('Error actualizando el nodo: "ID:{}"'.format(node_id), debug.COM)
                    execute = False

            else:

                execute = False

    elif (key == 'access_list'):

        log.logger('Enviando lista de las fechas de inicio de sesión ..."', debug.INF)

        end_limit = check_int.check(value)

        if not (end_limit == None):
        
            result = listOrder(admin, 'lastLogin', end_limit, agent=wrap.USE_ADMIN)

        else:

            result = log.logger(convert_int_error.format(value))
            execute = False

    elif (key == 'ping'):

        log.logger('ping ... haciendo pong ...', debug.INF)

    elif (key == 'getPeers'):

        log.logger('Obtendrá todos los puntos de la red ...', debug.WAR)

        result = wrap.getall(wrap.USE_PEER)

        if (len(result) == 0):

            result = log.logger('Aún no hay nodos en la red...', debug.WAR)
            execute = False

        else:

            log.logger('Mandando %d puntos ...' % (len(result)), debug.PER)

    elif (key == 'upload'):

        if (check_values.check(value, 3) == False):

            result = log.logger(nomenclature_error, debug.WAR)
            execute = False

        else:

            _content = value[0]
            _filename = os.path.basename(str(value[1]))
            bot_id = os.path.basename(str(value[2]))

            if (admin_in_bot.check(admin, bot_id)):

                _save = '%s/%s' % (share_folder, bot_id)

                create_folder.create(_save)

                _save += '/%s' % (_filename)

                log.logger('Escribiendo archivo "{}" ...'.format(_save), debug.PER)

                _bak_save = rename_order.rename(_save)

                if not (_bak_save == False):

                    log.logger('El archivo ya existe ...', debug.WAR)

                    _save = _bak_save

                    log.logger('Renombrado a: "{}"'.format(_save), debug.PER)

                try:

                    if (cipher_file == True):

                        wrap_file.wrap(_save, wrap._new_passwd, _content)

                    else:

                        with open(_save, 'wb') as file_object:

                            file_object.write(bytes_convert.convert(_content))

                except Exception as Except:

                    result = log.logger('Ocurrio una excepción escribiendo a: "{}". Excepción: "{}"'.format(_filename, Except), debug.WAR)
                    execute = False

                else:

                    result = log.logger('El archivo "{}" fue subido satisfactoriamente ...'.format(_filename), debug.PER)

            else:

                result = log.logger('No tiene permiso para subir el archivo "{}" a el espacio de directorio de "{}"'.format(_filename, bot_id), debug.COM)
                execute = False

    elif (key == 'download'):

        if (check_values.check(value, 2) == False):

            result = log.logger(nomenclature_error, debug.WAR)
            execute = False

        else:

            _filename = os.path.basename(str(value[0]))
            bot_id = os.path.basename(str(value[1]))

            if (admin_in_bot.check(admin, bot_id)):
            
                _save = '{}/{}/{}'.format(profile_folder, bot_id, _filename)
                
                log.logger('Quiere recuperar el archivo: "{}" ...'.format(_save), debug.PER)

                if (os.path.isfile(_save)):

                    log.logger('Leyendo archivo ...', debug.INF)

                    try:

                        if (cipher_file == True):

                            result = wrap_file.wrap(_save, wrap._new_passwd)

                            if (result == False):

                                log.logger('{}, no se pudo desencriptar..., Intentando sin desencriptar...'.format(_save), debug.WAR)

                        if (result == False) or (cipher_file == False):

                            with open(_save, 'rb') as file_object:

                                result = file_object.read()

                    except Exception as Except:

                        result = log.logger('Ocurrio una excepción leyendo a: "{}". Excepción: "{}"'.format(_filename, Except), debug.WAR)
                        execute = False

                    else:

                        log.logger('Leido.', debug.INF)
                        log.logger('Enviando archivo: "{}" ...'.format(_save), debug.PER)

                else: 

                    result = log.logger('El archivo "{}" no existe ...'.format(os.path.basename(_save)), debug.WAR)
                    execute = False

            else:

                result = log.logger('No tiene permiso para descargar el archivo "{}" de "{}"'.format(os.path.basename(_save), value[1]), debug.COM)
                execute = False

    elif (key == 'sharedFiles'):

        if (check_values.check(value, 3) == False):

            result = log.logger(nomenclature_error, debug.WAR)
            execute = False

        else:

            _bot_id = os.path.basename(str(value[0]))
            end_limit = check_int.check(value[1])
            pattern = str(value[2])
            _files = '{}/{}'.format(share_folder, _bot_id)

            log.logger('Mandando lista de archivos compartidos de "{}"'.format(_bot_id), debug.WAR)

            if not (end_limit == None):

                if (os.path.isdir(_files)):

                    result = []

                    for _ in listLimit.list_(sorted(os.listdir(_files)), end_limit):

                        result.append(_) if (re.search(pattern, _, re.IGNORECASE)) else None

                    if (len(result) == 0):

                        log.logger('¡No se obtuvo ninguna coincidencia!', debug.WAR)

                    else:

                        log.logger('Mandado %d archivos ...' % (len(result)), debug.PER)

                else:

                    result = log.logger('No se ha creado el directorio compartido de: "{}"'.format(_bot_id), debug.WAR)
                    execute = False

            else:

                result = log.logger(convert_int_error.format(value[1]), debug.WAR)
                execute = False

    elif (key == 'listFiles'):

        if (check_values.check(value, 3) == False):

            result = log.logger(nomenclature_error, debug.WAR)
            execute = False

        else:
        
            _bot_id = os.path.basename(str(value[0]))
            _files = '{}/{}'.format(profile_folder, _bot_id)
            end_limit = check_int.check(value[1])
            pattern = str(value[2])

            log.logger('Mandando lista de archivos de "{}"'.format(_bot_id), debug.WAR)
            
            if not (end_limit == None):

                if (os.path.isdir(_files)):

                    result = []

                    for _ in listLimit.list_(sorted(os.listdir(_files)), end_limit):

                        result.append(_) if (re.search(pattern, _, re.IGNORECASE)) else None

                    if (len(result) == 0):

                        log.logger('¡No se obtuvo ninguna coincidencia!', debug.WAR)

                    else:

                        log.logger('Mandando %d archivos ...' % (len(result)), debug.PER)

                else:

                    result = log.logger('El directorio de perfil de "{}" no existe ...'.format(_bot_id), debug.COM)
                    execute = False

            else:

                result = log.logger(convert_int_error.format(value[1]), debug.WAR)
                execute = False

    elif (key == 'addQueue'):

        if (check_values.check(value, 3) == False):

            result = log.logger(nomenclature_error, debug.WAR)
            execute = False

        else:

            _bot_id = str(value[1])
            _command = str(value[0])
            _args = value[2]

            if (isinstance(_args, dict)):

                log.logger('Agregará un comando del sistema a la cola de: "{}"'.format(_bot_id), debug.PER)

                if (admin_in_bot.check(admin, _bot_id)):

                    if (wrap.write(_bot_id, 'Queue', [_command, _args], separate=True) == True):

                        result = log.logger('Se agregó "{}" a la cola ...'.format(_command), debug.PER)
                
                    else:

                        result = log.logger('Error agregando el comando del sistema "{}" a "{}"'.format(_command, _bot_id), debug.COM)
                        execute = False

                else:

                    result = log.logger('No tiene permiso de agregarle "{}" a "{}" ...'.format(_command, _bot_id), debug.WAR)
                    execute = False

            else:

                result = log.logger('¡El tipo de dato de los parámetros no es correcto!', debug.WAR)
                execute = False

    else:

        return(False)

    return(execute, result)
