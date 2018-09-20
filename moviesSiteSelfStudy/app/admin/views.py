#_*_conding:utf-8_*_

from . import admin
from flask import render_template, redirect, url_for

@admin.route("/")
def index():
    return render_template("admin/index.html")

@admin.route("/login/")
def login():
    return render_template("admin/login.html")

@admin.route("/logout/")
def logout():
    return redirect(url_for("admin.login"))

@admin.route("/pwd/")
def pwd():
    return render_template("admin/pwd.html")

@admin.route("/tag/tag_add")
def tag_add():
    return render_template("admin/tag_add.html")

@admin.route("/tag/tag_list")
def tag_list():
    return render_template("admin/tag_list.html")


