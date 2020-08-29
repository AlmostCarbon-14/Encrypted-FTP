#!/usr/bin/env python3
import socket
import tqdm
import os
import sys
import re
from e_file import FileCrypt


class E_FTP_S:
    def __init__(self):
        self.addr = self.get_addr()
        self.port = 6069
        self.filename = input("Please Enter Filename:\n")
        self.buff_size = 4096
        self.seperator = "<SEPERATOR>"
        self.e_file = FileCrypt()
        self.key = self.e_file.key()
        if not self.validate_file():
            print("No such file exists")
            sys.exit()
        self.file_size = os.path.getsize(self.filename)
        
        self.connect()

    def get_addr(self):
        pattern = '[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}'
        addr = input("Please Enter Destination Address:\n")
        if addr.lower() == "localhost":
            return "localhost"
        if re.match(pattern, addr):
            return addr
        else:
            print("Invalid Address")
            sys.exit()

    def validate_file(self):
        return os.path.exists(self.filename)


    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.addr, self.port))
        sock.send(f"{self.key}{self.seperator}{self.filename}{self.seperator}{self.file_size}".encode())
        progress = tqdm.tqdm(range(self.file_size), f"Sending {self.filename}", unit="B", unit_scale=True, unit_divisor=1024)
        os.system("cp " + self.filename + " " + self.filename + "-copy")
        self.e_file.encrypt_file(self.filename + "-copy")
        with open(self.filename, "rb") as f:
            for _ in progress:
                bytes_read = f.read(self.buff_size)
                if not bytes_read:
                    break
                sock.sendall(bytes_read)
                progress.update(len(bytes_read))
        sock.close()
        os.remove(self.filename + "-copy")
        self.e_file.cleanup()

server_obj = E_FTP_S()
