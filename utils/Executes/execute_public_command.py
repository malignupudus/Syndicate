import requests
from os import getcwd, makedirs, listdir
from os.path import isdir, basename, splitext
from time import time

from modules.UI import rename_order

from utils.Wrappers import wrap
from utils.Checks import key_check_in_dict
from utils.Connections import connector
from utils.UI import debug
from utils.Extracts import real_extract_root_administrators
from utils.Ciphers import simplycrypt
from utils.Ciphers import generate_uniqkey
from utils.sys_utils import create_folder
from utils.Checks import check_url
from utils.sys_utils import bytes_convert
from utils.Shows import show_user_rooks
from utils.sys_utils import enum_bots

from conf import global_conf

public_files = global_conf.databases['public_files']

user_agent = ''
public_service = False

def execute(data, log):

    if not (isinstance(data, dict)):

        log.logger('¡El tipo de dato de los datos no es correcto!', debug.WAR)
        return(False)

    if (len(data) != 2):

        log.logger('¡La longitud de los datos no es correcta!', debug.WAR)
        return(False)

    if (data.get('token') == None) or (data.get('command') == None):

        log.logger('¡Hace falta el token o el comando!', debug.WAR)
        return(False)

    _keys = wrap.read('keys', agent=wrap.USE_SERVER)

    if (_keys == False):

        log.logger('No se pudo leer el par de claves de Evie...', debug.COM)
        return(False)

    (pub_key, priv_key) = (_keys['public_key'], _keys['private_key'])
    real_token = wrap.read('token', 'token', agent=wrap.USE_TOKEN)
    real_secret_key = wrap.read('secret_key', 'secret_key', agent=wrap.USE_SECRET_KEY)

    if (real_token == False):

        log.logger('No se pudo leer el token de acceso...', debug.COM)
        return(False)

    token = data['token']

    if not (isinstance(token, str)):

        log.logger('El tipo de dato del token de acceso no es correcto...', debug.WAR)
        return(False)

    if (token == real_token):
        
        log.logger('Correcto, el token de acceso es correcto ...', debug.INF)
    
    else:
        
        log.logger('Incorrecto, el token de acceso es incorrecto ...', debug.COM)
        return(False)

    (key, value) = data['command']

    if not (isinstance(key, str)):

        log.logger('¡El tipo de dato del comando o el valor no es correcto!', debug.WAR)
        return(False)

    if not (public_service == False):

        if not (key in public_service):

            log.logger('%s, No está habilitado en estos momentos o no existe ...' % (key), debug.WAR)
            return(False)

    if (key == 'getPubKey'):
        
        log.logger('Desea obtener la clave pública del servidor ...', debug.WAR)
        
        return(pub_key)

    elif (key == 'saveData'):

        log.logger('Construyendo perfil de un rook ...', debug.INF)

        if not (isinstance(value, list)):

            log.logger('¡El tipo de dato no es correcto!', debug.WAR)

            return(False)

        if (len(value) != 2):

            log.logger('La longitud de los datos no es correcta', debug.WAR)

            return(False)

        if not (isinstance(value[0], dict)) or not (isinstance(value[1], dict)):

            log.logger('El tipo de dato de la información del rook o los archivos de él, no es correcto', debug.WAR)

            return(False)

        (bot_id, bot_data) = tuple(value[0].items())[0]

        if not (isinstance(bot_data, dict)):

            log.logger('El tipo de dato de la información del rook no es correcto', debug.WAR)

            return(False)

        for _ in global_conf.keys_bot:

            if (key_check_in_dict.check(bot_data, _) == False):

                log.logger('No está definido la clave "{}" en la información del rook'.format(_), debug.WAR)

                return(False)

        profile_dir = '{}/{}/{}/{}'.format(getcwd(), global_conf.databases['database'], global_conf.databases['profiles'], bot_id)
        
        if not isdir(profile_dir):

            makedirs(profile_dir)

            log.logger('Creado, el directorio de perfil: "%s"' % (profile_dir), debug.PER)

        bot_data['profile'] = profile_dir
        bot_data['admins'] = real_extract_root_administrators.extract()
        
        if (bot_id in show_user_rooks.show()):

            log.logger('No se puede almacenar los datos de "%s" en el almacén, porque ya existe' % (bot_id), debug.WAR)

            return(False)

        log.logger('Almacenando datos de "%s" en el almacén ...' % (bot_id), debug.PER)

        if (wrap.add(bot_id, bot_data, username=bot_id, separate=True) == True):

            log.logger('Se almacenaron los datos de "%s" con éxito.' % (bot_id), debug.PER)

            if not (value[1] == {}):

                log.logger('Almacenando archivos ...', debug.INF)

                for filename, content_file in value[1].items():

                    filename = '%s/%s' % (profile_dir, basename(filename))

                    _bak_filename = rename_order.rename(filename)

                    if not (_bak_filename == False):

                        filename = _bak_filename

                    log.logger('Escribiendo: "%s" ...' % (filename), debug.PER)

                    try:

                        with open(filename, 'wb') as _obj:
                            
                            _obj.write(bytes_convert.convert(content_file))

                    except Exception as Except:

                        log.logger('Error escribiendo: {}. Excepción: {}'.format(filename, Except), debug.COM)

                    else:

                        log.logger('Escrito: "%s"' % (filename), debug.PER)

            return(True)

        else:
            
            log.logger('No se guardaron los datos en el almacén ... ')

            return(False)
    
    elif (key == 'resend'):

        if (len(value) != 2):

            log.logger('¡La longitud de los datos de los nodos no es correcta!', debug.WAR)
            return(False)

        (nodes, reply) = value

        if not (isinstance(reply, dict)):

            log.logger('¡El tipo de dato de la réplica de los datos no es correcto!', debug.WAR)
            return(False)

        if (len(reply) != 9):

            log.logger('¡La longitud de la réplica de los datos no es correcta!', debug.WAR)
            return(False)

        for _ in ['username', 'passphrase', 'uniqkey', 'iterations', 'security_number', 'decrement_number', 'chars', 'data', 'reply']:

            if (key_check_in_dict.check(reply, _) == False):

                log.logger('¡{}, No está incluida en la réplica!'.format(_), debug.WAR)
                return(False)

        if not (isinstance(nodes, dict)):

            log.logger('¡El tipo de dato de los nodos intermedios no es correcto!',debug.WAR)
            return(False) 
        
        if not (len(nodes) >= 2):

            log.logger('¡La longitud de los nodos no es correcta!', debug.WAR)
            return(False)

        check_nodes = [nodes[x] for x in nodes]

        if not ([] == [None for x in check_nodes if (len(x) != 3)]):

            log.logger('¡La longitud de un intermedio no es correcta!', debug.WAR)
            return(False)

        if (check_nodes[0][0] != 0):

            log.logger('¡No se puede enviar datos al nodo inicial!', debug.WAR)
            return(False)

        nodes_list = list(nodes)

        for _key, _value in nodes.items():

            (_init, _token, url_sum) = _value

            if not (isinstance(_init, int)):

                log.logger('¡El tipo de dato del indicador no es correcto!', debug.WAR)
                return(False)

            if (_init > 1) or (_init < 0):

                log.logger('¡El indicador no es correcto!', debug.WAR)
                return(False)

            if (_init == 1):

                nodes[_key][0] = 0
                break

        try:
            _key = simplycrypt.decrypt(real_secret_key, _key)

        except:
            
            log.logger('¡Error desencriptando la dirección URL del siguiente nodo!', debug.COM)
            return(False)

        if (len(url_sum) != 40):

            log.logger('¡La longitud de la suma de verificación de la URL no es correcta!', debug.WAR)
            return(False)

        end_point = nodes[nodes_list[-1]][-1]

        if not (url_sum == end_point):

            try:

                _token = simplycrypt.decrypt(real_secret_key, _token)

            except:

                log.logger('¡Error desencriptando el token de acceso de "{}"!'.format(_key), debug.WAR)
                return(False)

            log.logger('Enviando datos al siguiente nodo -> %s' % (_key), debug.PER)

            _data = connector.connect(_key, _token, 'resend', (nodes, reply), log, headers={'User-Agent':user_agent})

            log.logger('Re-enviado ...', debug.INF)

        else:

            log.logger('Re-enviando datos al nodo final -> "%s"' % (_key), debug.PER)

            try:

                _data = requests.post(_key, data=reply, timeout=global_conf.connector['timeout'], verify=False, headers={'User-Agent':user_agent}).content

            except Exception as Except:

                _data = str(Except)

                log.logger('Ocurrio una excepción: "%s"' % (Except), debug.WAR)

            else:

                log.logger('Los datos se re-enviaron satisfactoriamente ...', debug.INF)

        return(_data)

    elif (key == 'sendSOS'):

        log.logger('Envió un mensaje ...', debug.INF)
        log.logger('Gurdando ...', debug.INF)

        if not (isinstance(value, dict)):

            log.logger('¡No está siguiendo la especificación para almacenar mensajes!', debug.WAR)

            return(False)

        for _ in ['nickname', 'subject', 'message', 'files']:

            if (value.get(_) == None):

                log.logger('Falta definir: "%s"' % (_), debug.WAR)

                return(False)

        nickname = str(value['nickname'])
        subject = str(value['subject'][:98])
        message = str(value['message'])

        for _ in [nickname, subject, message]:

            if (_.strip() == ''):

                log.logger('¡Hay campos vacios!', debug.WAR)
                
                return(False)

        time_ = time()
        _files = value['files']
        _folder = None

        if not (isinstance(_files, list)):

            log.logger('¡El tipo de dato de los archivos no es correcto!', debug.WAR)

            return(False)

        _message_id = generate_uniqkey.generate()

        log.logger('ID: %s' % (_message_id), debug.PER)

        if not (_files == []):

            _folder = '%s/%s' % (public_files, _message_id)

            create_folder.create(_folder)

            for _ in _files:

                if (len(_) != 2):

                    log.logger('¡La longitud de la tupla no es correcta!', debug.WAR)

                    return(False)

                (_filename, _content) = _
                _filename = basename(str(_filename))

                log.logger('Envió un archivo: {}'.format(_filename), debug.PER)
                log.logger('Escribiendo ...', debug.INF)

                _save = '%s/%s' % (_folder, _filename)

                try:

                    with open(_save, 'wb') as _file_object:

                        _file_object.write(bytes_convert.convert(_content))

                except Exception as Except:

                    log.logger('Ocurrio una excepción al guardar a "{}". Excepción: {}'.format(_filename, Except))

                else:

                    log.logger('Escrito: %s' % (_save), debug.PER)

        if (wrap.add(_message_id, {'nickname':nickname, 'subject':subject, 'message':message, 'time':time_, 'profile':_folder}, agent=wrap.USE_MESSAGE) == True):

            log.logger('Guardado: %s' % (_message_id), debug.PER)

            return(True)

        else:

            log.logger('No se pudo guardar el mensaje: %s' % (_message_id), debug.WAR)

            return(False)

    else:

        return(False)
