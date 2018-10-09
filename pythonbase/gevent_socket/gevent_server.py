import sys
import socket
import gevent
from gevent import monkey
import time

monkey.patch_all()

def server(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0",port))
    print("server run on %s:%s" % ("0.0.0.0", port) )
    s.listen(100)
    while True:
        cli_addr = s.accept()
        gevent.spawn(handle_request, cli_addr)

def handle_request(conn):
    try:
        while 1:
            data = conn[0].recv(1024)
            print("recv from %s : %s" % (data.decode("utf-8"), conn[-1]))
            conn[0].send(data)
            if not data:
                conn.shutdown()
    except Exception as e:
        print("Some error occurred, season:%s" % e)
    finally:
        conn[0].close()

if __name__ == "__main__":
    server(5000)
