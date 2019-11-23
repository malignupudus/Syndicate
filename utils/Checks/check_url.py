# -*- coding: UTF-8 -*-

import sys

from utils.UI import debug
if (sys.version_info.major == 3):
    from urllib.parse import urlparse
elif (sys.version_info.major == 2):
    from urlparse import urlparse
else:
    raise NotImplementedError('No se detecto una versión de Python válida')

def check(url, log, verbose=True):

    error = False
    url = str(url)
    if (url.strip() == ''):
        if (verbose == True):
            log.logger('Una dirección URL válida no está vacia ...', debug.WAR)
        return(True)
    url = urlparse(url)
    
    scheme = url.scheme

    if (scheme == ''):

        error = True
        if (verbose == True):
            log.logger('No se definio un esquema o no es válido para "{}"'.format(url.geturl()), debug.WAR)

    else:

        if not (scheme == 'http') and not (scheme == 'https'):

            error = True
            if (verbose == True):
                log.logger('{}, No es un esquema válido para "{}"'.format(scheme, url.geturl()), debug.WAR)

        else:

            if (verbose == True): 
                log.logger('{}, Es un esquema válido'.format(scheme), debug.PER)

            if (url.hostname == None):

                error = True
                if (verbose == True):
                    log.logger('La dirección es inválida', debug.WAR)

            else:

                if (url.hostname.strip() == ''):

                    error = True
                    if (verbose == True):
                        log.logger('La dirección está vacia', debug.WAR)

                else:

                    if (verbose == True):
                        log.logger('{}, Es una dirección válida'.format(url.hostname), debug.PER)

                    try:

                        url.port

                    except ValueError:

                        error = True
                        if (verbose == True):
                            log.logger('El puerto de "{}" es inválido'.format(url.geturl()), debug.WAR)

                    else:

                        if (verbose == True):
                            log.logger('{}, Es un puerto válido'.format(url.port), debug.PER)

                        if (url.path == ''):
                            if (verbose == True):
                                log.logger('No se escribio una ruta. Se tomará cómo: \'/\'')

    return(error)
