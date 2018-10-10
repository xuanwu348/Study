import sys
try:
    import selectors
except ImportError:
    print("Please use python3.x")
    sys.exit(0)
import socket

def accept(sock, mask):
    conn, addr = sock.accept()
    print("accepted conn {} from {} with mask {}".format(conn, addr, mask))
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)

def read(conn, mask):
    data = conn.recv(1024)
    if data:
        print("recv data '{}' from conn {}".format(data.decode("utf-8"), conn))
        conn.send(data)
    else:
        print("disconnect", conn)
        sel.unregister(conn)
        conn.close()

if __name__ == "__main__":
    sel = selectors.DefaultSelector()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    addr = (("0.0.0.0", 5000))
    sock.bind(addr)
    sock.listen(100)
    sock.setblocking(False)
    print("Server run on %s:%s" % addr)
    sel.register(sock, selectors.EVENT_READ, accept)

    while True:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)


