# -*- coding: UTF-8 -*-

import re
from json import loads as j_loads
from yaml import load as y_loads

def convert_str(data):

    return(str(data))

def convert_list(data, split=','):

    data = str(data)

    return([x.strip() for x in data.split(split)])

def convert_tuple(data):

    data = str(data)

    return(tuple(convert_list(data)))

def convert_int(data):

    try:

        return(int(data))

    except (ValueError, TypeError):

        raise ValueError('{} no es un número o es un valor incorrecto')

def convert_bool(data):

    data = str(data).strip()

    if (data[:1] == '0') or (data[:2] == '-0') or (data == ''):

        return(False)

    else:

        return(True)

def convert_bytes(data):

    return(data.encode())

def sumary(value):

    if (value[:5].lower() == 'list:') or (value[:6].lower() == 'tuple:'):

        parsed = []
        value_of = 'list' if (value[:5].lower() == 'list:') else 'tuple'
        value_supreme = value[5:] if (value_of == 'list') else value[6:]
        char = value_supreme[0]
        
        if (char == ';'):

            raise KeyError('El carácter utilizado no es correcto, porque está reservado')

        result = convert_list(value_supreme[1:], char)
    
        for _ in result:

            parsed.append(sumary(_))

        return(tuple(parsed) if (value_of == 'tuple') else parsed)

    if (value[:4].lower() == 'str:'):

        return(value[4:])

    if (value[:4].lower() == 'null'):

        return(None)

    elif (value[:6].lower() == 'bytes:'):

        return(convert_bytes(value[6:]))

    elif (value[:4].lower() == 'int:'):

        return(convert_int(value[4:]))

    elif (value[:5].lower() == 'bool:'):

        return(convert_bool(value[5:]))

    elif (value[:5].lower() == 'dict:'):

        return(convert_dict(value[5:]))

    elif (value[:5].lower() == 'file:'):

        with open(value[5:], 'rb') as file_object:

            return(file_object.read())

    elif (value[:5].lower() == 'json:') or (value[:5].lower() == 'yaml:'):

        loads = j_loads if (value[:5].lower() == 'json:') else y_loads

        with open(value[5:], 'rt') as file_object:

            return(loads(file_object.read()))

    else:

        raise ValueError('No se pudo encontrar el tipo de dato que desea')

def convert_dict(data):

    data = str(data)

    result = {}

    if (data.strip() == ''):

        raise ValueError('Los datos introducidos no son correctos')

    char = re.search(r'^;.;', data)

    if (char):

        char = char.group(0)

    else:

        raise SyntaxError('¡Falta definir la etiqueta o no es una etiqueta válida!')

    for _ in data.split(char)[1:]:

        if (_.count('=') == 0):

            raise SyntaxError('Debe seguir la especificación acordada')

        (key, value) = _.split('=', 1)

        result[key] = sumary(value)

    return(result)
