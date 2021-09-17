import threading
import time
import socket

'''
PACKET STRUCTURE

BEGIN CONNECTION
"Hello"<BREAK>

END CONNECTION
"Bye"<BREAK>

TTL SYN
"RUTHERE?"<BREAK>

TTL ACK
"YAIM"<BREAK>


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

    def __ConnectionThread(self, clientSock, clientAddr):
        print(clientSock)
        print(clientAddr)
        # msg = clientSock.recv(self.BUFFER_SIZE).decode().split(self.SEPERATOR)

    def run(self):
        sock = socket.socket()
        sock.bind((self.ADDR, self.PORT))
        sock.listen(5)

        while True:
            cl_sock, cl_addr = sock.accept()
            self.__ConnectionThread(cl_sock, cl_addr)


server = Server("0.0.0.0", '5555')
server.run()
