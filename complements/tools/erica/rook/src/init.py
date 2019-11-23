from hashlib import md5 as _md5, sha1 as _sha1, sha224 as _sha224, sha256 as _sha256, sha384 as _sha384, sha512 as _sha512

class HashNotFound(Exception):

    '''
    Llamado cuando el hash no existe
    '''

hash_list = [_md5, _sha1, _sha224, _sha256, _sha384, _sha512]

def Crack(password_hash, wordlist, hash_func):

    if (isinstance(wordlist, list) != True):

        raise TypeError('El tipo de dato de la lista de hashes no es correcta')

    hash_ = [x for x in hash_list if (x.__name__[8:].lower() == hash_func.lower())]

    if ([] == hash_):

        raise HashNotFound('El hash no existe')

    else:

        hash_ = hash_[0]

    for _ in wordlist:

        _ = _.strip()

        if (hash_(_.encode()).hexdigest() == password_hash):

            return(True, _)

    return(False, password_hash)
