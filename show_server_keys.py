#!/usr/bin/env python3

while(1):

    try:

        from utils.sys_utils import no_terminate

    except KeyboardInterrupt:

        continue

    else:

        break

import sys
from os.path import basename, splitext

from modules.UI import argprogrammer

from utils.Wrappers import wrap
from utils.Ciphers import _decrypt_rsa_private_key

prog = basename(splitext(sys.argv[0])[0])

parser = argprogrammer.Parser()

parser.add(['-h', '--help'], 'help', 'Muestra la ayuda que estás viendo')
parser.add(['-P', '--rsa-passphrase'], 'rsa_passphrase', 'La frase de contraseña para desencriptar la clave privada RSA')

args = parser.parse_args()

rsa_passphrase = args.rsa_passphrase

_db = wrap.getall(wrap.USE_SERVER)

if (_db.get('keys') == None):

    print('Error leyendo las claves del servidor ...')
    sys.exit(1)

_keys = _db['keys']

(pub_key, priv_key) = (_keys['public_key'], _keys['private_key'])

if not (rsa_passphrase == None):

    try:

        priv_key = _decrypt_rsa_private_key._decrypt(priv_key, rsa_passphrase)

    except ValueError:

        print()
        print('\033[1m\033[37m* \033[33m\033[4mLa frase de contraseña de la clave privada es incorrecta. \033[37m*\033[0m')
        print()

print('\033[1m\033[34m\033[4mClave Pública\033[0m:')
print('\n\033[37m%s\033[0m' % (pub_key))
print('\n')
print('\033[1m\033[34m\033[4mClave Privada\033[0m:')
print('\n\033[37m%s\033[0m' % (priv_key))
