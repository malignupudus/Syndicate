from time import strftime, time

from utils.Wrappers import wrap
from utils.UI import debug
from utils.sys_utils import pos_convert
from utils.Extracts.extract_ips import _extract
from utils.sys_utils import convert

from modules.Ciphers import db_hash

from conf import global_conf

hashing_length = global_conf.hashing_length
_server_error_message = 'Hubo un error interno analizando el metodo de denegación ...'

def check(username, passphrase, uniqkey, recover, log, address, max_retry, retry_seconds, denied_method, iterations, chars, decrement_number, security_number):

    log.logger('Verificando credenciales del administrador...', debug.INF)

    chars = str(chars)

    try:

        iterations = pos_convert.convert(int(iterations))
        decrement_number = pos_convert.convert(int(decrement_number))
        security_number = pos_convert.convert(int(security_number))

    except ValueError:

        log.logger('No se introdujo un tipo de dato correcto en un parámetro ...', debug.COM)

        return(False)

    else:

        if (len(chars) > hashing_length['chars']):

            log.logger('El número de los caracteres (%d) sobrepasa el limite (%d)' % (len(chars), hashing_length['chars']), debug.WAR)

            return(False)

        elif (iterations > hashing_length['iterations']):

            log.logger('El número de iteraciones (%d) del cliente sobrepasa el limite (%d)' % (iterations, hashing_length['iterations']), debug.WAR)

            return(False)

        elif (decrement_number > hashing_length['decrement_number']):

            log.logger('El número de disminución (%d) del cliente sobrepasa el limite (%d)' % (decrement_number, hashing_length['decrement_number']), debug.WAR)

            return(False)

        elif (security_number > hashing_length['security_number']):

            log.logger('El número de seguridad (%d) del cliente sobrepasa el limite (%d)' % (security_number, hashing_length['security_number']), debug.WAR)

            return(False)

        else:

            log.logger('¡Los datos corresponden con las limitaciones asignadas!', debug.INF)

    denied_method = denied_method.lower()

    agent = wrap.USE_ADMIN
    address_string = address[0]
    spam_agent = wrap.USE_SPAM_FOR_ADMINS

    username = str(username)
    passphrase = str(passphrase)
    uniqkey = str(uniqkey)

    db_passphrase = wrap.read(username, 'passphrase', agent=agent, separate=True)
    
    new_uniqkey = False

    if (uniqkey.lower().count(':') == 1):

        log.logger('Parece que quiere acceder con la anterior clave única ...', debug.WAR)

        real_uniqkey = uniqkey.split(':')
        
        try:

            if not (real_uniqkey[0].lower() == 'recover'):
                
                log.logger('¡Uso un formato invalído!', debug.COM)

                return(False)

            uniqkey = real_uniqkey[1]

        except IndexError:
            
            log.logger('No tiene datos suficientes para comprobar que desea usar la última clave única', debug.COM)

            return(False)

    else:

        real_uniqkey = False

    if not (real_uniqkey == False):
        
        log.logger('Quiere usar la última clave para acceder y tiene un formato correcto', debug.INF)
        
        if (recover == True):

            log.logger('Va a tratar de acceder con la última clave única', debug.WAR)

            db_uniqkey = wrap.read(username, 'lastUniqkey', agent=agent, separate=True)

        else:

            log.logger('¡No está permitido usar la última clave única!', debug.INF)

            new_uniqkey = True

    else:

        new_uniqkey = True

    if (new_uniqkey == True):

        log.logger('Usando la clave única actual', debug.INF)

        db_uniqkey = wrap.read(username, 'uniqkey', agent=agent, separate=True)

    if (db_passphrase == False) or (db_uniqkey == False):
        
        log.logger('No se pudo obtener la clave única o la frase de contraseña', debug.WAR)

        return(False)

    log.logger('Verificando la existencia del administrador en el almacén de los intentos fallidos ...', debug.INF)
    
    if (username in wrap.getall(agent=spam_agent)):

        log.logger('¡Correcto, el administrador existe!', debug.INF)

    else:

        log.logger('El administrador no existe, almacenando un espacio en el almacén ...', debug.WAR)

        if (wrap.add(username, {'retry':0, 'IP':[], 'max_time':None}, agent=spam_agent) == True):

            log.logger('Se agregó el administrador al almacén', debug.INF)

        else:

            log.logger('Hubo un error agregando los datos al almacén. No se puede seguir operando', debug.COM)

            return(False)

    if (denied_method == 'forretry'):

        _method = wrap.read(username, 'retry', agent=spam_agent)

    elif (denied_method == 'forip'):

        try:

            _method = _extract(wrap.read(username, 'IP', agent=spam_agent), address_string)[-1][2]

        except (TypeError, IndexError):

            _method = 0

    else:

        log.logger(_server_error_message, debug.INF)

        return(False)

    if (_method >= max_retry):

        if (denied_method == 'forip'):

            try:

                _result = _extract(wrap.read(username, 'IP', agent=spam_agent), address_string)[-1][1]
            
            except (TypeError, IndexError):

                _trans = 0

            else:
            
                _trans = float(_result)

        elif (denied_method == 'forretry'):

            _trans = float(wrap.read(username, 'max_time', agent=spam_agent)) 

        if not (time() >= _trans):

            log.logger('¡Aún no ha transcurrido el tiempo maximo registrado!', debug.WAR)

        else:

            log.logger('Tiempo transcurrido con exito. Reiniciando valores ...', debug.INF)

            if (wrap.delete(username, agent=spam_agent) == True):

                log.logger('Correcto, se reiniciaron los valores con exito', debug.INF)

            else:

                log.logger('Hubo un error reiniciando los valores ...', debug.COM)

                return(False)

    if (denied_method == 'forretry'):

        if (wrap.read(username, 'retry', agent=spam_agent) >= max_retry):

            log.logger('Los intentos fallidos de inicio de sesión han llegado al maximo configurado ...', debug.WAR)

            return(False)

    elif (denied_method == 'forip'):

        try:

            _result = _extract(wrap.read(username, 'IP', agent=spam_agent), address_string)[-1][2]

        except (TypeError, IndexError):

            _result = 0

        if (_result >= max_retry):
            
            log.logger('Los intentos de inicios de sesión por parte de la dirección IP "%s" han llegado al maximo configurado ...' % (address_string), debug.WAR)

            return(False) 

    else:

        log.logger(_server_error_message, debug.WAR)

        return(False)

    if (db_uniqkey == uniqkey) and (db_hash.compare(passphrase, db_passphrase, iterations, chars, security_number, decrement_number) == True):
        
        log.logger('¡La frase de contraseña o la clave única es correcta!', debug.PER)

        wrap.write(username, 'lastLogin', strftime("%H:%M:%S&%d/%m/%Y"), agent=agent, separate=True)
        wrap.write(username, 'lastUniqkey', db_uniqkey, agent=agent, separate=True)
        
        return(True)
    
    else:

        log.logger('La frase de contraseña o la clave única no es correcta ...', debug.COM)

        result = []
        result1 = []
        result2 = []

        _max_time = time()+retry_seconds

        if (denied_method == 'forretry'):

            _retry = int(wrap.read(username, 'retry', agent=spam_agent))+1

            try:
                
                _retry_for_ip = int(_extract(wrap.read(username, 'IP', agent=spam_agent), address_string)[-1][2])
            
            except (TypeError, IndexError):
                
                _retry_for_ip = 0

            result2.append(wrap.write(username, 'max_time', _max_time, agent=spam_agent))
            result2.append(wrap.write(username, 'retry', _retry, agent=spam_agent))

            if (False in result2):

                log.logger('Ocurrio un error interno. no se puede remplazar el valor de intentos fallidos', debug.COM)

            return(False)

        else:

            _retry = int(wrap.read(username, 'retry', agent=spam_agent))
            
            try:
                
                _retry_for_ip = int(_extract(wrap.read(username, 'IP', agent=spam_agent), address_string)[-1][2])+1
            
            except (TypeError, IndexError):
                
                _retry_for_ip = 1 

        try:

            wrap.read(username, 'IP', agent=spam_agent)[-1][0]
        
        except (TypeError, IndexError):

            result1.append(False)
        
        result1.append(wrap.write(username, 'IP', _max_time, agent=spam_agent, target=wrap.TARGET_SUBINDEX_UPDATE, array_subindex=(-1, 1)))
        result1.append(wrap.write(username, 'IP', _retry_for_ip, agent=spam_agent, target=wrap.TARGET_SUBINDEX_UPDATE, array_subindex=(-1, 2)))

        if (False in result1):
            
            result.append(wrap.write(username, 'IP', [address_string, _max_time, _retry_for_ip], agent=spam_agent))

            if (False in result):

                log.logger('¡No se pudo agregar otro ingreso al almacén! ...', debug.COM)

                return(False)

        _bak_retry = _retry if (denied_method == 'forretry') else _retry_for_ip

        log.logger('Total de intentos fallidos registrados: "%d"' % (_bak_retry), debug.WAR)

        return(False)
