from os import makedirs
from os.path import isdir, dirname, basename

from utils.Wrappers import wrap
from utils.UI import debug
from utils.sys_utils import pos_convert
from utils.Extracts.extract_ips import _extract

from modules.Ciphers import db_hash

from time import time
from yaml import load

from conf import global_conf

hashing_length = global_conf.hashing_length
_server_error_message = 'Hubo un error interno analizando el metodo de denegación ...'

def check(passphrase, bot_id, log, address, max_retry, retry_seconds, denied_method, rdns, iterations, chars, decrement_number, security_number):

    passphrase = str(passphrase)
    bot_id = str(bot_id)
    chars = str(chars)

    log1 = debug.log(address=address, username='%s' % (bot_id), log=log, rdns=rdns) if not (bot_id == '') else debug.log(address=address, username='null', log=log, rdns=rdns)
    log1.logger('Verificando las credenciales del rook...', debug.INF)

    try:

        iterations = pos_convert.convert(int(iterations))
        decrement_number = pos_convert.convert(int(decrement_number))
        security_number = pos_convert.convert(int(security_number))

    except ValueError:

        log1.logger('No se introdujo un tipo de dato correcto en un parámetro ...', debug.COM)

        return(False)

    else:

        if (len(chars) > hashing_length['chars']):

            log1.logger('El número de los caracteres (%d) sobrepasa el limite (%d)' % (len(chars), hashing_length['chars']), debug.WAR)

            return(False)

        elif (iterations > hashing_length['iterations']):

            log1.logger('El número de iteraciones (%d) del cliente sobrepasa el limite (%d)' % (iterations, hashing_length['iterations']), debug.WAR)

            return(False)

        elif (decrement_number > hashing_length['decrement_number']):

            log1.logger('El número de disminución (%d) del cliente sobrepasa el limite (%d)' % (decrement_number, hashing_length['decrement_number']), debug.WAR)

            return(False)

        elif (security_number > hashing_length['security_number']):

            log1.logger('El número de seguridad (%d) del cliente sobrepasa el limite (%d)' % (security_number, hashing_length['security_number']), debug.WAR)

            return(False)

        else:

            log1.logger('¡Los datos corresponden con las limitaciones asignadas!', debug.INF)

    denied_method = denied_method.lower()
    address_string = address[0]
    spam_agent = wrap.USE_SPAM

    db_username = wrap.read(bot_id, 'username', separate=True)
    db_passphrase = wrap.read(bot_id, 'passphrase', separate=True)

    if (db_username == False) or (db_passphrase == False):
        
        log1.logger('No se pudo obtener el Nombre de usuario o frase de contraseña', debug.WAR)

        return(False)
    
    log1.logger('Verificando la existencia del bot en el almacén de los intentos fallidos ...', debug.INF)
    
    if (bot_id in wrap.getall(agent=wrap.USE_SPAM)):

        log1.logger('¡Correcto, el bot existe!', debug.INF)

    else:

        log1.logger('El bot no existe, almacenando un espacio en el almacén ...', debug.WAR)

        if (wrap.add(bot_id, {'retry':0, 'IP':[], 'max_time':None}, agent=wrap.USE_SPAM) == True):

            log1.logger('Se agrego el bot al almacén', debug.INF)

        else:

            log1.logger('Hubo un error agregando los datos al almacén. No se puede seguir operando', debug.COM)

            return(False)

    if (denied_method == 'forretry'):

        _method = wrap.read(bot_id, 'retry', agent=spam_agent)

    elif (denied_method == 'forip'):

        try:

            _method = _extract(wrap.read(bot_id, 'IP', agent=spam_agent), address_string)[-1][2]

        except (TypeError, IndexError):

            _method = 0

    else:

        log1.logger(_server_error_message, debug.INF)

        return(False)

    if (_method >= max_retry):

        if (denied_method == 'forip'):

            try:

                _result = _extract(wrap.read(bot_id, 'IP', agent=spam_agent), address_string)[-1][1]
            
            except (TypeError, IndexError):

                _trans = 0

            else:
            
                _trans = float(_result)

        elif (denied_method == 'forretry'):

            _trans = float(wrap.read(bot_id, 'max_time', agent=spam_agent)) 

        if not (time() >= _trans):

            log1.logger('¡Aún no ha transcurrido el tiempo maximo registrado!', debug.WAR)

        else:

            log1.logger('Tiempo transcurrido con exito. Reiniciando valores ...', debug.INF)

            if (wrap.delete(bot_id, agent=spam_agent) == True):

                log1.logger('Correcto, se reiniciaron los valores con exito', debug.INF)

            else:

                log1.logger('Hubo un error reiniciando los valores ...', debug.COM)

                return(False)

    if (denied_method == 'forretry'):

        if (wrap.read(bot_id, 'retry', agent=spam_agent) >= max_retry):

            log1.logger('Los intentos fallidos de inicio de sesión han llegado al maximo configurado ...', debug.WAR)

            return(False)

    elif (denied_method == 'forip'):

        try:

            _result = _extract(wrap.read(bot_id, 'IP', agent=spam_agent), address_string)[-1][2]

        except (TypeError, IndexError):

            _result = 0

        if (_result >= max_retry):
            
            log1.logger('Los intentos de inicios de sesión por parte de la dirección IP "%s" han llegado al maximo configurado ...' % (address_string), debug.WAR)

            return(False) 

    else:

        log1.logger(_server_error_message, debug.WAR)

        return(False)

    log = debug.log(address=address, username='%s:(%s)' % (db_username, bot_id), log=log, rdns=rdns)

    if (db_hash.compare(passphrase, db_passphrase, iterations, chars, security_number, decrement_number) == True):

        log.logger('Credenciales correctas', debug.INF)

        return(True)

    else:

        log.logger('¡Credenciales incorrectas!', debug.COM)

        result = []
        result1 = []
        result2 = []

        _max_time = time()+retry_seconds

        if (denied_method == 'forretry'):

            _retry = int(wrap.read(bot_id, 'retry', agent=spam_agent))+1

            try:
                
                _retry_for_ip = int(_extract(wrap.read(bot_id, 'IP', agent=spam_agent), address_string)[-1][2])
            
            except (TypeError, IndexError):
                
                _retry_for_ip = 0

            result2.append(wrap.write(bot_id, 'max_time', _max_time, agent=spam_agent))
            result2.append(wrap.write(bot_id, 'retry', _retry, agent=spam_agent))

            if (False in result2):

                log.logger('Ocurrio un error interno. No se puede remplazar el valor de intentos fallidos', debug.COM)

            return(False)

        else:

            _retry = int(wrap.read(bot_id, 'retry', agent=spam_agent))
            
            try:
                
                _retry_for_ip = int(_extract(wrap.read(bot_id, 'IP', agent=spam_agent), address_string)[-1][2])+1
            
            except (TypeError, IndexError):
                
                _retry_for_ip = 1 

        try:

            wrap.read(bot_id, 'IP', agent=wrap.USE_SPAM)[-1][0]
        
        except (TypeError, IndexError):

            result1.append(False)
        
        result1.append(wrap.write(bot_id, 'IP', _max_time, agent=spam_agent, target=wrap.TARGET_SUBINDEX_UPDATE, array_subindex=(-1, 1)))
        result1.append(wrap.write(bot_id, 'IP', _retry_for_ip, agent=spam_agent, target=wrap.TARGET_SUBINDEX_UPDATE, array_subindex=(-1, 2)))

        if (False in result1):
            
            result.append(wrap.write(bot_id, 'IP', [address_string, _max_time, _retry_for_ip], agent=spam_agent))

            if (False in result):

                log.logger('¡No se pudo agregar otro ingreso al almacén! ...', debug.COM)

                return(False)

        _bak_retry = _retry if (denied_method == 'forretry') else _retry_for_ip

        log.logger('Total de intentos fallidos registrados: "%d"' % (_bak_retry), debug.WAR)

        return(False)
