from subprocess import PIPE, STDOUT, Popen
from time import strftime
from hashlib import sha1
from inspect import isfunction
import shlex
import shelve

from utils.UI import debug
from utils.sys_utils import convert
from utils.sys_utils import my_addr, my_public_addr
from utils.Wrappers import wrap

from conf import global_conf

with shelve.open(wrap.getDB(wrap.USE_DEFEND), flag='n'):

    pass

def output_func(string, name):

    open("%s/%s" % (global_conf.databases['defend_logs'], name), 'a').write(str(string))
    print(str(string), end='')

def defend(command, address, bhost, bport, log):

    try:

        bhost = str(bhost)
        bport = str(bport)
        commands = [x.strip() for x in command.split(';') if (convert.convert_bool(x))]
        (host, port) = address

        # Bind

        (hostname, address) = my_addr.addr()

        for b_ in commands:

            cmd = b_

            try:

                limit = int(cmd.split(None, 1)[0])

            except:

                log('¡El limite debe ser un número!', debug.WAR)
                return

            cmd = ''.join(cmd.split(None, 1)[1:]).strip()

            for _key, _value in {'{ip}':host, '{port}':port, '{bhost}':bhost, '{bport}':bport, '{phost}':my_public_addr.addr}.items():

                if (cmd.find(_key) != -1):

                    if (isfunction(_value)):

                        _value = str(_value())

                    cmd = cmd.replace(_key, _value)

            uniqid = sha1(cmd.encode()).hexdigest()
            db_result = int(wrap.read(uniqid, 'limit', agent=wrap.USE_DEFEND))

            if not (limit == 0):

                if (db_result == 0):

                    if (wrap.add(uniqid, {'limit':1}, agent=wrap.USE_DEFEND) == False):

                        log('Lo siento no se pudo agregar un limite al almacén para la siguiente defensa: "{}"'.format(cmd), debug.COM)

                        return

                elif (db_result >= limit):

                    return

                else:

                    if (wrap.write(uniqid, 'limit', db_result+1, agent=wrap.USE_DEFEND) == False):

                        log('No se pudo actualizar el limite en el almacén para la siguiente defensa: "{}"'.format(cmd), debug.COM)

                        return

            parsed = shlex.split(cmd)

            try:

                result = Popen(parsed, stdout=PIPE, stderr=STDOUT, universal_newlines=True)

            except FileNotFoundError:

                log('El ejecutable: "{}" no se puede ejecutar porque no existe ...'.format(parsed[0]), debug.WAR)

                return
            
            except Exception as Except:

                log('Ocurrio un error desconocido al ejecutar el siguiente comando: "{}". Excepción: "{}"'.format(cmd, Except), debug.WAR)

                return
            
            pid = result.pid
            name = "%s.%s.%s.log" % (host, uniqid, strftime('%d-%m-%Y'))

            output_func('\033[1;37m***\033[0m \033[1;32mIniciando\033[0m: \033[1;33mID\033[0m:\033[1;37m%s\033[0m: \033[1;33mpid\033[0m:\033[1;37m%d\033[0m \033[1;34m~\033[0m \033[1;33mfile\033[0m:\033[1;37m%s ***\033[0m\n' % (uniqid, pid, name), name)
            
            with result as _process:

                for c_ in _process.stdout:

                    output_func("\033[1;34m%s\033[0m: \033[1m%s\033[0m\n" % (parsed[0], c_.rstrip()), name)
            
            output_func('\033[1;37m***\033[0m \033[1;32mFinalizado\033[0m: \033[1;33mID\033[0m:\033[1;37m%s\033[0m: \033[1;33mpid\033[0m:\033[1;37m%d\033[0m \033[1;34m~\033[0m \033[1;33mfile\033[0m:\033[1;37m%s ***\033[0m\n' % (uniqid, pid, name), name)

    except Exception as Except:

        log('Excepción ejecutando la defensa: {}'.format(Except), debug.COM)
