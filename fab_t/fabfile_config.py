#encoding:utf-8
from fabric import task, Config, Connection
import getpass

password = getpass.getpass("what's your password:")
host = "10.240.109.121"
config = Config()
conf_dict = {
            "user":"hddl",
            "port":22,
            "connect_kwargs":{"password":"intel123"},
            "timeouts":{"connect":5},
            "sudo":{'user':None, "prompt":"\\[sudo\\] password for hddl:", "password":password}
         } 
config.update(conf_dict)

def update_config(connection):
    run_hots = connection.host
    c = Connection(run_hots, config=config)
    return c
    
@task
def getplatforminfo(c):
    with update_config(c) as c:
        c.run("uname -a")
    

if __name__ == "__main__":
    c = Connection(host="10.240.109.121",config=config)
    c.run("uname -a")

