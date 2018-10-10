import socket
import select
import queue

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setblocking(False)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
addr = ("0.0.0.0", 5000)
s.bind(addr)
s.listen(100)
print("Server run on %s:%s" % addr)
readable_list = [s,]
writeable_list = []
msg = {}

while True:
    rb, wb, et = select.select(readable_list, writeable_list, readable_list)
    for r in rb:
        if r is s:
            conn, addr_ = r.accept()
            #conn.setblocking(False)
            print("Create new connect with %s:%s" % addr_)
            readable_list.append(conn)
            msg[conn] = queue.Queue()
        else:
            data = r.recv(1024)
            print("Recv data: {}".format(data.decode("utf-8")))
            msg[r].put(data)
            #if r not in writeable_list:
            writeable_list.append(r)

    for w in wb:
        print("send msg.....")
        data = msg[w].get()
        w.send(data)
        writeable_list.remove(w)

    for e in et:
        if e in writeable_list:
            writeable_list.remove(e)
        readable_list.remove(e)
        #e.close()
        del msg[e]
        e.close()





