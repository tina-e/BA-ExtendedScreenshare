import socket
import os

server_host = "0.0.0.0"
# or 0.0.0.0 for more than 1 network
server_port = 5000

SEPARATOR = "<SEP>"
BUFFER_SIZE = 4096 # TODO: problem mit kleinen Dateien -> nichts kommt an

server_socket = socket.socket()
server_socket.bind((server_host, server_port))

server_socket.listen(5)
print(f"[*] Listening as {server_host}:{server_port}")

client_socket, address = server_socket.accept()
print(f"{address} is connected.")

received = client_socket.recv(BUFFER_SIZE).decode()
filename = received.split(SEPARATOR)[0]
#filename, filesize = received.split(SEPARATOR)
# idk y but filesize braucht man hier, sonst kommt kein Inhalt an
filename = os.path.basename(filename)

with open(filename, "wb") as file:
    while True:
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            break
        file.write(bytes_read)

client_socket.close()
server_socket.close()