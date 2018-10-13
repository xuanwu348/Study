import socketserver
import json
import os
import re
from statuscode import statuscode


class MyTCPHandler(socketserver.BaseRequestHandler):

    def __enpacketmsg(self, data):
        if isinstance(data, bytes):
            return data
        else:
            return json.dumps(data).encode("utf-8")

    def __depacketmsg(self,data):
        if isinstance(data, bytes):
            return json.loads(data.strip().decode("utf-8"))

    #__init__(self, request, client_address, server)
    def handle(self):
        while 1:
            try:
                print("msg from:{}".format(self.client_address[0]))
                method_dict = self.__depacketmsg(self.request.recv(1024)) 
                print(method_dict)
                method = method_dict["method"]
                if hasattr(self, method):
                    self.request.send(self.__enpacketmsg(statuscode["408"]))
                    func = getattr(self,method)
                    func(method_dict)
                else:
                    err_msg = "{} not a internal command or a executable program".format(method)
                    statuscode["400"]["content"] = err_msg
                    self.request.send(self.__enpacketmsg(statuscode["400"]))
                    continue
            except Exception as e:
                print("Error occurred, reason:{}".format(e))
                break

    def put(self, *args):
        method_dict = args[0]
        filesize = method_dict['filesize']
        filename = method_dict['filename']
        data = self.__depacketmsg(self.request.recv(1024))
        if data["code"] == "200":
            pass
        if os.path.isfile(filename):
            msg = "File {} is eixsts, do you want to Overried or Rename, please press 'O' to overried,or press 'R' to rename".format(filename)
            statuscode["400"]["content"] = msg
            self.request.send(self.__enpacketmsg(statuscode["400"]))
            while 1:
                data = self.__depacketmsg(self.request.recv(1024))
                if len(data['content']) == 1 and str(data['content']).isalpha() and str(data['content']).upper() in ["O", "R"]:
                    if data['content'].upper() == "O":
                        self.request.send(self.__enpacketmsg(statuscode["200"]))
                        break
                    else:
                        while data['code'] != "200":
                            msg = "please input a new filename:"
                            statuscode["400"]["content"] = msg
                            self.request.send(self.__enpacketmsg(statuscode["400"]))
                            data = self.__depacketmsg(self.request.recv(1024))
                            if os.path.isfile(data["content"]):
                                continue
                            else:
                                filename_tmp = data["content"]
                                try:
                                    filebasename, extname = filename.split(".")
                                    filename = filename_tmp + "." + extname
                                except ValueError:
                                    filename = filename_tmp
                                print(filename)
                                self.request.send(self.__enpacketmsg(statuscode["200"]))
                                data = self.__depacketmsg(self.request.recv(1024))
                        break
        else:
            print("No this file and save the file....")
            self.request.send(self.__enpacketmsg(statuscode["200"]))
        print(filename)
        with open(filename, 'ab') as f:
                recv_size = 0
                while recv_size < filesize:
                    data = self.request.recv(1024)
                    f.write(data)
                    recv_size += len(data)
                    self.request.send(("Has received {} kb".format(recv_size)).encode("utf-8"))
                #to do add recv

if __name__ == "__main__":
    server_addr = ("0.0.0.0",5000)
    print("FTP server run on {}:{}".format(*server_addr))
    server = socketserver.ThreadingTCPServer(server_addr, MyTCPHandler)
    server.serve_forever()



