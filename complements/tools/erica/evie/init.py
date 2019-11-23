from utils.UI import evieModule
from utils.UI import debug

def main(result, log, bot_id):

    if (isinstance(result, tuple)):

        if (len(result) == 2):

            wrap = evieModule.CreateDatabase('erica')
            (success, pass_to_hash) = result

            if (success == True):

                log.logger('Hash crackeado => {}'.format(pass_to_hash), debug.PER)

            else:

                log.logger('El hash no se pudo crackear => {}'.format(pass_to_hash), debug.WAR)

            log.logger('Almacenando ...', debug.INF)

            if (bot_id in list(wrap.getall().keys())):

                if (wrap.write(bot_id, 'hash', result) == True):

                    log.logger('¡Hash almacenado!', debug.INF)

                else:

                    log.logger('¡Error almacenando el Hash!', debug.COM)

            else:

                if (wrap.add(bot_id, {'hash':[result]}) == True):

                    log.logger('¡Hash almacenado por primera vez!', debug.INF)

                else:

                    log.logger('¡Error almacenando el Hash!', debug.COM)

        else:

            log.logger('¡La longitud del resultado no es correcta!', debug.WAR)

    else:

        log.logger('El tipo de dato de los resultados del crackeo no es correcto ...', debug.WAR)
