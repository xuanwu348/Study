import paramiko
import sys
import os
import socket
import getpass

from paramiko.py3compat import u

try:
    import termios
    import tty
    has_termios = True
except ImportError:
    has_termios = False

def interactive_shell(chan):
    if has_termios:
        posix_shell(chan)
    else:
        windows_shell(chan)

def posix_shell(chan):
    import select

    oldtty = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.settimeout(0.0)
        while True:
            readable, writeable, errors = select.select([chan, sys.stdin], [], [], 1)
            if chan in readable:
                try:
                    x = u(chan.recv(1024))
                    if not len(x):
                        sys.stdout.write("\r\n**** EOF\r\n")
                        break
                    sys.stdout.write(x)
                    sys.stdout.flush()
                except socket.timeout:
                    pass
            if sys.stdin in readable:
                x = sys.stdin.read(1)
                if not len(x):
                    break
                chan.send(x)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty) 

def windows_shell(chan):
    import threading

    sys.stdout.write("Line-buffered terminal emulation. Press F6 or ^z to senf EOF.\r\n\r\n")
    def writeall(sock):
        while True:
            data = sock.recv(256).decode("utf-8")
            if not data:
                sys.stdout.write("\r\n*** EOF\r\n\r\n")
                sys.stdout.flush()
                break
            sys.stdout.write(data)
            sys.stdout.flush()

    writer = threading.Thread(target=writeall, args=(chan,))
    writer.start()
    
    try:
        while True:
            d = sys.stdin.read(1)
            if not d:
                break
            chan.send(d)
    except EOFError:
        pass

def run():
    default_username = getpass.getuser()
    username = input("Usernamer [%s]: " % default_username)
    if not len(username):
        username = default_username
    
    hostname = input("Hostname: ")
    if not len(hostname):
        print("[Error]Hostname required.")
        sys.exit(1)
    
    tran = paramiko.Transport((hostname, 22))
    tran.start_client()

    default_auth = "p"
    auth = input("Auth by (p)assword or (rsa) key[%s] " % default_auth)
    if not len(auth):
        auth = default_auth

    if auth == "r":
        default_path = os.path.join(os.environ['HOME'], ".ssh", "id_rsa")
        path = input("RSA key [%s]: " % default_path)
        if not len(path):
            path = default_path
        try:
            key = paramiko.RSAKey.from_private_key_file(path)
        except paramiko.PasswordRequiredException:
            password = getpass.getpass("RSA key password: ")
            key = paramiko.RSAKey.from_private_key_file(path, password)
        tran.auth_publickey(username, key)
    else:
        pw = getpass.getpass('Password for %s@%s:' % (username, hostname) )
        tran.auth_password(username, pw)
    
    chan = tran.open_session()
    chan.get_pty()
    chan.invoke_shell()
   
    interactive_shell(chan)
    chan.close()
    tran.close()

if __name__ == "__main__":
    run()
