#!/usr/bin/env python3

while(1):

    try:

        from utils.sys_utils import no_terminate

    except KeyboardInterrupt:

        continue

    else:

        break

from modules.UI import argprogrammer

from utils.Wrappers import wrap
from utils.Ciphers import generate_uniqkey

parser.set_head('''
       Syndicate Project - Actualizar el token de acceso
       -----------------   -----------------------------''')

parser = argprogrammer.Parser()

parser.add(['-h', '--help'], 'help', 'Mostrar la ayuda que estás viendo')
parser.add(['-l', '--long'], 'long', 'La longitud del token de acceso. Debe ser mayor o igual qué "32".', type=int, default=32)

args = parser.parse_args()

long_ = args.long

token = wrap.read('token', 'token', wrap.USE_TOKEN)

def _print(string):

    print(f'[Token-Update]: {string}') 

if (long_ == None):
    
    if not (token == False):

        _print('Token: %s' % (token))

    else:

        _print('¡Hay un error leyendo el token!')

else:

    _print('Actualizando token ...')
    
    token = generate_uniqkey.generate(long_)

    if (wrap.add('token', {'token':token}, agent=wrap.USE_TOKEN) == True):

        _print('Token actualizado: "%s"' % (token))

    else:

        _print('Error actualizando el token de acceso ...')
