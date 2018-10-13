import socket
import json
import os


statuscode = {
        "200" : {"code":"200", "content":"200 OK"},
        "201" : {"code":"201", "content":"201 query"},
        "408" : {"code":"408", "content":"408 temp response"},
        "403" : {"code":"403", "content":"403 forbidden"},
        "404" : {"code":"404", "content":"404 error"},
        "400" : {"code":"400", "content":""}
        }


class FtpClient(object):
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def help(self):
        msg = '''
        ls
        pwd
        cd ../..
        get filename
        put filename
        '''
        print(msg)
    def connect(self,ip,port):
        self.client.connect((ip, port))
    def interactive(self):
        #self.authenticate()
        while True:
            cmd = input(">>").strip()
            if len(cmd) ==0:continue
            cmd_str = cmd.split()[0]
            if hasattr(self,"cmd_%s" % cmd_str):
                func = getattr(self,"cmd_%s" % cmd_str)
                func(cmd)
            else:
                self.help()
                
    def cmd_put(self,*args):
        
        cmd_split =  args[0].split()
        if len(cmd_split) >1:
            filename = cmd_split[1]
            if os.path.isfile(filename):
                filesize = os.stat(filename).st_size
                msg_dic = {
                    "method": "put",
                    "filename":filename,
                    "filesize": filesize,
                }
                self.client.send(json.dumps(msg_dic).encode("utf-8"))
                print("send",json.dumps(msg_dic).encode("utf-8") )
              
                server_response = json.loads(self.client.recv(1024).decode("utf-8"))
                if server_response['code'] == "408":
                    self.client.send(json.dumps(statuscode['200']).encode("utf-8"))
                server_response = json.loads(self.client.recv(1024).decode("utf-8"))
                while server_response["code"] != "200":
                    print(server_response['content'])
                    choice = input("Please input 'O' or 'R':")
                    statuscode['400']['content'] = choice.strip()
                    self.client.send(json.dumps(statuscode['400']).encode("utf-8"))
                    server_response = json.loads(self.client.recv(1024).decode("utf-8"))
                    while server_response['content'].find("filename") != -1:
                        newname = input("Please input filename:")
                        statuscode['400']['content'] = newname .strip()
                        self.client.send(json.dumps(statuscode['400']).encode("utf-8"))
                        server_response = json.loads(self.client.recv(1024).decode("utf-8"))
                        if server_response['code'] == "200":
                            self.client.send(json.dumps(statuscode['200']).encode("utf-8"))
                            break
    
                f = open(filename,"rb")
                for line in f:
                    self.client.send(line)
                    data = self.client.recv(1024).strip().decode("utf-8")
                    print(data)
                else:
                    print("file upload success...")
                    f.close()
            else:
                print(filename,"is not exist")
    def cmd_get(self):
        pass

if __name__ == "__main__":
    ftp = FtpClient()
    ftp.connect("192.168.8.103",5000)
    ftp.interactive()
