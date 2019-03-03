#encoding:utf-8
from flask import Flask, send_from_directory, abort, render_template
import os
import random
import sys

app = Flask(__name__)


if sys.version_info.major !=3:
    raise Exception("Please use python with version greater or equal 3.4")

namelists = {}
for dirname, temp, filenames in os.walk("./"):
    for name in filenames:
        if name.endswith(("mp4","pdf","txt","docx","doc","jpg","bmp","png","log")):
            temp_path = os.path.join(dirname, name).replace("\\", "/") if sys.platform == "win32" else os.path.join(dirname, name)              
            if name in namelists.keys():
                namelists[name + str(random.randint(0,9))] = temp_path
            else:
                namelists[name] = temp_path

@app.route("/")
def index():
    content = ""
    for name in namelists.keys():
        content += '<a href="{0}">{0}</a></br>'.format(name)
    return content

@app.route("/<name>", methods=["GET"])
def sendFile(name):
    try:
        if os.path.isfile(namelists[name]):
            if name.endswith(".mp4"):
                return render_template("player.html",filep=namelists[name])
            return send_from_directory("./", namelists[name], as_attachment=True)
    except KeyError as e:
        print("\033[32m{} KeyError\033[0m".format(name.encode("utf-8")))
        pass
    abort(404)
    
if __name__ == "__main__":
    app.run(("0.0.0.0"),debug = True)
