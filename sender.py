# https://www.thepythoncode.com/article/send-receive-files-using-sockets-python

import socket
import os

SEPARATOR = "<SEP>"
BUFFER_SIZE = 4096

host = "192.168.178.169" # receiver-ip
port = 5000
filename = "/home/martinaemmert/Documents/network_send_test.txt"

filesize = os.path.getsize(filename)

client_socket = socket.socket()
print(f"[+] Connecting to {host}:{port}")
client_socket.connect((host, port))
print(f"Connected to {host}:{port}")

client_socket.send(f"{filename}{SEPARATOR}".encode())

with open(filename, "rb") as file:
    while True:
        bytes_read = file.read(BUFFER_SIZE)
        if not bytes_read: # done
            break
        client_socket.sendall(bytes_read)

client_socket.close()