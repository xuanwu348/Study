#encoding:utf-8
from fabric import task, Connection
import socket
import getpass


password = getpass.getpass("what's your password:")
key_filename = "./Identity"
host = "10.240.109.121"
user = "hddl"
port = 22
timeout = 5

def update_c_config(connect):
    runHost = connect.host if connect.host.split(".").__len__() == 4 else host
    conf = {
           "host":runHost,
           "user":user,
           "port":port,
           "connect_timeout":timeout,
           "connect_kwargs":{"password": password
                             #"key_filename": key_filenam
                             }
        }
    for k, v in conf.items():
        if hasattr(connect, k):
            setattr(connect, k, v)
    return connect

@task
def get_uname(c):
    try:
        with update_c_config(c) as c:
            c.run("uname -a")
    except socket.timeout:
        print("Timeout")

if __name__ == "__main__":
    c = Connection(host=host)
    c = update_c_config(c)
    c.run("uname -a")
    


