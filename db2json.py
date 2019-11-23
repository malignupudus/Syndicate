#!/usr/bin/python3

while(1):

    try:

        from utils.sys_utils import no_terminate

    except KeyboardInterrupt:

        continue

    else:

        break

import sys
import re
from os.path import isfile
try:
    from utils.Wrappers import wrap
except Exception as Except:
    print(str(Except))
    sys.exit(1)
from json import dumps
from base64 import b64encode
from modules.UI import argprogrammer

def __dict_json_decode(data):

    _result = {}

    for key, value in data.items():

        _result[key] = b64encode(value).decode()

    return(_result)

optionals = 'Opcionales'

parser = argprogrammer.Parser()

parser.add(['-h', '--help'], 'help', 'Muestra la ayuda que estás viendo', group=optionals)
parser.add(['-separate'], 'separate', 'Sí el almacén se divide en varias partes, deberia usarme', type=bool, action=True)
parser.add(['-username'], 'username', 'Yo debo ir junto a mi hermano "-separate"')
parser.add(['-personal'], 'personal', 'Usé un almacén personal en vez de uno predeterminado')
parser.add(['-db-identifier'], 'user', 'El identificador de la base de datos. Use «-show-ids» para ver los identificadores disponibles', type=int, default=1)
parser.add(['-show-ids'], 'show_ids', 'Muestra los identificadores de las base de datos', type=bool, action=True, group=optionals)
parser.add(['-raw'], 'raw', 'Muestra la base de datos sin desencriptar. *Igualmente se le preguntará los datos necesarios*', type=bool, action=True, group=optionals)

args = parser.parse_args()

user = args.user
show_ids = args.show_ids
raw = args.raw
personal = args.personal
separate = args.separate
username = args.username

if not (personal == None):

    wrap.db_personal = personal

if (show_ids == False):

    try:

        if not (username == None) and (separate == True) and not (isfile('{}/{}.db'.format(wrap.getDB(user), username))):

            print(dumps((True, '¡El almacén seleccionado no existe!')))
            sys.exit(1)

        if (raw == False):

            db = wrap.getall(user, username=username, separate=separate)

        else:

            db = __dict_json_decode(dict(wrap.raw(user, username=username, separate=separate)))

    except wrap.databaseIsNotDefined as Except:

        print(str(Except))
        sys.exit(1)

    except wrap.agentNotExists:

        print(dumps((True, 'El identificador no existe ...')))
        sys.exit(1)

    except OSError as Except:

        print(dumps((True, str(Except))))
        sys.exit(1)

    else:

        print(dumps((False, db), indent=6))

else:

    print('\nIdentificadores:\n%s\n' % ('-'*15))

    _ids = [x for x in dir(wrap) if (re.match('^USE_.', x))]

    for indicator, _id in enumerate(_ids, 1):

        print(f'{indicator}): {_id}')

    print()
