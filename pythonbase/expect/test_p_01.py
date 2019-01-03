import os
import time
import sys

sys.stdout.write("\rplease input:\n")
asd = sys.stdin.read(2)
if asd.strip() == "a":
    sys.stdout.write("\rab:\n")
    sdf = sys.stdin.read(2)
    if sdf.strip() == "a":
        sys.stdout.write("b:\n")
        cde = sys.stdin.read(2)
        if cde.strip() == "b":
            #output = os.popen("uname -a")
            sys.stdout.write("asdffffaffa:1,2,3\n")
            asdf = input(">")
            
        else:
            input("c:")
    else:
        input("d:")
else:
    input("f:")

