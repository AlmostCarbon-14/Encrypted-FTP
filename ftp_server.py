#!/usr/bin/env python3
import socket
import tqdm
import os
import time
import sys
import subprocess as sp
from e_file import FileCrypt


SEPERATOR = "<SEPERATOR>"
BUFF_SIZE = 4096
args = sys.argv
if "-p" in args: #this is for later if I feel like it
    PORT = port_scan()
else:
    PORT = input("Please Enter a Port Number: \n")

cmd = "ifconfig | grep 255.255.255.0"

inet = sp.check_output(cmd, shell = True)
inet = wlan.decode("utf-8")
inet = wlan.split(" ")
inet_addr = inet[inet.index("inet") + 1]
print(inet_addr)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((socket.gethostbyname(socket.gethostname()), int(PORT)))
print(f"Listening at {socket.gethostbyname(socket.gethostname())} : {PORT}")
sock.listen(5)

client_socket, addr = sock.accept()
recv = client_socket.recv(BUFF_SIZE).decode()
key, name, size = recv.split(SEPERATOR)
name = os.path.basename(name)
size = int(size)
key = key[2:-1]

progress = tqdm.tqdm(range(size), f"Receiving {name}", unit="B", unit_scale=True, unit_divisor=1024)
with open(name, "wb") as f:
    for _ in progress:
        bytes_read = client_socket.recv(BUFF_SIZE)
        if not bytes_read:    
            break
        f.write(bytes_read)
        progress.update(len(bytes_read))
    print(f"{name} Has Finished Downloading and has been saved in this directory")
    client_socket.close()
    sock.close()
    f.close()
e_file = FileCrypt(False)
e_file.decrypt_with_key(name, key)
time.sleep(5)
