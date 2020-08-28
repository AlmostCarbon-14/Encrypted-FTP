#!/usr/bin/env python3
import socket
import tqdm
import os
from e_file import FileCrypt


SEPERATOR = "<SEPERATOR>"
BUFF_SIZE = 4096

sock = socket.socket()
sock.bind(("localhost", 6069))
sock.listen(5)

client_socket, addr = sock.accept()

recv = client_socket.recv(BUFF_SIZE).decode()

key, name, size = recv.split(SEPERATOR)

name = os.path.basename(name)

size = int(size)

print("Received: ", key, name, size)

progress = tqdm.tqdm(range(size), f"Receiving {name}", unit="B", unit_scale=True, unit_divisor=1024)
with open(name, "ab") as f:
    for _ in progress:
        bytes_read = client_socket.recv(BUFF_SIZE)
        if not bytes_read:    
            break
        f.write(bytes_read)
        progress.update(len(bytes_read))

    client_socket.close()
    sock.close()
