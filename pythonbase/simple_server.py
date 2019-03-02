#encoding:utf-8
from flask import Flask, send_from_directory, abort
import os
import random
import sys

app = Flask(__name__)

namelists = {}
for dirname, temp, filenames in os.walk("./"):
    for name in filenames:
        if name.endswith(("mp4","pdf","txt","docx","doc","jpg","bmp","png")):
            temp_path = os.path.join(dirname, name).replace("\\", "/") if sys.platform == "win32" else os.path.join(dirname, name)              
            if name in namelists.keys():
                namelists[name + str(random.randint(0,9))] = temp_path
            else:
                namelists[name] = temp_path

@app.route("/")
def index():
    content = ""
    for name in namelists.keys():
        content += "<a href=./{0}>{0}</a></br>".format(name)
    return content

@app.route("/<string:name>", methods=["GET"])
def sendFile(name):
    if os.path.isfile(namelists[name]):
        return send_from_directory("./", namelists[name], as_attachment=True)
    abort(404)
    
if __name__ == "__main__":
    app.run(("0.0.0.0"),debug = True)
