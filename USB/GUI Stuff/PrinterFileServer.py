#!/usr/bin/env python3

import os
from tkinter import *
#import tqdm
import socket


class PrinterFileServerWithGUI:
    def __init__(self, address, port, textFrame, path=""):
        self.ADDR = address
        self.PORT = int(port)
        self.SEPERATOR = "<BREAK>"
        self.BUFFER_SIZE = 4096
        self.textArea = textFrame
        if path == "":
            self.PATH = os.path.abspath(os.getcwd())
        else:
            if os.path.isdir(path):
                self.PATH = path
            else:
                self.__outputMsg("Invalid path given", False)
        print("Finished setup")

    def run_client(self, filename):
        if os.path.isfile(filename):
            filesize = os.path.getsize(filename)
            sock = socket.socket()
            sock.connect((self.ADDR, self.PORT))
            sock.send("{} {} {}".format(filename, self.SEPERATOR, filesize).encode())
            with open(filename, "rb") as f:
                while True:
                    bytes_read = f.read(self.BUFFER_SIZE)
                    if not bytes_read:
                        break
                    sock.sendall(bytes_read)
            sock.close()
            self.__outputMsg("Successfully Sent {}".format(filename))
        else:
            print(filename)
            self.__outputMsg("file was not found", False)

    def run_server(self):
        sock = socket.socket()
        sock.bind((self.ADDR, self.PORT))
        sock.listen(5)
        print("Server {} is listening for connections on Port {}".format(self.ADDR, self.PORT))
        self.__outputMsg("Server {} is listening for connections on Port {}".format(self.ADDR, self.PORT))
        while True:
            cl_sock, cl_addr = sock.accept()
            self.__outputMsg("Server {} connected to {} successfully".format(self.ADDR, cl_addr))

            recv = cl_sock.recv(self.BUFFER_SIZE).decode()
            filename, filesize = recv.split(self.SEPERATOR)
            filename = os.path.basename(filename)

            with open(self.PATH + "/" + filename.strip(), "wb") as f:
                while True:
                    bytes_read = cl_sock.recv(self.BUFFER_SIZE)
                    if not bytes_read:
                        break
                    f.write(bytes_read)
            cl_sock.close()
            sock.close()
            self.__outputMsg("Successfully saved {} to {}".format(filename, self.PATH + '/' + filename.strip()))

    def __outputMsg(self, message, append=True):
        if append:
            self.textArea.insert(INSERT, "\n" + message)
        else:
            self.textArea.delete('1.0', END)
            self.textArea.insert(INSERT, message)





class PrinterFileServer():
    def __init__(self, address, port, path=""):
        self.ADDR = address
        self.PORT = int(port)
        self.SEPERATOR = "<BREAK>"
        self.BUFFER_SIZE = 4096
        if path == "":
            self.PATH = os.path.abspath(os.getcwd())
        else:
            if os.path.isdir(path):
                self.PATH = path
            else:
                print("Invalid path given")

    def run_client(self, filename):
        if os.path.isfile(filename):
            filesize = os.path.getsize(filename)
            sock = socket.socket()
            sock.connect((self.ADDR, self.PORT))
            sock.send("{} {} {}".format(filename, self.SEPERATOR, filesize).encode())
#           progress = tqdm.tqdm(range(filesize), "Sending {}".format(filename), unit="B", unit_scale=True, unit_divisor=1024)
            with open(filename, "rb") as f:
                while True:
                    bytes_read = f.read(self.BUFFER_SIZE)
                    if not bytes_read:
                        break
                    sock.sendall(bytes_read)
#                   progress.update(len(bytes_read))
            sock.close()
        else:
            print("file was not found")


    def run_server(self):
        sock = socket.socket()
        sock.bind((self.ADDR, self.PORT))
        sock.listen(5)
        while True:
            print("Server {} is listening for connections on Port {}".format(self.ADDR, self.PORT))
            cl_sock, cl_addr = sock.accept()
            print("Server {} connected to {} succesfully".format(self.ADDR, cl_addr))

            recv = cl_sock.recv(self.BUFFER_SIZE).decode()
            filename, filesize = recv.split(self.SEPERATOR)
            filename = os.path.basename(filename)
            filesize = int(filesize)

#            progress = tqdm.tqdm(range(filesize), "Receiving {}".format(filename), unit="B", unit_scale = True, unit_divisor = 1024)
            with open (self.PATH + "/" + filename.strip(), "wb") as f:
                while True:
                    bytes_read = cl_sock.recv(self.BUFFER_SIZE)
                    if not bytes_read:
                        break
                    f.write(bytes_read)
#                    progress.update(len(bytes_read))
            cl_sock.close()
            sock.close()

