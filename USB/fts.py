#!/usr/bin/env python3

import RPi.GPIO as GPIO
import os
import time
import tqdm
import socket



PORT = 1069
ADDR = "0.0.0.0"


class PrinterFileServer():
    def __init__(self, address, port):
        self.ADDR = address
        self.PORT = port
        self.SEPERATOR = "<BREAK>"
        self.MNT_PATH = 'mnt/usb'
        self.SDA_PATH = 'dev/sda1'
        self.BUFFER_SIZE = 4096

    def mount(self):
        try:
            if (not os.path.isdir(self.MNT_PATH)):
                os.system("sudo mkdir {}".format(self.MNT_PATH))
        except:
            print("couldn't make folder")

        try:
            os.system("sudo mount {} {}".format(self.SDA_PATH, self.MNT_PATH))
        except:
            print("Could not mount USB")


    def dismount(self):
        return True
        if (os.path.isdir(self.MNT_PATH)):
            try:
                os.system("sudo umount {}".format(self.MNT_PATH))
            except:
                print("drive couldn't be dismounted")
                return false

    def run_client(self, filename):
        if os.path.isfile(filename):
            filesize = os.path.getsize(filename)
            sock = socket.socket()
            sock.connect((self.ADDR, self.PORT))
            sock.send("{} {} {}".format(filename, self.SEPERATOR, filesize).encode())
            progress = tdqm.tqdm(range(filesize), "Sending {}".format(filename), unit="B", unit_scale=True, unit_divisor=1024)
            with open(filename, "rb") as f:
                while True:
                    bytes_read = f.read(self.BUFFERSIZE)
                    if not bytes_read:
                        break
                    sock.sendall(bytes_read)
                    progress.update(len(bytes_read))
            sock.close()
        else:
            print("file was not found")


    def run_server(self):
        sock = socket.socket()
        sock.bind((self.ADDR, self.PORT))
        while True:
            sock.listen(5)
            print("Server {} is listening for connections on Port {}".format(self.ADDR, self.PORT))
            cl_sock, cl_addr = sock.accept()
            print("Server {} connected to {} succesfully".format(self.ADDR, cl_addr))

            recv = cl_sock.recv(self.BUFFER_SIZE).decode()
            filename, filesize = recv.split(self.SEPERATOR)
            filename = os.path.basename(filename)
            filesize = int(filesize)

            progress = tqdm.tqdm(range(filesize), "Receiving {}".format(filename), unit="B", unit_scale = True, unit_divisor = 1024)
            with open (self.MNT_PATH + "/" + filename, "wb") as f:
                while True:
                    bytes_read = cl_sock.recv(self.BUFFER_SIZE)
                    if not bytes_read:
                        break
                    f.write(bytes_read)
                    progress.update(len(bytes_read))
            cl_sock.close()
            sock.close()

