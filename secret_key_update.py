#!/usr/bin/env python3

while(1):

    try:

        from utils.sys_utils import no_terminate

    except KeyboardInterrupt:

        continue

    else:

        break

from modules.UI import argprogrammer

from utils.sys_utils import separate_space
from utils.Wrappers import wrap
from utils.Ciphers import generate_uniqkey

parser = argprogrammer.Parser()

parser.set_head('''
       Syndicate Project - Actualizar la clave secreta
       -----------------   ---------------------------''')

parser.add(['-h', '--help'], 'help', 'Mostrar la ayuda que estás viendo')
parser.add(['-l', '--long'], 'long', 'La longitud de la clave secreta. Debe ser mayor o igual qué "32".', type=int, default=32)

args = parser.parse_args()

long_ = args.long

secret_key = wrap.read('secret_key', 'secret_key', wrap.USE_SECRET_KEY)

def _print(string):

    print(f'[SECRET-KEY]: {string}') 

if (long_ == None):
    
    if not (secret_key == False):

        _print('Clave secreta: %s' % (secret_key))

    else:

        _print('¡Hay un error leyendo la clave secreta!')

else:

    if (long_ >= 32):

        _print('Actualizando clave secreta ...')
        
        secret_key = separate_space.separate(generate_uniqkey.generate(long_))

        if (wrap.add('secret_key', {'secret_key':secret_key}, agent=wrap.USE_SECRET_KEY) == True):

            _print('Clave secreta actualizada: "%s"' % (secret_key))

        else:

            _print('Error actualizando la clave secreta ...')

    else:

        _print('La longitud de la clave secreta debe ser mayor o igual qué 32')
