from Crypto.Cipher import AES
from Crypto import Random
from hashlib import sha256
from base64 import b64encode, b64decode

class AESCript:

    def __init__(self, password):

        if (len(password) < 32):

            password = sha256(password).digest()

        else:

            if (isinstance(password, bytes)):

                password = password[:32]

            else:

                password = sha256(password).digest()

        self.password = password
        self._block_size = 128
        self.__mode = AES.MODE_CBC

    def __pad(self, string):

        return string + (self._block_size - len(string) % self._block_size) * chr(self._block_size - len(string) % self._block_size)

    def __unpad(self, string):

        return string[:-ord(string[len(string)-1:])]

    def encrypt(self, raw):

        iv = Random.new().read(AES.block_size)
        method = AES.new(self.password, self.__mode, iv)
        return iv + method.encrypt(self.__pad(b64encode(raw).decode()).encode())

    def decrypt(self, encrypted_data):

        iv = encrypted_data[:AES.block_size]
        method = AES.new(self.password, self.__mode, iv)

        try:

            return b64decode(self.__unpad(method.decrypt(encrypted_data)[AES.block_size:])).decode()

        except UnicodeDecodeError:

            return b64decode(self.__unpad(method.decrypt(encrypted_data)[AES.block_size:]))
