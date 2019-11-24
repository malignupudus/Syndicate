#!/usr/bin/env python3

import shelve
import sys
from conf import global_conf

argv = sys.argv[1:]
flag = 'c' if not (argv == []) else 'n'

if not (argv == []):

    if (argv[0][:4].lower() == 'help'):

        print(f'{sys.argv[0]}:' + '\n'
                '\t' + 'help    Muestra la ayuda' + '\n'
                '\t' + '<id>    Identificador del comando a borrar' + '\n\n'
                '\t' + 'Nota: Si no coloca ningún parámetro se reiniciara toda el almacén.')
        sys.exit(0)

try:

    with shelve.open('{}/{}'.format(global_conf.databases['database'], global_conf.databases['defend']), writeback=True, flag=flag) as wrap:

        if (argv != []):

            if (wrap.get(argv[0]) != None):

                wrap.pop(argv[0])
                print('SUCCESS: Borrado: {}'.format(argv[0]))

            else:

                print('ERROR: {} no existe ...'.format(argv[0]))

        else:

            print('SUCCESS: El almacén se borro completamente')

except Exception as Except:

    print('ERROR: Error reiniciando el almacén de la defensa. Excepción: {}'.format(Except))
