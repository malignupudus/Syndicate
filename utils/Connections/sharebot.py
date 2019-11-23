import os

from utils.Wrappers import wrap
from utils.UI import debug
from utils.Connections import connector

from conf import global_conf

def share(bot_id, secondaryServerAddr, token, headers, shareFiles, log):
    
    files = {}
    bot_data = wrap.read(bot_id, separate=True)
    bot_data['admins'] = []
    bot_data['profile'] = None
    bot_data['servers'] = []

    if (bot_data == False): 

        return(False, log.logger('No se obtuvieron datos de: "{}"'.format(bot_id), debug.WAR))

    try:

        log.logger('Enviando el siguiente rook: "%s" a "%s" ...' % (bot_id, secondaryServerAddr), debug.WAR)

        if (shareFiles == True):

            log.logger('Se decidio compartir los archivos ...', debug.INF)

            _directory = '%s/%s/%s' % (global_conf.databases['database'], global_conf.databases['profiles'], bot_id)

            if (os.path.isdir(_directory)):

                log.logger('Indexando ...', debug.INF)

                _files = os.listdir(_directory)
                
                if (_files == []):

                    log.logger('Aún no hay archivos para enviar ...', debug.WAR)

                else:

                    for _ in _files:

                        _file = '%s/%s' % (_directory, _)

                        if (os.path.isfile(_file)):

                            log.logger('Leyendo: "%s" ...' % (_file), debug.WAR)

                            with open(_file, 'rb') as _obj:

                                files[_file] = _obj.read()

                            log.logger('Incluido: "%s"' % (_file), debug.PER)

                        else:

                            log.logger('%s, ¡Es un directorio!' % (_file), debug.WAR)

            else:

                return(False, log.logger('No existe el directorio de perfil de "{}" o es un archivo ...'.format(bot_id), debug.WAR))

        response = connector.connect(secondaryServerAddr, token, 'saveData', ({bot_id:bot_data}, files), log, return_exception=False, headers=headers)

        if not (response == False):

            log.logger('Se envio con éxito a "%s"' % (bot_id), debug.INF)

            return(True)

        else: 

            return(False, log.logger('Hubo un error enviando los datos de "{}"'.format(bot_id), debug.WAR))

    except Exception as Except: 

        return(False, log.logger('Ocurrio una excepción: "{}"'.format(Except), debug.COM))
