#!/usr/bin/env python3

while(1):

    try:

        from utils.sys_utils import no_terminate

    except KeyboardInterrupt:

        continue

    else:

        break

from os.path import isfile

from modules.UI import argprogrammer
from modules.UI import rename_order
from modules.Ciphers import obfuscate_passwd

from utils.sys_utils import bytes_convert
from utils.Wrappers import wrap_file

from conf import global_conf

verbose = lambda string: print(f'[DECRYPT] - {string}')

default_iterations = global_conf.hashing['iterations']
default_security_chars = global_conf.hashing['chars']
default_security_number = global_conf.hashing['security_number']
default_decrement_number = global_conf.hashing['decrement_number']

optionals = 'Opcionales'

parser = argprogrammer.Parser()

parser.set_head('''
       Syndicate Project - Desencriptar archivos almacenados
       -----------------   ---------------------------------''')

parser.add(['-h', '--help'], 'help', 'Mostrar la ayuda y sale', group=optionals)
parser.add(['-no-rename'], 'no_rename', 'Úselo para no renombrar el archivo en caso de existir', type=bool, action=True, group=optionals)
parser.add(['-p', '--password'], 'password', 'Contraseña para desencriptar', require=True)
parser.add(['-i', '--iterations'], 'iterations', 'El número de iteraciones', default=default_iterations, group=optionals, type=int)
parser.add(['-sn', '--security-number'], 'security_number', 'El número de seguridad', default=default_security_number, group=optionals, type=int)
parser.add(['-dn', '--decrement-number'], 'decrement_number', 'El número de disminución', default=default_decrement_number, group=optionals, type=int)
parser.add(['-sc', '--security-chars'], 'security_chars', 'Los caracteres de seguridad', default=default_security_chars, group=optionals)
parser.add(['-I', '--input'], 'input', 'El fichero de entrada y encriptado', require=True)
parser.add(['-o', '--output'], 'output', 'El fichero de salida que será desencriptado', require=True)

args = parser.parse_args()

iterations = str(args.iterations)
security_number = str(args.security_number)
decrement_number = str(args.decrement_number)
security_chars = args.security_chars
password = obfuscate_passwd.obfuscate(args.password+security_chars+iterations+security_number+decrement_number)
input_ = args.input
output = args.output
no_rename = args.no_rename

if (isfile(input_)):

    try:

        result = wrap_file.wrap(input_, password)

        if (result == False):

            verbose('Error desencriptado a: "{}"'.format(input_))

        else:

            _bak_output = rename_order.rename(output)

            if not (_bak_output == False) and not (no_rename == True):

                output = _bak_output

            with open(output, 'wb') as _file_object:

                _file_object.write(bytes_convert.convert(result))

            verbose('Desencriptado: {} -> {}'.format(input_, output))

    except Exception as Except:

        verbose('Ocurrio una excepción desconocida: {}'.format(Except))

else:

    verbose('El archivo "{}" no existe...'.format(input_))
