#server: xpra start :100 --start=firefox --use-display
#client: xpra attach ssh://lab:password@192.168.178.169/200
#-> statt 'start' was anderes testen?

# xprop _NET_WM_PID
# uuid = 8180f5b933d84afd9c7765f198811234


#auf client + server gerät beim öffnen der anwendung
#xpra attach ssh://lab@192.168.178.169/100 --sharing

#öffnen der anwendung mittels:
#xpra start :XX --start=anwendung --use-display --sharing

import subprocess

is_client = True
display = '100'


#client command - accessing the application
def accessing_command(is_self):
    server_user = 'lab'
    server_password = 'apfelsaft'
    server_ip = 'localhost'
    if not is_self:
        server_ip = '192.168.178.169'
    host = 'ssh://' + server_user + ':' + server_password + '@' + server_ip + '/' + display
    return 'xpra attach ' + host + ' --sharing'

#server command - starting the application
def starting_command():
    application = 'gnome-terminal'
    #command = 'xpra start :' + display + ' --sharing'
    #out = subprocess.check_output(command, shell=True)
    #return 'DISPLAY=:' + display + ' ' + application
    return 'xpra start :' + display + ' --start=' + application + ' --use-display --sharing'


if is_client:
    command = accessing_command(False)
if not is_client:
    command = starting_command()
    subprocess.Popen(command, shell=True)
    command = accessing_command(True)
subprocess.Popen(command, shell=True)

