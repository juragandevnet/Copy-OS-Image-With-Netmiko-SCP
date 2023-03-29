from threading import Thread
from netmiko import ConnectHandler, file_transfer
import re
import getpass

def CopyScp(device_type, username, password, ip_address):
    SshLogin = {
        "device_type" : device_type,
        "ip" : ip_address,
        "username" : username,
        "password" : password,
        }
    try:
        net_connect = ConnectHandler(**SshLogin)
        host = net_connect.send_command("show run | i hostname")
        hostname = re.search(r"\b(\w+)$", host)
        SecureCopy = file_transfer(
            net_connect,
            source_file = "../c800-universalk9-mz.SPA.159-3.M6.bin",
            dest_file = "../c800-universalk9-mz.SPA.159-3.M6.bin",
            file_system="flash:",
            direction="put",
            overwrite_file="True",
            socket_timeout = 3600
        )
        print(hostname.group(1) + " = " + str(SecureCopy))
    except Exception:
        print("Check your Network Connection, make sure you can SSH to", ip_address)

### READ FILE ###
f = open("devices.txt", "r")

### LOGIN ###
username = input("Username: ")
password = getpass.getpass()

### THREAD PROCESS ###
threads=[]
threads = [Thread(target=CopyScp, args=("cisco_ios", username, password, ip_address)) for ip_address in f.readlines()]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
