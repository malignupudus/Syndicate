from modules.Ciphers import POO_RSA as rsa
from modules.Ciphers import aes

from utils.Ciphers import generate_uniqkey

from zlib import compress, decompress
from yaml import safe_load as load, safe_dump as dump
from base64 import b64encode, b64decode

encode = lambda string: b64encode(string)
decode = lambda string: b64decode(string)

def encrypt(raw, public_key):

    raw = dump(raw)

    rsa_test = rsa.main()
    rsa_test.import_PublicKey(public_key)

    key_session = generate_uniqkey.generate(32)

    aes_test = aes.AESCript(key_session.encode())

    key_session = rsa_test.encrypt(key_session)

    content = {}

    content['key_session'] = key_session
    content['content'] = aes_test.encrypt(raw.encode())

    return(encode(compress(dump(content).encode())))

def decrypt(enc_data, private_key):

    enc_data = load(decompress(decode(enc_data)))

    rsa_test = rsa.main()
    rsa_test.import_PrivateKey(private_key)

    key_session = rsa_test.decrypt(enc_data['key_session']).encode()
    
    aes_test = aes.AESCript(key_session)

    content = aes_test.decrypt(enc_data['content'])

    return(load(content))
