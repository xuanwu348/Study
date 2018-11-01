import paramiko
import sys
import os
import socket
import select
import getpass
import termios
import tty
from paramiko.py3compat import u

username = "hddl"
password = getpass.getpass("What's your password:")

tran = paramiko.Transport(('10.240.109.208',22))
tran.start_client()
tran.auth_password(username, password)

chan = tran.open_session()
chan.get_pty()
chan.invoke_shell()

oldtty = termios.tcgetattr(sys.stdin)

try:
    tty.setraw(sys.stdin.fileno())
    chan.settimeout(0.0)

    while True:
        readable, writable, error = select.select([chan, sys.stdin,], [], [], 1)
        if chan in readable:
            try:
                x = u(chan.recv(1024))
                if not len(x):
                    print('\r\n*** EOF\r\n')
                    break
                sys.stdout.write(x)
                sys.stdout.flush()
            except socket.timeout:
                pass
        if sys.stdin in readable:
            inp = sys.stdin.read(1)
            if not len(inp):
                break
            chan.sendall(inp)
finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)

chan.close()
tran.close()


