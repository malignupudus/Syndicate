# -*- coding: UTF-8 -*-

import re
from json import loads as j_loads
from yaml import load as y_loads

def convert_str(data):

    return(str(data))

def convert_list(data):

    data = str(data)

    return([x.strip() for x in data.split(',')])

def convert_tuple(data):

    data = str(data)

    return(tuple(convert_list(data)))

def convert_int(data):

    try:

        return(int(data))

    except (ValueError, TypeError):

        return(False)

def convert_bool(data):

    data = str(data)

    if (data[:1] == '0'):

        return(False)

    else:

        return(True)

def convert_bytes(data):

    return(data.encode())

def convert_dict(data):

    data = str(data)

    result = {}

    if (data.strip() == ''):

        return(False)

    char = re.search(r'^;.;', data)

    if (char):

        char = char.group(0)

    else:

        raise SyntaxError('¡Falta definir la etiqueta o no es una etiqueta válida!')

    for _ in data.split(char)[1:]:

        if (_.count('=') == 0):

            return(False)

        (key, value) = _.split('=', 1)

        if (value[:4].lower() == 'str:'):

            result[key] = value[4:]

        elif (value[:6].lower() == 'bytes:'):

            result[key] = convert_bytes(value[6:])

        elif (value[:5].lower() == 'list:'):

            result[key] = convert_list(value[5:])

        elif (value[:4].lower() == 'int:'):

            result[key] = convert_int(value[4:])

        elif (value[:5].lower() == 'bool:'):

            result[key] = convert_bool(value[5:])

        elif (value[:5].lower() == 'dict:'):

            result[key] = convert_dict(value[5:])

        elif (value[:6].lower() == 'tuple:'):

            result[key] = convert_tuple(value[6:])

        elif (value[:5].lower() == 'file:'):

            with open(value[5:], 'rb') as file_object:

                result[key] = file_object.read()

        elif (value[:5].lower() == 'json:') or (value[:5].lower() == 'yaml:'):

            loads = j_loads if (value[:5].lower() == 'json:') else y_loads

            with open(value[5:], 'rt') as file_object:

                result[key] = loads(file_object.read())

        else:

            return(False)

    return(result)
