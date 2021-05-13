from paramiko import SSHClient, AutoAddPolicy
import getpass
#from rich import print, pretty, inspect
import win_geo

window = win_geo.get_win_at(100, 100)
window_class = [elem.lower() for elem in window.get_wm_class()]

host = '192.168.178.169'
user = 'lab'
password = 'afpelsaft'
#password = getpass.getpass()

client = SSHClient()
#client.load_host_keys('/etc/hosts.allow')
client.load_system_host_keys()
client.set_missing_host_key_policy(AutoAddPolicy())
client.connect(host, username=user, password=password)
del password
print("connection done")


print(window_class)
for win in window_class:
    command = 'DISPLAY=:0 ' + win
    stdin, stdout, stderr = client.exec_command(command)
    err_msg = f'{stderr.read().decode("utf-8")}'
    if not err_msg: break
if "command not found" in err_msg:
    print(window.get_geometry())
    print("sending screenshot...")


stdin.close()
stdout.close()
stderr.close()

client.close()

