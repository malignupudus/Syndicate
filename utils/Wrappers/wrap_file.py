from modules.Ciphers import aes
from utils.sys_utils import bytes_convert
from os import chmod

def wrap(filename, passwd, content=None):

    passwd = str(passwd).encode()
    _aes = aes.AESCript(passwd)

    if not (content == None):

        with open(filename, 'wb') as _file_object:

            result = _file_object.write(_aes.encrypt(bytes_convert.convert(content)))

        chmod(filename, 0o444)

        return(result)

    else:

        with open(filename, 'rb') as _file_object:

            try:

                dat = _aes.decrypt(_file_object.read())

            except:

                #DEBUG
                #raise

                return(False)

            else:

                return(dat if not (dat == '') else False)
