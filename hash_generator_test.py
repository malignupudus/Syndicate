#!/usr/bin/env python3

while(1):

    try:

        from utils.sys_utils import no_terminate

    except KeyboardInterrupt:

        continue

    else:

        break

from time import time

from modules.Ciphers import db_hash
from modules.UI import argprogrammer

from utils.sys_utils import bell
from utils.sys_utils import clear

from conf import global_conf

hashing = global_conf.hashing

group_optionals = 'Opcionales'

parser = argprogrammer.Parser()
parser.set_head('''
       Syndicate Project - Saber la duración de la generación del Hash
       -----------------   -------------------------------------------''')

parser.add(['-h', '--help'], 'help', 'Mostrar la ayuda y sale', group=group_optionals)
parser.add(['-i', '--iterations'], 'iterations', 'Las iteraciones de procesamiento', type=int, default=hashing['iterations'])
parser.add(['-sn', '--security-number'], 'security_number', 'El número de seguridad', type=int, default=hashing['security_number'])
parser.add(['-sc', '--security-chars'], 'security_chars', 'Los caracteres de seguridad', default=hashing['chars'])
parser.add(['-dn', '--decrement-number'], 'decrement_number', 'El número de disminución', type=int, default=hashing['decrement_number'])
parser.add(['-s', '--string'], 'string', 'El texto a usar', require=True)
parser.add(['-H', '--hash'], 'hash', 'Comparar el hash con el string. Si no se usa se genera un hash en vez de comparar.', group=group_optionals)

args = parser.parse_args()

iterations = args.iterations
security_number = args.security_number
security_chars = args.security_chars
decrement_number = args.decrement_number
string = args.string
hash_ = args.hash

if (True in [True for x in [iterations, security_number, decrement_number] if (x == None)]):

    print('El tipo de dato de algún argumento no es correcto.')
    sys.exit(1)

try:

    if not (hash_):

        clear.clear()
        print(f'Generando: {string} = ?')
        _init_time = time()
        _hash = db_hash.hash(string, iterations, security_chars, security_number, decrement_number)
        clear.clear()
        bell.bell()
        print(f'Generado: {string} = {_hash}')
        print('Tiempo transcurrido: %.4fs' % (time()-_init_time))

    else:
        
        clear.clear()
        print(f'Comparando: {string} == {hash_} = ?')
        _init_time = time()
        _compare = db_hash.compare(string, hash_, iterations, security_chars, security_number, decrement_number)
        clear.clear()
        bell.bell()
        print(f'Comparado: {string} == {hash_} = {_compare}')
        print('Tiempo transcurrido: %.4fs' % (time()-_init_time))
        
except KeyboardInterrupt:

    pass

except Exception as Except:

    print('Ocurrio una excepción: {}'.format(Except))
