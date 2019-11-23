# -*- coding: UTF-8 -*-

import Crypto.Hash.MD2 as MD2
import Crypto.Hash.MD4 as MD4
import Crypto.Hash.MD5 as MD5
import Crypto.Hash.SHA as SHA
import Crypto.Hash.SHA224 as SHA224
import Crypto.Hash.SHA256 as SHA256
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_PSS

class HashAlgoNotFound(Exception):
    """
    Cuando no existe el algoritmo
    """

class PrivateKeyNotFound(Exception):
    """
    Cuando la clave privada no está definida o usa un formato incorrecto
    """

class PublicKeyNotFound(Exception):
    """
    Cuando la clave pública no está definida
    """

class privateKeyFound(Exception):
    """
    Cuando se reconoce que es una clave privada en vez de pública
    """

class main:

    def __init__(self):

        self.__keys = [None, None]
        self.__publicKey = None
        self.__privateKey = None
        
        self.__format = 'PEM'
        self.__pkcs = 8

        self.__hashes = {'MD2':MD2, 'MD4':MD4, 'MD5':MD5, 'SHA':SHA, 'SHA224':SHA224, 'SHA256':SHA256}

    def generate(self, bitsize=1024, passphrase=None):

        """
        Generar el par de llaves RSA.

        :bitsize int: Tamaño en bits de las llaves

        """

        bitsize = int(bitsize)

        self.__privateKey = RSA.generate(bitsize)
        self.__publicKey = self.__privateKey.publickey()

        private_key = self.__privateKey.exportKey(self.__format, pkcs=self.__pkcs) if (passphrase == None) else self.__privateKey.exportKey(self.__format, pkcs=self.__pkcs, passphrase=passphrase)
        private_key = private_key.decode()

        self.__keys = [self.__publicKey.exportKey(self.__format, pkcs=self.__pkcs).decode(), private_key]

    def export(self):

        """
        Exportar la clave pública y privada
        """

        return(self.__keys)

    def export_PublicKey(self):

        """
        Exportar la clave pública
        """

        return(self.__keys[0])

    def export_PrivateKey(self, passphrase=None):

        """
        Exportar la clave privada

        :passphrase str: Frase de contraseña para cifrar la clave privada
        """

        return(self.__keys[1] if (passphrase == None) else self.__privateKey.exportKey(passphrase=passphrase, pkcs=self.__pkcs))

    def import_PublicKey(self, key):

        """
        Importar la clave pública

        :key str o bytearray: Clave pública
        """

        self.__publicKey = RSA.importKey(key)

        if (self.__publicKey.has_private() == True):

            raise privateKeyFound('La clave no es un formato para una clave pública')
        
        self.__keys[0] = self.__publicKey.exportKey(self.__format, pkcs=self.__pkcs).decode()

    def import_PrivateKey(self, key, passphrase=None):

        """
        Importar la clave privada

        :key str o bytearray: Clave privada
        :passphrase str: Frase de contraseña para descifrar la clave privada
        """

        self.__privateKey = RSA.importKey(key, passphrase=passphrase) if not (passphrase == None) else RSA.importKey(key)

        if (self.__privateKey.has_private() == False):

            raise privateKeyNotFound('No es un formato valído para una clave privada')

        self.__keys[1] = self.__privateKey.exportKey(self.__format, pkcs=self.__pkcs).decode()

    def encrypt(self, data):

        """
        Cifrar datos

        :data str: El string a cifrar
        """

        data = data.encode()

        wrap = PKCS1_OAEP.new(self.__publicKey)
        return(wrap.encrypt(data))

    def decrypt(self, data):

        """
        Descifrar datos

        :data str: Los datos cifrados
        """

        wrap = PKCS1_OAEP.new(self.__privateKey)
        return(wrap.decrypt(data).decode())

    def __hash_exists(self, hash_algo):

        for _ in self.__hashes:

            if (_ == hash_algo):

                return(True)

        return(False)

    def __sign_detect(self, hash_algo):

        if (self.__hash_exists(hash_algo) == False):

            raise HashAlgoNotFound('El algoritmo no existe')

    def sign(self, data, hash_algo='SHA256'):

        """
        Firmar datos

        :data str: El dato a firmar
        :hash_algo str: El algoritmo de cifrado
        """

        self.__sign_detect(hash_algo)

        if not (self.__privateKey):

            raise PrivateKeyNotFound('La clave privada no esta definida')

        algo = self.__hashes[hash_algo]
        h = algo.new()
        h.update(data.encode())
        signer = PKCS1_PSS.new(self.__privateKey)
        return(signer.sign(h))

    def verify(self, data, signature, hash_algo='SHA256'):

        """
        Verificar si un dato ha sido modificado

        :data str: El dato a firmar
        :signature str: La firma a comprobar con el dato firmado
        :hash_algo str: El algoritmo de cifrado
        """
        
        self.__sign_detect(hash_algo)

        if not (self.__publicKey):

            raise PublicKeyNotFound('La clave pública no esta definida')

        algo = self.__hashes[hash_algo]
        h = algo.new()
        h.update(data.encode())
        verify = PKCS1_PSS.new(self.__publicKey)
        return(verify.verify(h, signature))
