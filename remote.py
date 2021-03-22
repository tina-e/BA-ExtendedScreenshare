import subprocess

host = '192.168.178.'
user = 'pi'

#command = 'ssh -tt pi@192.168.178.167 -X'
command = 'ssh ' + user + '@' + host + ' -X'
subprocess.Popen(command, shell=True)

command = 'dillo'
subprocess.Popen(command, shell=True)


##########################################################################

import Xlib
import paramiko
from ewmh import EWMH
ewmh = EWMH()

password = ''

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(host, 22, username=user, password=password)

#channel = ssh_client.get_transport().open_session()
#print(channel)
#print(type(channel))
#x11 = channel.request_x11()
#print(type(x11))
#print(x11)

