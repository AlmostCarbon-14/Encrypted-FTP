#!/usr/bin/env python3
import socket
import time
import tqdm
import os
import sys
import shutil as sh
import re
from e_file import FileCrypt


class E_FTP_S:
    def __init__(self):
        self.addr = self.get_addr()
        self.port = self.get_port()
        self.filename = input("Please Enter Filename:\n")
        self.buff_size = 4096
        self.seperator = "<SEPERATOR>"
        self.e_file = FileCrypt(True)
        self.key = self.e_file.key()
        if not self.validate_file():
            print("No such file exists")
            sys.exit()
        self.file_size = os.path.getsize(self.filename)
        self.connect()

    def get_port(self):
        port = int(input("Please Enter a Port Number: \n"))
        if port <= 1024 or port >= 65535:
            print("Your port value must be in this range (1024, 65535)")
            sys.exit()
        return port

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
        try:
            sock.connect((self.addr, self.port))
            sock.send(f"{self.key}{self.seperator}{self.filename}{self.seperator}{self.file_size}".encode())
        except:
            print("Failure to connect to host")
            self.finish()
        progress = tqdm.tqdm(range(self.file_size), f"Sending {self.filename}", unit="B", unit_scale=True, unit_divisor=1024)
        sh.copyfile(self.filename, self.filename + "-copy")
        time.sleep(2)
        self.e_file.encrypt_file(self.filename + "-copy")
        try:
            with open(self.filename + "-copy", "rb") as f:
                for _ in progress:
                    bytes_read = f.read(self.buff_size)
                    if not bytes_read:
                        break
                    sock.sendall(bytes_read)
                    progress.update(len(bytes_read))
        except:
            print("Error Reading/Sending file")    
        print(f"\"{self.filename}\" Has Completed Sending...Goodbye")
        self.finish(sock)
        time.sleep(5)

    def finish(self, sock):
        sock.close()
        os.remove(self.filename + "-copy")
        self.e_file.cleanup()

server_obj = E_FTP_S()
