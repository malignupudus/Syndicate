#!/usr/bin/env python3

while(1):

    try:

        from utils.sys_utils import no_terminate

    except KeyboardInterrupt:

        continue

    else:

        break

import sys
import re
import os
from os import get_terminal_size
from datetime import datetime
from time import sleep

try:

    from utils.Wrappers import wrap

except Exception as Except:

    print(str(Except))
    sys.exit(1)

from utils.sys_utils import clear
from utils.sys_utils import bell

from modules.UI import argprogrammer
from modules.UI import iInput

from conf import global_conf

def _detect_time(_extract, time_, hours, minutes, seconds, microseconds):
    
    _time_formated = '{}:{}:{}.{}'.format(_extract.hour, _extract.minute, _extract.second, _extract.microsecond)

    if (_time_formated == time_):

        return(True)

    elif (hours == _extract.hour):

        if (minutes == 0) and (seconds == 0) and (microseconds == 0):

            return(True)

        elif not (minutes == 0) and (seconds == 0) and (microseconds == 0):

            if (minutes == _extract.minute):

                return(True)

        elif not (minutes == 0) and not (seconds == 0) and (microseconds == 0):

            if (minutes == _extract.minute) and (seconds == _extract.second):

                return(True)

        elif not (minutes == 0) and not (seconds == 0) and not (microseconds == 0):

            if (minutes == _extract.minute) and (seconds == _extract.second) and (microseconds == _extract.microsecond):

                return(True)

        elif not (microseconds == 0) and (minutes == 0) and (seconds == 0):

            if (microseconds == _extract.microsecond):

                return(True)

        elif not (seconds == 0) and not (microseconds == 0) and (minutes == 0):

            if (seconds == _extract.second) and (microseconds == _extract.microsecond):

                return(True)

        elif not (seconds == 0) and (microseconds == 0) and (minutes == 0):

            if (seconds == _extract.second):

                return(True)

    elif (minutes == _extract.minute):

        if (seconds == 0) and (microseconds == 0):

            return(True)

        elif not (seconds == 0) and (microseconds == 0):

            if (seconds == _extract.second):

                return(True)

        elif not (seconds == 0) and not (microseconds == 0):

            if (seconds == _extract.second) and (microseconds == _extract.microsecond):

                return(True)

        elif not (microseconds == 0) and (seconds == 0):

            if (microseconds == _extract.microsecond):

                return(True)

    elif (seconds == _extract.second):

        if (microseconds == 0):

            return(True)

        elif (microseconds == _extract.microsecond):

            return(True)

    elif (microseconds == _extract.microsecond):

        return(True)

def _detect_date(_extract, date, year, month, day):

    _date_formated = '{}-{}-{}'.format(_extract.year, _extract.month, _extract.day)

    if (_date_formated == date):

        return(True)

    elif (year == _extract.year):

        if (month == 0) and (day == 0):

            return(True)

        elif not (month == 0) and (day == 0):

            if (month == _extract.month):

                return(True)

        elif (month == 0) and not (day == 0):

            if (day == _extract.day):

                return(True)

    elif (month == _extract.month):

        if (day == 0):

            return(True)

        elif (day == _extract.day):

            return(True)

    elif (day == _extract.day):

        return(True)

index = 0

(max_year, max_month, max_day, max_hour, max_minute, max_second, max_microsecond) = (datetime.max.year, datetime.max.month, datetime.max.day, datetime.max.hour, datetime.max.minute, datetime.max.second, datetime.max.microsecond)

optionals = 'Opcionales'
pattern_group = 'Búsqueda'
spec_group = 'Búsqueda especifica'

default_which = 'message'

parser = argprogrammer.Parser()

parser.set_head('''
       Syndicate Project - Enviar mensajes a un Evie
       -----------------   -------------------------''')

parser.set_footer('\n' + '  ' + 'En caso de usar --date y --time, se combinarán los valores y en caso de querer usar valores especificos se usa el "0". Ejemplo: "--time 00:23:00".')

parser.add(['-h', '--help'], 'help', 'Mostrar la ayuda qué estás viendo', group=optionals)
parser.add(['-l', '--limit'], 'limit', 'Limite a mostrar. 0 (Infinito)', default=0, type=int)
parser.add(['-t', '--time'], 'time', f'Buscar por tiempo en vez de patrón. Sintaxis: HH:MM:SS.MSMSMS [MAX: {max_hour}:{max_minute}:{max_second}.{max_microsecond}]', group=spec_group)
parser.add(['-d', '--date'], 'date', f'Busca por fecha en vez de patrón. Sintaxis: AA-MM-DD [MAX: {max_year}-{max_month}-{max_day}]', group=spec_group)
parser.add(['-s', '--search'], 'search', 'El patrón de búsqueda', group=pattern_group)
parser.add(['-which'], 'which', 'Elegir el dato a utilizar en la búsqueda. Los valores permitidos, son: [NICKNAME], [SUBJECT], [MESSAGE]', uniqval=['nickname', 'subject', 'message'], group=pattern_group, default=default_which)
parser.add(['-delete'], 'delete', 'Borrar uno o más mensajes. Separa por \',\' seguido del ID del mensaje para borrar varios a la vez', type=list)

args = parser.parse_args()

limit = args.limit
time_ = args.time
date = args.date
search = args.search
which = args.which
delete = args.delete

if not (delete == None):

    for _ in delete:

        if (wrap.delete(_, agent=wrap.USE_MESSAGE) == True):

            print('Se elimino correctamente: {}'.format(_))

        else:

            print('Error eliminando a: {}'.format(_))

else:

    if not (date == None):

        date = date.split('-')

        if (len(date) > 3):

            print('Error en la sintaxis. No está siguiendo la sintaxis necesario para usar la fecha.')
            sys.exit(1)

        elif (True in [True for x in date if (x.strip() == '')]):

            print('No puede usar campos vacios para representar la fecha. Recuerde qué en caso de no querer usar valores especificos, se usan los ceros o no se escriben.')
            sys.exit(1)

        else:

            (year, month, day) = (date+[None, None])[:3]

            _dat = {'month':month, 'day':day}

            [globals().__setitem__(x, '00') for x in _dat if (_dat[x] == None)]

            for _ in {'year', 'month', 'day'}:

                try:

                    globals()[_] = int(globals()[_])

                except ValueError:

                    print('{}, No es un tipo de dato correcto'.format(globals()[_]))
                    sys.exit(1)

            if (len(str(year)) != 4):

                print('La longitud del año no es la correspondiente.')
                sys.exit(1)

            else:

                if (year > max_year):

                    print('EL año se excedió del limite permitido.')
                    sys.exit(1)

            if (len(str(month)) > 2):

                print('La longitud del mes no es la correspondiente.')
                sys.exit(1)

            else:

                if (month > max_month):

                    print('EL mes se excedió del limite permitido.')
                    sys.exit(1)

            if (len(str(day)) > 2):

                print('La longitud del día no es la correspondiente.')
                sys.exit(1)

            else:

                if (day > max_day):

                    print('El día se excedió del limite permitido.')
                    sys.exit(1)

            date = '%d-%d-%d' % (year, month, day)

    if not (time_ == None):

        time_ = time_.split(':')

        if (len(time_) > 4):

            print('Error en la sintaxis. No está siguiendo la sintaxis necesaria para usar el tiempo.')
            sys.exit(1)

        elif (True in [True for x in time_ if (x.strip() == '')]):

            print('No puede usar campos vacios para representar el tiempo. Recuerde qué en caso de no querer usar valores especificos, se usan los ceros o no se escriben.')
            sys.exit(1)

        else:

            (hours, minutes, seconds) = (time_+[None, None])[:3]

            if (minutes == None):

                minutes = '00'

            if (seconds == None):

                seconds = '00.000000'

            SS_AND_MS = seconds.split('.')[:2]
            seconds = SS_AND_MS[0]
            
            if (len(SS_AND_MS) == 1):

                microseconds = '000000'

            else:

                microseconds = SS_AND_MS[1]

            for _ in {'hours', 'minutes', 'seconds', 'microseconds'}:

                try:

                    globals()[_] = int(globals()[_])

                except ValueError:

                    print('{}, No es un tipo de dato correcto'.format(globals()[_]))
                    sys.exit(1)

            if (len(str(hours)) > 2):

                print('La longitud de la hora no es la correspondiente.')
                sys.exit(1)

            else:

                if (hours > max_hour):

                    print('La hora se excedió del limite permitido.')
                    sys.exit(1)

            if (len(str(minutes)) > 2):

                print('La longitud de los minutos no es la correspondiente.')
                sys.exit(1)

            else:

                if (minutes > max_minute):

                    print('Los minutos se excedieron del limite permitido.')
                    sys.exit(1)

            if (len(str(seconds)) > 2):

                print('La longitud de los segundos no es la correspondiente.')
                sys.exit(1)

            else:

                if (seconds > max_second):

                    print('Los segundos se excedieron del limite permitido.')
                    sys.exit(1)

            if (len(str(microseconds)) > 6):

                print('La longitud de los micro-segundos no es la correspondiente.')
                sys.exit(1)

            else:

                if (microseconds > max_microsecond):

                    print('Los micro-segundos se excedieron del limite permitido.')
                    sys.exit(1)

        time_ = '%d:%d:%d.%d' % (hours, minutes, seconds, microseconds)

    print('Leyendo mensajes ...')
    sleep(1)

    messages_lst = wrap.getall(wrap.USE_MESSAGE)

    if (len(messages_lst) == 0):

        print('Aún no hay mensajes...')
        sys.exit(0)

    messages = [x for x in messages_lst]
    messages = messages[:limit] if not (limit == 0) else messages

    if not (date == None) or not (time_ == None):

        result = []

        for _ in messages:

            _extract = datetime.fromtimestamp(messages_lst[_]['time'])

            if not (date == None) and not (time_ == None):

                _formated = '{}-{}-{} {}:{}:{}.{}'.format(_extract.year, _extract.month, _extract.day, _extract.hour, _extract.minute, _extract.second, _extract.microsecond)

                if (_formated == '{} {}'.format(date, time_)):

                    result.append(_)

                elif (_detect_date(_extract, date, year, month, day) == True) or (_detect_time(_extract, time_, hours, minutes, seconds, microseconds) == True):

                    result.append(_)

            elif not (date == None) and (time_ == None):

                if (_detect_date(_extract, date, year, month, day) == True):

                    result.append(_)

            elif (date == None) and not (time_ == None):

                if (_detect_time(_extract, time_, hours, minutes, seconds, microseconds) == True):

                    result.append(_)

        messages = result

    if not (search == None):

        result = []

        for _ in messages:

            if (which.lower() == 'nickname'):

                if (re.search(search, messages_lst[_]['nickname'], re.IGNORECASE)):

                    result.append(_)

            elif (which.lower() == 'subject'):

                if (re.search(search, messages_lst[_]['subject'], re.IGNORECASE)):

                    result.append(_)

            elif (which.lower() == 'message'):

                if (re.search(search, messages_lst[_]['message'], re.IGNORECASE)):

                    result.append(_)

        messages = result

    if (len(messages) == 0):

        print('¡Sin coincidencias!')
        sys.exit(0)

    while (1):

        (columns, lines) = get_terminal_size()

        clear.clear()

        print()

        wrapper = messages_lst[messages[index]]
        _write = datetime.fromtimestamp(wrapper['time'])

        print('\t\033[1m\033[34mID:\033[0m \033[4m\033[1m\033[37m{}\033[0m'.format(messages[index]))
        print()
        print('\t\t\033[37mDe: \033[1m{}\033[0m'.format(wrapper['nickname']))
        print('\t\t\033[37mSubject: \033[1m{}\033[0m'.format(wrapper['subject']))
        print('\t\t\033[37mFecha y Hora de escritura: \033[1m{}-{}-{} ~ {}:{}:{}.{}\033[0m'.format(_write.year, _write.month, _write.day, _write.hour, _write.minute, _write.second, _write.microsecond))
        print('\t\t\033[37mMensaje:\033[0m')

        for _ in wrapper['message'].splitlines():

            print('\t\t\t\033[1;37m{}\033[0m'.format(_))

        print()

        if (wrapper['profile'] == None):

            print('\t\t\033[1;37mNo se incrustaron archivos...\033[0m')

        else:

            if (os.path.isdir(wrapper['profile'])):

                _files = os.listdir(wrapper['profile'])

                if (len(_files) == 0):

                    print('\t\t\033[1;37mNo hay archivos almacenados en "{}"\033[0m'.format(wrapper['profile']))

                else:

                    print('\t\t\033[37mIncrustado: \033[1;37m{}: {}\033[0m'.format(wrapper['profile'], ', '.join(_files)))

            else:

                print('\t\tNo existe el directorio de archivos...')

        print()
        print('\033[3mSiguiente (%d/%d) o (Q)uit\033[0m\033[%dB' % (index+1, len(messages), lines-1), end='')

        try:

            key = iInput.iInput(char=' ', char_limit=1)

        except KeyboardInterrupt:

            break

        except Exception as Except:

            clear.clear()
            print('Error desconocido: {}'.format(Except))
            sys.exit(1)

        if (key == 'r'):

            if not (index == len(messages)-1):

                index += 1

        elif (key == 'l'):

            if (index > 0):

                index -= 1
        
        elif (key == 'q'):

            break

        else:

            bell.bell()

    clear.clear()
