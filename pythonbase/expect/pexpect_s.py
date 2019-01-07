#encoding:utf-8
import os
import getpass
try:
    import pexpect as expect
except ImportError as e:
    print("Please install pexpect(sudo pip3 install pexpect)")

hostname = "192.168.1.106"
#password = getpass.getpass()

logfile = open("./log.log","ab")
child = expect.spawn("ssh %s" % hostname, logfile=logfile, timeout=1)
child.expect('password:')
child.sendline(password)
child.expect("$")
child.sendline("uname -a\n")
child.expect("[\d+.]*\d+")
output = child.match.group(0) 
print("\033[32m%s\033[0m" % output.decode("utf-8"))
child.interact()
logfile.close()


