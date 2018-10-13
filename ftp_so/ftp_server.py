import socketserver
import json
import os
import uuid
import re


class MyTCPHandler(socketserver.BaseRequestHandler):
    #__init__(self, request, client_address, server)
    def handle(self):
        while 1:
            try:
                self.data = self.request.recv(1024).strip()
                print("msg from:{}".format(self.client_address[0]))
                recv_data = self.data.decode("utf-8")
                print(recv_data)
                method_dict = json.loads(recv_data)
                method = method_dict["method"]
                if hasattr(self, method):
                    self.request.send("200 OK".encode("utf-8"))
                    func = getattr(self,method)
                    func(method_dict)
                else:
                    err_msg = "{} not a internal command or a executable program".format(method)
                    self.request.send(err_msg.encode("utf-8"))
                    continue
            except Exception as e:
                print("Error occurred, reason:{}".format(e))
                break

    def put(self, *args):
        method_dict = args[0]
        filesize = method_dict['filesize']
        filename = method_dict['filename']
        if os.path.isfile(filename):
            filename_temp = str(uuid.uuid4().hex)
            with open(filename_temp, 'ab') as f:
                recv_size = 0
                while recv_size < filesize:
                    data = self.request.recv(1024)
                    f.write(data)
                    recv_size += len(data)
                    self.request.send(("Has received {} kb".format(recv_size)).encode("utf-8"))
                #to do add recv
            msg = ("File {} is eixsts, do you want to overried or rename, please press 'O' to overried,or press 'R' to rename"
                    .format(filename)).encode("utf-8")
            self.request.send(msg)
            while 1:
                data = self.request.recv(1024).strip()
                if len(data) == 1 and str(data).isalpha():
                    if data.upper() == "O":
                        os.remove(filename)
                        os.rename(filename_temp, filename)
                        self.request.send(("File override, and save the file {} success!".format(filename)).encode("utf-8"))
                    elif data.upper() == "R":
                        self.request.send(("Please input the name:".encode("utf-8")))
                        filename_new = self.request.recv(1024).strip().decode("utf-8")
                        if os.path.isfile(filename):
                            self.request.send(msg)
                            continue
                        else:
                            try:
                                filebasename, extname = filename.split(".")
                                os.rename(filename_temp, filename_new + "." + extname)
                            except ValueError:
                                os.rename(filename_temp, filename_new)
                else:
                    self.request.send("please press 'O' to overried,or press 'R' to rename".encode("utf-8"))
                    continue
        with open(filename, "ab") as f:
            recv_size = 0 
            while recv_size < filesize:
                data = self.request.recv(1024)
                f.write(data)
                recv_size += len(data)
                self.request.send(("Has received {} kb".format(recv_size)).encode("utf-8"))

if __name__ == "__main__":
    server_addr = ("0.0.0.0",5000)
    print("FTP server run on {}:{}".format(*server_addr))
    server = socketserver.ThreadingTCPServer(server_addr, MyTCPHandler)
    server.serve_forever()



