import socket

server_addr = ("localhost",5000)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(server_addr)

while True:
    data = bytes(input(">>>>"),encoding="utf-8")
    s.send(data)
    recv_data = s.recv(1024)
    print("recv: %s" % recv_data.decode("utf-8"))
