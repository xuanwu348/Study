import os
import time
import sys

sys.stdout.write("\rplease input:\n")
asd = sys.stdin.read(2)
sys.stdout.write("\r" + asd + "\n")
if asd.strip() == "a":
    sys.stdout.write("\rab:\n")
    sdf = sys.stdin.read(2)
    sys.stdout.write("\r%s\n" % sdf)
    if sdf.strip() == "a":
        cde = input("b:")
        if cde == "b":
            exit
        else:
            input("c:")
    else:
        input("d:")
else:
    input("f:")

