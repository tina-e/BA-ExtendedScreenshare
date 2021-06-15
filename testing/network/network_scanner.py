import networkscan
import socket

my_network = "192.168.178.0/24"
my_scan = networkscan.Networkscan(my_network)
my_scan.run()

list_of_available_devices = []
for i in my_scan.list_of_hosts_found:
    try:
        list_of_available_devices.append(socket.gethostbyaddr(i))
    except socket.herror:
        continue

print(list_of_available_devices)