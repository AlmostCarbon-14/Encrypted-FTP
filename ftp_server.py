#!/usr/bin/env python3
import socket
import tqdm
import os
from e_file import FileCrypt


SEPERATOR = "<SEPERATOR>"
BUFF_SIZE = 4096
PORT = input("Please Enter a Port Number: \n")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(('', int(PORT)))
sock.listen(5)

client_socket, addr = sock.accept()

recv = client_socket.recv(BUFF_SIZE).decode()

key, name, size = recv.split(SEPERATOR)

name = os.path.basename(name)

size = int(size)

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
print("Key: " + key)
print("Key Type: " + type(key))
e_file = FileCrypt(False)
e_file.decrypt_with_key(name, key)
