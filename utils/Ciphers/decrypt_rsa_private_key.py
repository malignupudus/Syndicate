import sys
from utils.Ciphers import _decrypt_rsa_private_key

def decrypt(priv_key, key, admin):

    try:

        priv_key = _decrypt_rsa_private_key._decrypt(priv_key, key)

    except ValueError:

        print('La frase de contraseña de "%s" es incorrecta!' % (admin))
        sys.exit(1)

    else:

        return(priv_key)
