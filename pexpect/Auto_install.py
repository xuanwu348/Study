import os
import subprocess
passwd = "intel123"
import sys
import time
import threading
import queue
try:
    import pexpect
except ImportError:
    os.system("echo {}|sudo -S pip3 install pexpect".format(pexpect))
    try:
        import pexpect
    except ImportError:
        print("Please install pexpect!")
        exit()
from functools import wraps
q = queue.Queue()

class AptInstall():
    def __init__(self, pkgname, passwd=passwd):
        self.pkgname = [pkgname.strip(),] if len(pkgname.strip().split()) < 2 else pkgname.strip().split()
        self.passwd = passwd
    
    def generateCMD(self):
        cmds = []
        for pkg in self.pkgname:
            cmds.append([pkg,"sudo apt install {}".format(pkg)])
        return cmds
      
    def password(self, child):
        child.sendline(self.passwd)

    @staticmethod
    def Y_or_N(child, pkg):
        child.sendline("Y")
        child.wait()
        index = child.expect(["installed", pexpect.TIMEOUT, pexpect.EOF, "Processing"])
        if index == 0:
            print("\033[32mInstall successfully\033[0m\n")
        elif index == 1:
            print("\033[33mTimeout\033[0m\n")
        elif index == 2:
            print("\033[32mEOF\033[0m\n")
        elif index == 3:
            self.installed(pkg)

    @staticmethod
    def installed(pkg):
        print("\033[32m{} has installed!\033[0m\n".format(pkg))


    @staticmethod
    def invalid(pkg):
        print("\033[33mUnable to locate package {}\033[0m".format(pkg))

    def __call__(self):
        cmds = self.generateCMD()
        for pkg,cmd in cmds:
            #child = pexpect.spawn("sudo bash", encoding="utf-8", logfile=sys.stdout)
            child = pexpect.spawn("sudo bash")
            q.put("1")
            watchstatus(pkg)
            index = child.expect(["#","password"])
            if index == 0:
                child.sendline(cmd)
            elif index ==1:
                self.password(child)
            index = child.expect(['Y/n','Unable','already',"#", "Processing", pexpect.TIMEOUT, pexpect.EOF])
            try:
                if index == 0:
                    self.Y_or_N(child, pkg)
                elif index == 1:
                    self.invalid(pkg)
                elif index in [2,3,4,6]:
                    self.installed(pkg)
                elif index == 5:
                    print("\033[33mTimeout\033\0m\n")
            except Exception as e:
                print(e)
                print("**********"*10)
                child.close(force=True)
            finally:
                while not q.empty():
                    q.get()
                time.sleep(1)
                child.close(force=True)

def decorate_th(f):
    @wraps(f)
    def w(*args, **kwargs):
        t = threading.Thread(target=f, args=args, kwargs=kwargs)
        t.start()
    return w

@decorate_th
def watchstatus(pkg):
    while not q.empty():
        sys.stdout.write("\r{} installing {} ".format(time.ctime(), pkg))
        time.sleep(0.5)

if __name__ == "__main__":
    AptInstall("vim")()
    AptInstall("ffmpeg")()
    AptInstall("nload")()
    AptInstall("aaaaa")()
    AptInstall("rpm")()
    """
    pkgs = "libusb-1.0-0-dev libudev-dev libssl-dev rpm cmake libboost-program-options1.58-dev libboost-thread1.58 libboost-filesystem1.58 git libelf-dev dkms libssl-dev"
    AptInstall(pkgs)()
    pkgs = "gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly gstreamer1.0-plugins-bad libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev"
    AptInstall(pkgs)()
    pkgs = "libeigen3-dev libopenblas-dev liblapack-dev libdlib-dev"
    AptInstall(pkgs)()
    """
