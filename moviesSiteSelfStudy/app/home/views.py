#_*_ encoding:utf-8 _*_
from . import home
from flask import render_template


@home.route("/")
def index():
    return render_template("home/index.html")
