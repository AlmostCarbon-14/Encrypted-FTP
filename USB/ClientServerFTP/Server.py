#!/usr/bin/env python3

import threading
import time
import random
import socket

'''
PACKET STRUCTURE

BEGIN CONNECTION
{NAME}<BREAK>"Hello"<BREAK>

END CONNECTION
{NAME}<BREAK>"Bye"<BREAK>

TTL SYN
"RUTHERE?"<BREAK>

TTL ACK
{NAME}<BREAK>"YAIAM"<BREAK>

BUSY
"YES/NO<BREAK>"

SEND REQUEST
{NAME}<BREAK>"SENDREQ"<BREAK>
'''


def sendStr(self, args):
    ret = ''
    for arg in args:
        ret += arg + '<BREAK>'
    return ret


class Server:

    def __init__(self, Address, Port):
        self.connections = {}
        self.BUFFER_SIZE = 4096
        self.SEPERATOR = "<BREAK>"
        self.ADDR = Address
        self.PORT = int(Port)
        self.TTL = 1800

    def __TTL(self, name):
        while True:
            time.sleep(self.TTL)
            addr = self.connections['name']
            clientSock = socket.socket()
            clientSock.connect(addr)
            try:
                clientSock.send(sendStr("RUTHERE?"))
                msg = clientSock.recv(self.BUFFER_SIZE).decode().split(self.SEPERATOR)
                if msg[0] == "YAIAM":
                    pass
                clientSock.close()
            except socket.timeout:
                try:
                    self.connections.pop(name)
                except:
                    pass
            finally:
                clientSock.close()
                break

    def __ConnectionThread(self, clientSock, clientAddr):
        msg = clientSock.recv(self.BUFFER_SIZE).decode().split(self.SEPERATOR)
        print(msg)
        if msg[1] == 'Hello':
            if msg[0] not in self.connections:
                self.connections[msg[0]] = clientAddr
                ttlThread = threading.Thread(target=self.__TTL(), args=(msg[0],))
                ttlThread.start()
        elif msg[1] == 'Bye':
            self.connections.pop(msg[1])
        elif msg[1] == 'ListUsers':
            print(f"Sending: {sendStr(self.connections.keys())}")
            clientSock.send(sendStr(self.connections.keys()))
        clientSock.close()

    def run(self):
        sock = socket.socket()
        sock.bind((self.ADDR, self.PORT))
        sock.listen(5)
        print(f"Server is listening at {self.ADDR} : {self.PORT}")
        while True:
            cl_sock, cl_addr = sock.accept()
            print(f"Host has connected to: {cl_addr[0]} : {cl_addr[1]}")
            thread = threading.Thread(target=self.__ConnectionThread, args=(cl_sock, cl_addr))
            thread.start()


server = Server("0.0.0.0", random.randint(1000, 65000))
server.run()
