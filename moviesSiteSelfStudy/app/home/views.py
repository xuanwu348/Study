#_*_ encoding:utf-8 _*_
from . import home
from flask import render_template, redirect, url_for, session, flash, request
from app.home.form import RegistForm, LoginForm
import uuid
from app.models import User,Userlog
from werkzeug.security import generate_password_hash
from app import db
from functools import wraps

def user_login_req(f):
    @wraps(f)
    def decorate_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("home.login", next=request.url))
        return f(*args,**kwargs)
    return decorate_function

@home.route("/")
def index():
    return render_template("home/index.html")

@home.route("/login/", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data["account"]).first()
        if not user:
            flash("登录失败，账号或者密码错！","err")
            return redirect(url_for("home.login"))
        if not user.check_pwd(data["pwd"]):
            flash("登录失败，账号或者密码错！","err")
            return redirect(url_for("home.login"))
        session["user"] = data["account"]
        session["user_id"] = user.id
        flash("登录成功", "OK")
        userlog = Userlog(
                user_id = user.id,
                ip = request.remote_addr,
                )
        db.session.add(userlog)
        db.session.commit()
        return redirect(url_for("home.user"))
    return render_template("home/login.html", form = form)

@home.route("/logout/")
def logout():
    session.pop("user",None)
    session.pop("user_id", None)
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
        flash("注册成功！请登录......", "OK")
        return redirect(url_for('home.login'))
    return render_template("home/regist.html", form = form)

@home.route("/user/")
@user_login_req
def user():
    return render_template("home/user.html")

@home.route("/pwd/")
@user_login_req
def pwd():
    return render_template("home/pwd.html")

@home.route("/loginlog/")
@user_login_req
def loginlog():
    return render_template("home/loginlog.html")

@home.route("/comments/")
@user_login_req
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



