#!/usr/bin/env python3

import threading
import time
import random
import socket

'''
PACKET STRUCTURE

BEGIN CONNECTION
"Hello"<BREAK>{NAME}<BREAK>

END CONNECTION
"Bye"<BREAK>{NAME}<BREAK>

TTL SYN
"RUTHERE?"<BREAK>

TTL ACK
"YAIAM"<BREAK>


'''


class User:

    def __init__(self, Address, Port):
        self.ADDR = Address
        self.PORT = Port

    def __str__(self):
        return f"{self.Name} is at {self.ADDR} : {self.PORT}"


class Server:

    def __init__(self, Address, Port):
        self.connections = {}
        self.BUFFER_SIZE = 4096
        self.SEPERATOR = "<BREAK>"
        self.ADDR = Address
        self.PORT = int(Port)

    def __ConnectionThread(self, clientSock):
        msg = clientSock.recv(self.BUFFER_SIZE).decode().split(self.SEPERATOR)
        print(msg)
        if msg[0] == 'Hello':
            self.connections[msg[1]] = clientSock



    def run(self):
        sock = socket.socket()
        sock.bind((self.ADDR, self.PORT))
        sock.listen(5)
        print(f"Server is listening at {self.ADDR} : {self.PORT}")
        while True:
            cl_sock, cl_addr = sock.accept()
            self.__ConnectionThread(cl_sock)


server = Server("0.0.0.0", random.randint(1000, 65000))
server.run()
