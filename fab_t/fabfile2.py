from fabric import Connection
import getpass

c = Connection(host="192.168.8.103",port="22",user='pi')
password = getpass.getpass("what's your password?")
c.connect_kwargs.password = password
result = c.run("uname -a")
print(result.stdout)
