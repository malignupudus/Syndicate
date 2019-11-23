import sys
from modules.Ciphers import POO_RSA

def check(rsa_password, credentials):

    _passwords = rsa_password.split(',')
    _evalue_credentials = {}

    for _ in _passwords: 

        if (_.count(':') != 1):

            print('La frase de contraseña "%s" no sigue el formato correcto!' % (_))
            sys.exit(1)

        _admin = _.split(':')[0]
        _pass = _.split(':')[1]

        if not (_admin in credentials):

            print('%s, parece ser que no existe ...' % (_admin))
            sys.exit(1) 

        _evalue_credentials[_admin] = _pass

    return(_evalue_credentials)
