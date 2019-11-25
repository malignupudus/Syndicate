from modules.Ciphers import aes
from utils.sys_utils import bytes_convert
from yaml import safe_dump as dump, safe_load as load
from zlib import compress, decompress
from base64 import b64encode, b64decode

def encrypt(passwd, data, use_base64=True):

    _aes = aes.AESCript(bytes_convert.convert(passwd))
    data = compress(_aes.encrypt(bytes_convert.convert(dump(data))))

    return(b64encode(data) if (use_base64 == True) else data)

def decrypt(passwd, data, use_base64=True):

    _aes = aes.AESCript(bytes_convert.convert(passwd))

    return(load(_aes.decrypt(decompress(b64decode(data) if (use_base64 == True) else data))))
