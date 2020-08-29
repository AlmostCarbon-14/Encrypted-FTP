#!/usr/bin/env python3


from cryptography.fernet import Fernet
import time
import random
import string
import os

class FileCrypt:
    def __init__(self):
        self.salt = self.__salt_gen()
        self.__write_key(self.salt)

    def __salt_gen(self):
        password_characters = string.digits
        password = ''.join(random.choice(password_characters) for i in range(8))
        return password
                                    
    def __write_key(self, salt):
        key = Fernet.generate_key()
        with open ("key" + salt + ".ky", "wb") as key_file:
            key_file.write(key)
                                                                                
    def __load_key(self):
        return open("key" + self.salt + ".ky", "rb").read()
    
    def key(self):
        return self.__load_key()

    def encrypt_file(self, filename): 
        f = Fernet(self.__load_key())
        with open(filename, "rb") as file:
            data = file.read()
            e_data = f.encrypt(data)
            file.close()
        with open(filename, "wb") as file:
            file.write(e_data)
                           
    def cleanup(self):
        os.system("rm key*")

    def decrypt_file(self, filename):
        f = Fernet(self.__load_key())
        with open(filename, "rb") as file:
            e_data = file.read()
            data = f.decrypt(e_data)
        with open(filename, "wb") as file:
            file.write(data)
    
    def decrypt_with_key(self, filename, key):
        f = Fernet(key)
        with open(filename, "rb") as file:
            e_data = file.read()
            data = f.decrypt(e_data)
        with open(filename, "wb") as file:
            file.write(data)
