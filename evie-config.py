#!/usr/bin/env python3

while(1):

    try:

        from utils.sys_utils import no_terminate

    except KeyboardInterrupt:

        continue

    else:

        break

import shelve
import sys
import re
from pprint import pprint

from modules.UI import argprogrammer

from utils.Wrappers import wrap

from conf import global_conf

def _print(string):

    print(f'[Evie-Config]: {string}')

_max_row = 0

data_group = 'Interactuar con los datos'
danger_group = 'Reiniciar la configuración'

parser = argprogrammer.Parser()

parser.set_head('''
       Syndicate Project - Configuración dinamica de Evie
       -----------------   ------------------------------''')

parser.add(['-h', '--help'], 'help', 'Muestra la ayuda que estás viendo', group='Opcionales')

parser.add(['-k', '--key'], 'key', 'La clave de la configuración')
parser.add(['-sK', '--sub-key'], 'sub_key', 'La sub-clave de confiuración')
parser.add(['-v', '--value'], 'value', 'El valor de la clave de configuración')

parser.add(['-print-configuration'], 'print_config', 'Imprimir los valores de configuración', type=bool, action=True, group=data_group)
parser.add(['-static'], 'static', 'Muestra la configuración estática', type=bool, action=True, group=data_group)
parser.add(['-t', '--target'], 'target', 'Objetivo a borrar. Valores únicos: [KEY] y [SUBKEY]', uniqval=['KEY', 'SUBKEY'], group=data_group)

parser.add(['-r', '--reset'], 'reset', 'Borrar todos los datos (Peligroso)', type=bool, action=True, group=danger_group)

args = parser.parse_args()

key = args.key
sub_key = args.sub_key
value = args.value
print_config = args.print_config
target = args.target
reset = args.reset
static = args.static

if not (key == None) or (print_config == True):

    dat = wrap.getall(wrap.USE_CONFIG)

    if (dat.get('config') == None):

        dat['config'] = {}

    dat = dat['config']

    if (print_config == True):

        if (static == True):

            _print('Leyendo archivo de configuración estática ...')

            _transformer = {}
            static_config = global_conf.__dict__

            for _ in static_config.keys():

                if (re.match(r'(?!__).+(?!__)', _)):

                    _transformer[_] = static_config.get(_)

            print()
            pprint(_transformer, indent=6, width=100)
            sys.exit(0)

        if (len(dat) == 0):

            _print('Aún no se introducen valores al fichero de configuración.')
            sys.exit(1)

        for key, value in dat.items():

            for subkey, subvalue in value.items():

                if (len(subkey) > _max_row):

                    _max_row = len(subkey)

        _max_space = ' '*_max_row

        print()
        
        for key, value in dat.items():

            print(f'{key}:')

            if (len(value) == 0):

                print('\t\033[4mAún no se introducen valores a la sub-clave\033[0m')

            else:

                for subkey, subvalue in value.items():

                    subkey = (subkey+' '*(_max_row))[:_max_row]

                    print(f'\t{subkey}{_max_space}{subvalue}')

    else:

        if (target == None):

            if (sub_key == None):

                _print('¡La sub-clave no está definida!')
                sys.exit(1)

            if (value == None):

                _print('¡El valor no está definido!')
                sys.exit(1)

            if (dat.get(key) == None):

                dat[key] = {}

            dat[key][sub_key] = value

            if (wrap.add('config', dat, agent=wrap.USE_CONFIG) == True):

                _print(f'Asignado => {key} => {sub_key} => {value}')

            else:

                _print(f'Error asignando a => {key} => {sub_key} => {value}')

        else:


            if (dat.get(key) == None):

                _print(f'¡La clave "{key}" no existe!')
                sys.exit(1)

            if (target.lower() == 'key'):

                del dat[key]

                if (wrap.add('config', dat, agent=wrap.USE_CONFIG) == True):

                    _print(f'Borrado => {key}')

                else:

                    _print(f'No se pudo borrar => {key}')

            elif (target.lower() == 'subkey'):

                if (dat[key].get(sub_key) == None):

                    _print(f'¡La subclave "{sub_key}" no existe!')
                    sys.exit(1)

                del dat[key][sub_key]

                if (wrap.add('config', dat, agent=wrap.USE_CONFIG) == True):

                    _print(f'Borrado => {key} => {sub_key}')

                else:

                    _print(f'No se pudo borrar => {key} => {sub_key}')

elif (reset == True):

    _print('Reiniciando ...')

    try:

        with shelve.open('%s/%s' % (global_conf.conf['conf_dir'], global_conf.conf['conf_file']), flag='n') as _obj:

            pass

    except Exception as Except:

        _print('No se pudo reiniciar, porque ocurrio una excepción: "%s"' % (Except))

    else:

        _print('Reiniciado.')

else:

    print('No has introducido ningún parámetro ...')
