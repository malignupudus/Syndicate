from subprocess import PIPE, STDOUT, Popen
from time import strftime
from hashlib import sha1
import shlex
import copy
import shelve

from utils.sys_utils import my_addr, my_public_addr
from utils.Wrappers import wrap
from utils.Ciphers import generate_uniqkey

with shelve.open(wrap.getDB(wrap.USE_DEFEND), flag='n'):

    pass

def output_func(string, name):

    open("defend/logs/%s" % (name), 'a').write(str(string))
    print(str(string), end='')

def defend(command, address, bport):

    bport = str(bport)
    commands = command.split(';')
    (host, port) = address.split('#')

    # Bind

    (hostname, address) = my_addr.addr()

    for b_ in commands:

        cmd = copy.copy(b_)

        for _key, _value in {'{ip}':host, '{port}':port, '{bhost}':address, '{bport}':bport, '{phost}':my_public_addr.addr}.items():

            try:

                _value.__name__

            except:

                cmd = cmd.replace(_key, str(_value))

            else:

                cmd = cmd.replace(_key, str(_value()))

        limit = int(cmd.split('{limit}')[0])
        cmd = cmd.replace('%d{limit}' % (limit), '')
        program = cmd.split('{program}')[0]
        cmd = cmd.replace('{program}','')
        
        uniqid = sha1(cmd.encode()).hexdigest()
        db_result = int(wrap.read(uniqid, 'limit', agent=wrap.USE_DEFEND))

        if not (limit == 0):

            if (db_result == 0):

                if (wrap.add(uniqid, {'limit':1}, agent=wrap.USE_DEFEND) == False):

                    print('Lo siento no se pudo agregar un limite al almacén para la siguiente defensa: "%s"' % (cmd))

                    return

            elif (db_result >= limit):

                return

            else:

                if (wrap.write(uniqid, 'limit', db_result+1, agent=wrap.USE_DEFEND) == False):

                    print('No se pudo actualizar el limite en el almacén para la siguiente defensa: "%s"' % (cmd))

                    return

        uniqkey = generate_uniqkey.generate()
        args = shlex.split(cmd)

        try:

            result = Popen(args, stdout=PIPE, stderr=STDOUT, universal_newlines=True)

        except FileNotFoundError:

            print('El ejecutable: "%s" no se puede ejecutar porque existe ...' % (args[0]))

            return
        
        except Exception as Except:

            print('Ocurrio un error desconocido al ejecutar el siguiente comando: "%s". Excepción: "%s"' % (cmd, Except))

            return
        
        pid = result.pid
        name = "pid-%d-%s.%s.%s.log" % (pid, host, uniqkey, strftime('%d-%m-%Y'))

        output_func('\033[1;37m***\033[0m \033[1;32mIniciando\033[0m: \033[1;33mID\033[0m:\033[1;37m%s\033[0m: \033[1;33mpid\033[0m:\033[1;37m%d\033[0m \033[1;34m~\033[0m \033[1;33mfile\033[0m:\033[1;37m%s ***\033[0m\n' % (uniqkey, pid, name), name)
        
        with result as _process:

            for c_ in _process.stdout:

                output_func("\033[1;34m%s\033[0m: \033[1m%s\033[0m\n" % (program, c_.rstrip()), name)
        
        output_func('\033[1;37m***\033[0m \033[1;32mFinalizado\033[0m: \033[1;33mID\033[0m:\033[1;37m%s\033[0m: \033[1;33mpid\033[0m:\033[1;37m%d\033[0m \033[1;34m~\033[0m \033[1;33mfile\033[0m:\033[1;37m%s ***\033[0m\n' % (uniqkey, pid, name), name)
