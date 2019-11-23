import os
from utils.Ciphers import generate_uniqkey
from utils.Ciphers import simplycrypt

EXTENSION = 'symplix'

class decryptionError(Exception):

    """
    Cuando hay un error desencriptando los datos
    """

def tree(path):

    if not (os.path.isdir(path)):

        raise OSError('{}, no existe o no es un directorio')

    for root, directory, files in os.walk(path):

        for _ in files:

            file_ = os.path.join(root, _)

            if (os.path.isfile(file_)):

                yield file_

def encrypt(file, extension=EXTENSION):

    key = generate_uniqkey.generate(32)
    filename  = '{}.{}'.format(file, extension)

    if (os.path.isfile(file)):

        with open(file, 'rb') as obj:

            file_encrypt = simplycrypt.encrypt(key, obj.read(), False)

        with open(file, 'wb') as obj:

            obj.write(file_encrypt)

        os.rename(file, filename)

        return({
                    'filename':'{}/{}'.format(os.getcwd(), filename),
                    'length':len(file_encrypt),
                    'password':key
                    
                })

    else:

        raise FileNotFoundError('¡El archivo "{}" no existe!'.format(file))

def decrypt(file, key, extension=EXTENSION, exception=False):

    if (os.path.isfile(file)):

        if (file.endswith('.{}'.format(extension)) == True):

            with open(file, 'rb') as obj:

                try:

                    file_decrypt = simplycrypt.decrypt(key, obj.read(), False)

                except:

                    if (exception == True):

                        raise

                    else:

                        raise decryptionError('¡Error desencriptando los datos!')

            with open(file, 'wb') as obj:

                obj.write(file_decrypt)

            os.rename(file, os.path.splitext(file)[0])

            return(os.path.splitext(file)[0])

    else:

        raise FileNotFoundError('¡El archivo "{}" no existe!'.format(file))

def tree_encrypt(directory, extension=EXTENSION):

    files = []

    if (os.path.isdir(directory)):

        for _ in tree(directory):

            files.append(encrypt(_, extension))

        return(files)

    else:

        raise NotADirectoryError('{} no es un directorio'.format(directory))

def tree_decrypt(data, extension=EXTENSION):

    index = 0

    if (isinstance(data, list)):

        for _ in data:

            if (isinstance(_, dict)):

                if (isinstance(_.get('filename'), str)) and (isinstance(_.get('password'), str)):

                    try:

                        decrypt(_.get('filename'), _.get('password'), extension)

                    except:

                        pass

                    else:

                        index += 1

        return(index)

    else:

        raise TypeError('El tipo de dato de los datos no es correcto')
