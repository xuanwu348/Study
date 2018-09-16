#_*_conding:utf-8_*_

from . import admin

@admin.route("/")
def index():
    return "<h1 style='color:red'>this is admin<h1>"
