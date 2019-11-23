import requests
from hashlib import sha1
from urllib3 import disable_warnings
from yaml import load, dump

from utils.Ciphers import simplycrypt
from utils.Wrappers import wrap
from utils.UI import debug

from conf import global_conf

disable_warnings()

def connect(url, token, command, data, log, return_exception=True, headers=None):

    if not (isinstance(url, str)):

        log.logger('El tipo de dato de la URL no es correcto', debug.WAR)
        return(False)

    if not (isinstance(url, str)):

        log.logger('El tipo de dato del token de acceso no es correcto', debug.WAR)
        return(False)

    share = {}
    share['token'] = token

    log.logger('Usando el acceso público de "%s"' % (url), debug.INF)

    try:

        try:

            pubKey = wrap.getall(wrap.USE_TMP)[sha1(url.encode()).hexdigest()]['pub_key']

        except KeyError:

            log.logger('No se encontro la clave pública en el almacén ... Descargandola de: "%s"' % (url), debug.PER)

            share['command'] = ('getPubKey', None)

            pubKey = simplycrypt.decrypt(token, requests.post(url=url, data=simplycrypt.encrypt(token, share), headers=headers, verify=False, timeout=global_conf.connector['timeout']).content)

            if (pubKey == False):

                log.logger('Hubo un error extrayendo la clave pública de: "%s"' % (url), debug.COM)

                return(False)

            log.logger('Almacenando la clave pública en el almacén ...', debug.INF)

            if (wrap.add(sha1(url.encode()).hexdigest(), {'pub_key':pubKey}, agent=wrap.USE_TMP) == True):

                log.logger('La clave pública se guardó en el almacén', debug.INF)

            else:

                log.logger('Error guardando la clave pública en el almacén  ...', debug.WAR)

                return(False)

        log.logger('Enviando "%s" a "%s" ...' % (command, url), debug.PER)

        share['command'] = (command, data)

        content = simplycrypt.decrypt(token, requests.post(url=url, data=simplycrypt.encrypt(token, share), headers=headers, verify=False, timeout=global_conf.connector['timeout']).content)

        log.logger('Contenido enviado con éxito a: "%s"' % (url), debug.PER)

        return(content)

    except Exception as Except:

        log.logger('Ocurrio un error conectando a un acceso público. Excepción: "%s"' % (Except), debug.WAR)

        if (return_exception == True):

            return(str(Except))

        else:

            return(False)
