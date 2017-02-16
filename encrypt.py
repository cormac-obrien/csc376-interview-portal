# Copyright 2016. DePaul University. All rights reserved.
# This work is distributed pursuant to the Software License
# for Community Contribution of Academic Work, dated Oct. 1, 2016.
# For terms and conditions, please see the license file, which is
# included in this distribution.

import pip

try:
    __import__('imp').find_module('Crypto')
    from Crypto import Random
    from Crypto.Cipher import AES
except ImportError:
    pip.main(['install', 'pycryptodome'])
    from Crypto import Random
    from Crypto.Cipher import AES

####################################################
#                    Tom Plutz                     #
# The encryption class takes a string 16, 24,or 32 #
# digit key as a string and is converted to bytes  #
# by the constructor. Use by instantiating an      #
# Encrypt object with the key passed and call      #
# encrypt or decrypt with a string passed as msg   #
####################################################


class Encrypt:
    def __init__(self, key):
        self.key = bytes(key, 'utf-8')

    def encrypt(self, message, key_size=256):
        message = (str(message) + ("\0" * (
            (AES.block_size - len(message) % AES.block_size))))
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(bytes(message, 'utf-8'))

    def decrypt(self, ciphertext):
        if (len(ciphertext) == 0):
            return ''
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.decode("utf-8", 'ignore').rstrip("\0")
