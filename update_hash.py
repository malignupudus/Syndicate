#!/usr/bin/env python3

while(1):

    try:

        from utils.sys_utils import no_terminate

    except KeyboardInterrupt:

        continue

    else:

        break

import re
import sys
from os.path import isfile

from modules.Ciphers import db_hash
from modules.UI import iInput

from utils.Wrappers import wrap

from conf import global_conf

_db_passwd = '%s/%s' % (global_conf.conf['conf_dir'], global_conf.conf['db_passwd'])

def _debug(indicator, datatype=str, char=None):

    while (True):

        try:

            _input = iInput.iInput(char=char, datatype=datatype, indicator=indicator)

        except KeyboardInterrupt:

            print()
            sys.exit(1)

        if not (_input):

            continue

        return(_input)

if (isfile(_db_passwd)):

    print()
    print('* ¿Estás seguro de querer continuar? *')
    print()

    while (True):

        try:

            _confirm = iInput.iInput(char_limit=1, indicator='> ')

        except KeyboardInterrupt:

            sys.exit(1)

        if not _confirm:

            continue

        if (re.match(r'^(1|y|s){1}', _confirm)):

            break

        elif (re.match(r'^(0|n){1}', _confirm)):

            sys.exit(0)

        else:

            print('Debe ingresar (1|y|s), para afirmar y (0|n) para negar.')
            continue

    _passwd = _debug('Contraseña Nueva: ', char='*')
    _security_number = _debug('Número de seguridad: ', datatype=int)
    _decrement_number = _debug('Número de disminución: ', datatype=int)
    _security_chars = _debug('Caracteres de seguridad: ')
    _iterations = _debug('Número de iteraciones: ', datatype=int)

    print('Procesando ...')

    _hash = db_hash.hash(_passwd, _iterations, _security_chars, _security_number, _decrement_number)

    print('Sobre-Escribiendo ...')

    with open(_db_passwd, 'wt') as _obj:

        _obj.write(_hash)

    print('Hecho.')
    print()

else:

    print('El Hash no existe! ...')
