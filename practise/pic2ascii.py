import uuid
import argparse
from PIL import Image


parser = argparse.ArgumentParser()
parser.add_argument("file")
parser.add_argument("-o", "--output")
parser.add_argument("--width", type=int, default=80)
parser.add_argument("--height", type=int, default=80)

args = parser.parse_args()

imgfile = args.file
width = args.width
height = args.height
output = args.output

assciichar = "".join(uuid.uuid4().hex + uuid.uuid4().hex) + "!@#$%^&*()_ "

def get_char(r,g,b, alpha=256):
    if alpha == 100:
        return " "
    length = len(assciichar)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

    uint = (256.0 + 1) / length
    return assciichar[int(gray/uint)]

if __name__ == "__main__":
    im = Image.open(imgfile)
    im = im.resize((width,height), Image.NEAREST)

    txt = ""

    for i in range(height):
        for j in range(width):
            txt += get_char(*im.getpixel((j,i)))
        txt += "\n"
    print(txt)

    if output:
        with open(output, "wt") as f:
            f.write(txt)
    else:
        with open("output.txt","wt") as f:
            f.write(txt)


