# -*- coding: UTF-8 -*-

class InvalidHeader(Exception):

    '''Cuando el encabezado es incorrecto'''

def check(headers):

    if not (isinstance(headers, dict)) and not (headers == None):

        raise InvalidHeader('Encabezado inválido.')

    if not (headers == None):

        for _key, _value in headers.items():

            if not (isinstance(_key, str)) or not (isinstance(_value, str)):

                raise InvalidHeader('El tipo de dato de la clave o el valor no es un «string»')

            elif (_key.strip() == ''):

                raise InvalidHeader('La clave es inválida')

            elif not (_value == '') and (_value.strip() == ''):

                raise InvalidHeader('El valor es inválido')
