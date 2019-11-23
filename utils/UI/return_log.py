from utils.UI import debug

def imprint(log, method, response):

    response = int(response)

    _custom_format = '{0} ({1}): [%s]'.format(method, response)

    if (response == 404):

        log.logger(_custom_format % ('¡Posible escaneo!'), debug.WAR)

    elif (response == 511):

        log.logger(_custom_format % ('Requiere de authenticación para continuar!'), debug.WAR)

    elif (response == 400):

        log.logger('El cliente no esta siguiendo el estandar requerido!', debug.COM)
    
    elif (response == 411):

        log.logger(_custom_format % ('Error en la sintaxis, requiere de la clave en el encabezado "Content-Length"'), debug.WAR)

    elif (response == 403):

        log.logger(_custom_format % ('¡ACCESO DENEGADO!'), debug.COM)

    elif (response == 401):
                
        log.logger(_custom_format % ('Esta intentando acceder al login falso'), debug.INF)

    else:
        
        log.logger('%s (%s)' % (method, response), debug.INF)
