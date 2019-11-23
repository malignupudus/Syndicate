from utils.UI import debug
from utils.sys_utils import bytes_convert
from modules.UI import rename_order
from os.path import basename, dirname

from conf import global_conf

profile = '{}/{}'.format(global_conf.databases['database'], global_conf.databases['profiles'])

def main(result, log, function, bot_id):

    if (function == 'copytree') or (function == 'copy') or (function == 'detect'):

        if (isinstance(result, tuple)):

            filename = basename(str(result[0])).strip()

            if not (filename == ''):

                filename = '{}/{}/{}'.format(profile, bot_id, filename)

                bak_filename = rename_order.rename(filename)

                if not (bak_filename == False):

                    filename = bak_filename

                with open(filename, 'wb') as file_object:

                    file_object.write(bytes_convert.convert(result[1]))

                log.logger('Guardado: {}'.format(filename), debug.PER)

            else:

                log.logger('El nombre del archivo es inválido', debug.WAR)

        else:

            log.logger('El tipo de dato del resultados de los archivos capturados no es correcto', debug.WAR)

    elif (function == 'init'):

        log.logger('Capturado: {} => {}'.format(dirname(result[0]), basename(result[0])), debug.PER)
        
    else:

        log.logger('{} no es una función válida para este complemento'.format(function), debug.WAR)
