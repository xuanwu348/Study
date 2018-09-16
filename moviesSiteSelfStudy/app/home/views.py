#_*_ encoding:utf-8 _*_
from . import home


@home.route("/")
def index():
    return "<h1 style='color:green'> this is home<h1>"
