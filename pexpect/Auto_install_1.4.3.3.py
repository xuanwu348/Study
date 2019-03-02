#encoding:utf-8

import os
import subprocess
import sys
if int(sys.version[:1]) < 3:
    print("\033[33mPlease use python3.x!\033[0m\n")
    exit()
import time
import threading
import re
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
from datetime import datetime
import pickle
import queue
q = queue.Queue()

class AptInstall():
    def __init__(self, pkgnames):
        self.pkgnames = pkgnames.strip()
        self.passwd = passwd
    
    def password(self, child):
        child.sendline(self.passwd)

    @staticmethod
    def installed_or_fail(child, pkgnames):
        res_fail = re.compile("fail|Fail|error|Error")
        res_unable = re.compile("administration")
        pkg = pkgnames.strip().split()[0]
        while 1:
            with open("{}/apt_{}.log".format(installed_log, pkg),"rt") as f:
                content = f.read()
                fail_info = res_fail.findall(content)
                unable_info = res_unable.findall(content)
                pid = os.popen('ps -ef|grep "apt-get install -y {}"|grep -v grep'.format(pkg)).read()
                if pid:
                    time.sleep(1)
                    continue
                if content.find("newly installed") != -1 and not fail_info :
                    print("\033[32mInstall {} successfully\033[0m\n".format(pkgnames))
                    saveresult(pkgnames)
                    break
                elif fail_info:
                    print("fail_info:",pkgnames,fail_info)
                    break
                elif unable_info:
                    cmd = '''for pid in `ps -ef|grep -n "apt-get"|grep -v grep|awk '{print $2}'`;do kill -9 $pid;done'''
                    os.system("echo {}|sudo rm -rf  {}/apt_{}.log".format(passwd, installed_log, pkg))
                    time.sleep(1)
                    child.sendline("apt-get install -y {} > {}/apt_{}.log 2>&1".format(pkgnames, installed_log, pkg))
                    time.sleep(3)
                    print("\033[34mTry again.......\033[0m\n")
                else:
                    time.sleep(0.5)
                    continue


    def __call__(self):
        pkg = self.pkgnames.strip().split()[0]
        cmd = "apt-get install -y {} > {}/apt_{}.log 2>&1".format(self.pkgnames, installed_log, pkg)
        #child = pexpect.spawn("sudo bash", encoding="utf-8", logfile=sys.stdout)
        try:
            child = pexpect.spawn("sudo bash")
            q.put("1")
            watchstatus(self.pkgnames)
            index = child.expect(["#","password"])
            if index == 0:
                child.sendline(cmd)
                time.sleep(2)
                self.installed_or_fail(child, self.pkgnames)
            elif index ==1:
                self.password(child)
                child.sendline(cmd)
                time.sleep(2)
                self.installed_or_fail(child, self.pkgnames)
        finally:
            while not q.empty():
                q.get()
            time.sleep(1)

def decorate_th(f):
    @wraps(f)
    def w(*args, **kwargs):
        t = threading.Thread(target=f, args=args, kwargs=kwargs)
        t.start()
    return w

@decorate_th
def watchstatus(pkg):
    while not q.empty():
        sys.stdout.write("\r{} installing {}...... ".format(time.ctime(), pkg[:20]))
        time.sleep(0.5)

def split_line(processing):
    print("\033[33m" +  "-----"* 10 + "\033[0m\n")
    print(" " * (int((50 - len(processing))/2)) + str(processing) + " " * (int((50 - len(processing))/2)) + "\n")
    print("\033[33m" +  "-----"* 10 + "\033[0m\n")

class cd():
    def __init__(self, path):
        self.path = path
    def __enter__(self):
        os.chdir(self.path)
    def __exit__(self, exc_type, exc_value, trace):
        os.chdir(BASE_DIR)

def install_sh(child, pkg="unknown"):	
    index = child.expect(["Y/n",'Unable','already',"Processing","#", pexpect.TIMEOUT, pexpect.EOF])
    if index == 0:
        child.sendline("Y")
        child.wait()
        index = child.expect(["installed", pexpect.TIMEOUT, pexpect.EOF, "Processing"])
        if index in [0,3]:
            print("\033[32mInstall {} successfully\033[0m\n".format(pkg))
            saveresult(pkg)
        elif index == 1:
            print("\033[33mTimeout\033[0m\n")
        elif index == 2:
            print("\033[32mEOF\033[0m\n")
    elif index in [2,3,4,6]:
        print("\033[32mInstall {} successfully\033[0m\n".format(pkg))
        saveresult(pkg)
    elif index == 1:
        print("\033[33mSome problem may occurred during install {}\033[0m\n".format(pkg))
    elif index == 5:
        print("\033[33mTimeout\033[0m\n")

def sendline(child,command):
    child.expect("#")
    child.sendline(command)

def install_kernel(child):
    while 1:
        child.sendline("./install_4_14_kernel.sh |tee {}/install_kernel.log".format(installed_log))
        child.expect(["ENTER"])
        child.sendline("\n")
        time.sleep(4)
        output = os.popen("ps -ef|grep install_4_14_kernel.sh|grep -v grep").read()
        while output:
             output = os.popen("ps -ef|grep install_4_14_kernel.sh|grep -v grep").read()
             sys.stdout.write("\r{} please wait for install kernel.......".format(time.ctime()))
             time.sleep(1)
        res_already = re.compile("already")
        res_reboot =re.compile("reboot")
        with open("{}/install_kernel.log".format(installed_log),'rt') as f: 
            content = f.read()
        if res_already.findall(content):
            print("\n\r\033[32mKernel has installed\033[0m\n")
            saveresult("kernel")
            break
        if res_reboot.findall(content):
            print("\033[32m\n\rInstall completed will reboot after 5s...\033[0m\n")
            saveresult("kernel")
            time.sleep(5)
            #child.sendline("reboot")
            os.system("echo {}|sudo -S reboot".format(passwd))
        time.sleep(1)
        print("\n\r\033[33mTry again to install kernel.......\033[0m\n")

def saveresult(pkg):
    global result_data
    with open(result_picklefile,"wb") as f:
        if pkg not in result_data:
            result_data.append(pkg)
            print("\n\033[32mHas install below options:\033[0m\n\r\033[33m{}\033[0m\n".format(",".join(result_data)))
            pickle.dump(result_data,f)
            print("-----"*10 + "\n")


if __name__ == "__main__":
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    result_picklefile = os.path.join(BASE_DIR,"Installed_result.dat")
    try:
        with open(result_picklefile, "rb") as f:
            result_data = pickle.load(f)
    except (FileNotFoundError, EOFError) as e:
        print(e,"\nCreating the file......")
        result_data = []
        with open(result_picklefile,"wb") as f:
            pickle.dump(result_data, f)

    HOME_PATH = os.getenv("HOME")
    username = "hddl"
    passwd = "intel123"
    HOSTNAME = "xxxxxxx"
    proxy = "http://child-prc.intel.com:913"
    openvino_install_path = "/opt/intel/computer_vision_sdk/"
    openvino_tgz = "/home/hddl/ww51_openvino/l_openvino_toolkit_p_2018.5.445.tgz"
    opencl_gz = "/home/hddl/ww51_openvino/intel_sdk_for_opencl_2017_7.0.0.2568_x64.gz"
    HDDLs_rpm = "/home/hddl/ww51_openvino/Intel_Movidius_MyriadX_HDDL-S_Linux-BetaV1.2-ww03_2019.x86_64.rpm"
    src_certificate = "/home/hddl/ww51_openvino/certificate"
    dst_server_cer = ""
    dst_control_cer = ""
    dst_receive_cer = ""
    hddls_server_controller_receiver = "/home/hddl/ww51_openvino"
    installed_log = os.path.join(BASE_DIR, "install_log")
    filename_self = os.path.abspath(__file__)
    if not os.path.exists(installed_log):
        os.system("mkdir {}".format(installed_log))
    bashrc_file = os.path.join(HOME_PATH, ".bashrc")
    cmd_for_reboot = "python3 {}".format(filename_self)
    output = os.popen("cat {}".format(bashrc_file)).read().strip()
    if "kernel" in result_data:
        if output.find(cmd_for_reboot) != -1:
            cmd_ = "sed -i -e 's#{}#\##g' {}".format(cmd_for_reboot, bashrc_file)
            os.system(cmd_)
    else:
        if output.find(cmd_for_reboot) != -1:
            pass
        else:
            with open(bashrc_file, "at") as f:
                f.write(cmd_for_reboot)


    
    #Install dependence package
    if "dependencePkg" not in result_data:
        split_line("Apt install")
        time.sleep(1)
        AptInstall("nload")()
        pkgs = "libusb-1.0-0-dev libudev-dev libssl-dev rpm cmake libboost-program-options1.58-dev libboost-thread1.58 libboost-filesystem1.58 git libelf-dev dkms libssl-dev"
        AptInstall(pkgs)()
        pkgs = "gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly gstreamer1.0-plugins-bad libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev"
        AptInstall(pkgs)()
        pkgs = "libeigen3-dev libopenblas-dev liblapack-dev libdlib-dev"
        AptInstall(pkgs)()
        saveresult("dependencePkg") 
    
    """
    #Install Openvino
    if "openvino" not in result_data:
        split_line("Install Openvino")
        time.sleep(1)
        openvino_install_package = openvino_tgz[:openvino_tgz.rfind(".")]
        if os.path.exists(openvino_install_package):
            os.system("rm -rf {}".format(openvino_install_package))
        with cd(os.path.dirname(openvino_tgz)):
            os.system("tar -xvf {}".format(openvino_tgz))
        with cd(openvino_install_package):
            child = pexpect.spawn("sudo bash", encoding="utf-8",logfile=sys.stdout)    
            index = child.expect(["#","password"])
            if index == 0:
                child.sendline("./install_cv_sdk_dependencies.sh")
                install_sh(child,"cv_sdk_dependencies")
            elif index == 1:
                child.sendline(passwd)
                index = child.expect(["#"])
                if index == 0:
                    child.sendline("./install_cv_sdk_dependencies.sh")
                    install_sh(child,"cv_sdk_dependencies")
            cmd_ = "sed -i -e 's#ACCEPT_EULA=decline#ACCEPT_EULA=accept#g' silent.cfg"
            child.sendline(cmd_)
            child.expect(["#"])
            child.sendline("./install.sh -s silent.cfg")
            time.sleep(5)
            output = os.popen("ps -ef|grep silent.cfg|grep -v grep").read()
            while output:
                output = os.popen("ps -ef|grep silent.cfg|grep -v grep").read()
                time.sleep(2)
                sys.stdout.write("\r\033[32m{} It's installing openvino.....\033[0m".format(time.ctime()))
            print("\033[32m\n\rInstall openvino done\033[0m\n")
            sendline(child,"ln -sf /opt/intel/mediasdk/lib64/libva.so.2 /usr/lib/libva.so")
            sendline(child,"ln -sf /opt/intel/mediasdk/lib64/libva-drm.so.2 /usr/lib/libva-drm.so")
            res = re.compile("setupvars.sh")
            output = os.popen("cat %s/.bashrc" % HOME_PATH).read()
            with open("%s/.bashrc" % HOME_PATH, "at") as f:
                if not res.findall(output):
                    f.write(". /opt/intel/computer_vision_sdk/bin/setupvars.sh")
            child.close(force=True)
            saveresult("openvino")


    #install kernel
    if "kernel" not in result_data:
        split_line("Upgrade kernel")
        time.sleep(1)
        with cd(openvino_install_path + "install_dependencies"):
            child = pexpect.spawn("sudo bash", encoding="utf-8",logfile=sys.stdout)
            index = child.expect(["#","password"])
            if index == 0:
                child.sendline("./install_NEO_OCL_driver.sh")
                install_sh(child,"NEO_OCL_driver")
            elif index == 1:
                child.sendline(passwd)
                index = child.expect(["#"])
                if index == 0:
                    child.sendline("./install_NEO_OCL_driver.sh")
                    install_sh(child,"NEO_OCL_driver.sh")
            sendline(child,"usermod -a -G video {}".format(username))
            res = re.compile("i915")
            with open("/etc/default/grub", "rt") as f:
                if not res.findall(f.read()):
                    sendline(child,"sed -i -e 's#quiet splash#quiet splash i915.alpha_support=1#g' /etc/default/grub")
                    sendline(child,"update-grub")
                    child.expect(["done","#"])
                    print("\n\r\033[32mUpdate grub done\033[0m\n")
            install_kernel(child)
            child.close()
            saveresult("kernel")

    #Additional Installation Steps for Intel® Vision Accelerator Design with Intel® Movidius™ VPUs
    if "VPU" not in result_data:
        split_line("Additional Installation Steps for Intel® Vision Accelerator Design with Intel® Movidius™ VPUs")
        pkgs = "libusb-1.0-0 libboost-program-options1.58.0 libboost-thread1.58.0 libboost-filesystem1.58.0 libssl1.0.0 libudev1 libjson-c2"
        AptInstall(pkgs)()
        HDDL_INSTALL_DIR = os.getenv("HDDL_INSTALL_DIR")
        with cd(HDDL_INSTALL_DIR):
            child = pexpect.spawn("sudo bash",encoding="utf-8",logfile=sys.stdout)
            index = child.expect(["#","password"])
            if index == 0:
                child.sendline("usermod -a -G user {}".format(username)) 
            elif index == 1:
                child.sendline(passwd)
                index = child.expect(["#"])
                child.sendline("usermod -a -G user {}".format(username))
            sendline(child,"chmod +x ./generate_udev_rules.sh")
            sendline(child,"./generate_udev_rules.sh /etc/udev/rules.d/98-hddlbsl.rules")
            sendline(child,'sed -i "s/\(.*i2c_i801$\)/#\1/g" /etc/modprobe.d/blacklist.conf')
            sendline(child,"modprobe i2c_i801")
            cmd = '''for pid in `ps -ef|grep -n "hddldaemon\|autoboot"|grep -v grep|awk '{print $2}'`;do kill -9 $pid;done'''
            os.system(cmd)
            sendline(child,"cd drivers")
            sendline(child,"chmod +x ./setup.sh")
            sendline(child,"./setup.sh install| tee {}/hddl_driver_install.log".format(installed_log))
            time.sleep(3)
            cmd = "ps -ef|grep setup.sh|grep -v grep"
            output = os.popen(cmd).read()
            while output:
                 output = os.popen(cmd).read()
                 sys.stdout.write("\r{} please wait for install hddl driver.......".format(time.ctime()))
                 time.sleep(1)
            res_installed = re.compile("installed")
            with open("{}/hddl_driver_install.log".format(installed_log), "rt") as f:
                content = f.read()
            if len(res_installed.findall(content)) >= 2:
                print("\n\r\033[32mDriver install done\033[0m\n")
            else:
                print("\n\r\033[33mDriver install occurred some problem, please install by mannual\033[0m\n")
            INTEL_CVSDK_DIR = os.getenv("INTEL_CVSDK_DIR")
            child.sendline("cd {}".format(INTEL_CVSDK_DIR))
            sendline(child,'cp -av $(find -name "*.rules") /etc/udev/rules.d/')
            sendline(child,"udevadm control --reload-rules")
            sendline(child,"udevadm trigger")
            sendline(child,"ldconfig")
            child.expect("#")
            child.close(force=True)
            output = os.popen("lsmod|grep my").read().split()
            if 'myd_vsc' in output and 'myd_ion' in output:
                print("\n\r\033[32mFind myd_vsc and myd_ion\033[0m\n")
            else:
                print("\n\r\033[32mDon't find myd_vsc and myd_ion, please check driver install\033[0m\n")
            saveresult("VPU")


    if "opencl" not in result_data:
        split_line("Install opencl")
        time.sleep(1)
        AptInstall("dkms")()
        opencl_install_path = opencl_gz[:opencl_gz.rfind(".")]
        
        if os.path.exists(opencl_install_path):
            os.system("rm -rf {}".format(opencl_install_path))
        with cd(os.path.dirname(opencl_gz)):
            os.system("tar -xvf {}".format(opencl_gz))
        
        with cd(opencl_install_path):
            child = pexpect.spawn("sudo bash")
            index = child.expect(["#","password"])
            if index == 0:
                child.sendline("./install.sh |tee {}/install_opencl.log".format(installed_log))
            elif index == 1:
                child.sendline(passwd)
                child.expect("#")
                child.sendline("./install.sh |tee {}/install_opencl.log".format(installed_log))
            child.expect("quit")
            child.sendline("1")
            time.sleep(1)
            while 1:
                index = child.expect(["menu: ","\w+\\n\\r"])
                if index == 0:
                    child.sendline("accept")
                    time.sleep(0.5)
                    break
                elif index == 1:
                    child.sendline(" ")
                    continue
            with open("{}/install_opencl.log".format(installed_log),"rb") as f:
                f.read()
                file_position = f.tell()
            res_enter = re.compile('Start installation Now')
            while 1:
                with open("{}/install_opencl.log".format(installed_log), "rb") as f:
                    f.seek(file_position)
                    content = f.read()
                    if res_enter.findall(content.decode("utf-8")):
                        file_position = f.tell()
                        break 
                    sys.stdout.write("\r{} checking the prerequisites. It can take several minutes. Please wait...".format(time.ctime()))
                    time.sleep(0.5)
            print("\n\r")
            child.expect('"Enter"')
            child.sendline("1\n")
            child.expect('"Enter"')
            child.sendline("1\n")
            time.sleep(10)
            child.expect('"Enter"')
            child.sendline(" ")
            child.expect('"Enter"')
            child.sendline(" ")
            res_Complete = re.compile('Complete')
            while 1:
                with open("{}/install_opencl.log".format(installed_log), "rb") as f:
                    f.seek(file_position)
                    content = f.read()
                    if res_Complete.findall(content.decode("utf-8")):
                        print("\033[32mInstall complete!\033[0m")
                        break
                sys.stdout.write("\r{} Wait to complete ....".format(time.ctime()))
                time.sleep(0.5)
            saveresult("opencl") 


    #Install json_c
    if "Json_c" not in result_data:
        split_line("Json_c")
        time.sleep(1)
        pkgs = "git autoconf libtool"
        AptInstall(pkgs)()
        with cd(HOME_PATH):
            os.system("git clone https://github.com/json-c/json-c.git")
            os.chdir("json-c")
            os.system("git checkout f8c632f579c71012f9aca81543b880a579f634fc")
            os.system("sh autogen.sh")
            os.system("./configure && make")
            os.system("echo {}|sudo -S make install".format(passwd))
            saveresult("Json_c") 


    #install uWebSocket
    if "uWebSocket" not in result_data:
        split_line("uWebSocket")
        time.sleep(1)
        AptInstall("libssl-dev")()
        with cd(HOME_PATH):
            os.system("git clone https://github.com/uNetworking/uWebSockets.git")
            os.chdir("uWebSockets")
            os.system("git checkout 1a126c8d4eb9127c2689ede9a8fdf8abcb62b981")
            os.system("make")
            os.system("echo {}|sudo -S make install".format(passwd))
            saveresult("uWebSocket")
  

    #Install OpenCV
    if "OpenCV" not in result_data:
        split_line("Install Opencv")
        time.sleep(1)
        os.system("echo {}|sudo -S ln -sf /opt/intel/opencl/SDK/include /opt/intel/opencl/include".format(passwd))
        os.system("echo {}|sudo -S ln -sf /opt/intel/mediasdk/include/va /usr/local/include/va".format(passwd))
        with cd(HOME_PATH):
            os.system("git clone https://github.com/opencv/opencv.git")
            os.chdir("opencv")
            os.system("git checkout 6ffc48769ac60d53c4bd1913eac15117c9b1c9f7")
            os.system("mkdir build")
            os.chdir("build")
            os.system("export CPLUS_INCLUDE_PATH=/opt/intel/mediasdk/include:$CPLUS_INCLUDE_PATH;cmake -DWITH_VA_INTEL=ON -DWITH_IPP=OFF -DWITH_CUDA=OFF ..;make -j8")
            os.system("echo {}|sudo -S make install".format(passwd))
        saveresult("OpenCV")  


    #Set enviroment variables
    if "SetENV" not in result_data:
        split_line("Set enviroment variables")
        time.sleep(1)
        envs = [r"LD_LIBRARY_PATH=/usr/local/lib:/opt/intel/computer_vision_sdk_2018.5.445/deployment_tools/inference_engine/external/hddl/lib:$LD_LIBRARY_PATH",
                r"PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/opt/intel/mediasdk/lib64/pkgconfig",
                r"LD_LIBRARY_PATH=/opt/intel/mediasdk/lib64:/opt/intel/computer_vision_sdk/inference_engine/lib/ubuntu_16.04/intel64:$LD_LIBRARY_PATH",
                r"LD_LIBRARY_PATH=/opt/intel/computer_vision_sdk_2018.5.445/deployment_tools/inference_engine/external/omp/lib:/usr/lib/x86_64-linux-gnu/gstreamer-1.0:$LD_LIBRARY_PATH",
                r"HDDLS_CVDL_KERNEL_PATH=/usr/lib/x86_64-linux-gnu/libgstcvdl/kernels",
                r"PATH=$PATH:/opt/intel/mediasdk/bin/"]
        with open("%s/.bashrc" % HOME_PATH, "at") as f:
            content = os.popen("cat %s/.bashrc" % HOME_PATH).read()
            for env in envs:
                if content.find(env) != -1:
                    continue
                else:
                    f.write("export" + " " + env + "\n")
            saveresult("SetENV")
        print("\033[32mSet enviroment variables done\033[0m\n")



    #Install hddls
    if "hddls" not in result_data:
        split_line("Install hddls")
        time.sleep(1)
        os.system("echo {}|sudo -S rpm -ivh --nodeps {}".format(passwd, HDDLs_rpm))
        AptInstall("nodejs-legacy npm")()
        child = pexpect.spawn("sudo bash", encoding="utf-8", logfile=sys.stdout)
        index = child.expect(["#","password"])
        if index == 0:
            child.sendline("npm config set proxy {}".format(proxy))
        elif index == 1:
            child.sendline(passwd)
            sendline(child,"npm config set proxy {}".format(proxy))
        sendline(child,"npm install -g n")
        time.sleep(5)
        sendline(child,"n stable")
        time.sleep(10)
        with cd(hddls_server_controller_receiver):
            sendline(child,"npm install")
            time.sleep(10)
        child.close(force=True)
        saveresult("hddls")
    """    
    


    #About certificate
    if "certificate" not in result_data:
        split_line("certificate")
        time.sleep(1)
        res_hostname = re.compile(HOSTNAME)
        output = os.popen("cat /etc/hosts").read().strip()
        if res_hostname.findall(output):
            pass
        else:
            child = pexpect.spawn("sudo bash")
            index = child.expect(["#","password"])
            if index == 0:
                child.sendline('echo "127.0.0.1   {}" >> /etc/hosts'.format(HOSTNAME))
            elif index == 1:
                child.sendline(passwd)
                child.expect("#")
                child.sendline('echo "127.0.0.1   {}" >> /etc/hosts'.format(HOSTNAME))
            child.expect("#")
            child.close(force=True)
        print("\n\rcp sertificate\033[0m\n")
        #os.system("cp -r {}/server/ {}".format(src_certificate, dst_server_cer))
        #os.system("cp -r {}/client/ {}".format(src_certificate, dst_control_cer))
        #os.system("cp -r {}/client/ {}".format(src_certificate, dst_receive_cer))
        saveresult("certificate")

    print("\n\r\033[33mAll contents were installed\033[0m\n")
    print("\n\033[32mHas installied below options:\033[0m\n\r\033[33m{}\033[0m\n".format(", ".join(result_data)))

