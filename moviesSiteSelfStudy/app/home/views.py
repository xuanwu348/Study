#_*_ encoding:utf-8 _*_
from . import home
from flask import render_template, redirect, url_for, session, flash
from app.home.form import RegistForm
import uuid
from app.models import User
from werkzeug.security import generate_password_hash
from app import db

@home.route("/")
def index():
    return render_template("home/index.html")

@home.route("/login/")
def login():
    return render_template("home/login.html")

@home.route("/logout/")
def logout():
    return redirect(url_for("home.login"))

@home.route("/regist/", methods=["GET","POST"])
def regist():
    form = RegistForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
                name = data["name"],
                pwd = generate_password_hash(data['pwd']),
                email = data['email'],
                phone = data["phone"],
                uuid = uuid.uuid4().hex,
                )
        db.session.add(user)
        db.session.commit()
        flash("注册成功！", "OK")
        session['user'] = data["name"]
        user_id = User.query.filter_by(name=data['name']).first()
        session['user_id'] = user_id.id
        return redirect(url_for('home.user'))
    return render_template("home/regist.html", form = form)

@home.route("/user/")
def user():
    return render_template("home/user.html")

@home.route("/pwd/")
def pwd():
    return render_template("home/pwd.html")

@home.route("/loginlog/")
def loginlog():
    return render_template("home/loginlog.html")

@home.route("/comments/")
def comments():
    return render_template("home/comments.html")

@home.route("/moviecol")
def moviecol():
    return render_template("home/moviecol.html")

@home.route("/animation/")
def animation():
    return render_template("home/animation.html")

@home.route("/search")
def search():
    return render_template("home/search.html")

@home.route("/play")
def play():
    return render_template("home/play.html")



