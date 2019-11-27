import shelve
from utils.Ciphers import simplycrypt
from hashlib import sha512

def __create(path):

    with shelve.open(path):

        pass

def add(key, value, password, path):

    __create(path)

    try:

        with shelve.open(path, writeback=True) as obj:

            obj[sha512(key.encode()).hexdigest()] = simplycrypt.encrypt(password, value)

    except:

        #DEBUG
        #raise

        return(False)

    else:

        return(True)

def read(key, password, path):

    __create(path)

    try:

        with shelve.open(path, flag='r') as obj:

            _data = obj[sha512(key.encode()).hexdigest()]

    except:

        #DEBUG
        #raise

        return(False)

    else:

        return(simplycrypt.decrypt(password, _data))
