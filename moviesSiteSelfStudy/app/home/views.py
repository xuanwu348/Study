#_*_ encoding:utf-8 _*_
from . import home
from flask import render_template, redirect, url_for, session, flash, request
from app.home.form import RegistForm, LoginForm, UserdetailForm
import uuid
from app.models import User,Userlog
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from app import db, app
from functools import wraps
import datetime
import os

def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename

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

@home.route("/user/", methods=["GET","POST"])
@user_login_req
def user():
    form = UserdetailForm()
    user = User.query.filter_by(id=session["user_id"]).first()
    if request.method == "GET":
        form.name.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
        if user.face:
            form.face.data = user.face
            form.face.validators.clear()
        form.info.data = user.info
    if form.validate_on_submit():
        data = form.data
        try:
            file_face = secure_filename(form.face.data.filename)
        except AttributeError:
            file_face = secure_filename(form.face.data)
        print(file_face)
        user.face = change_filename(file_face)
        user_count = User.query.filter_by(name=data["name"]).count()
        if user.name != data["name"] and user_count == 1:
            flash("昵称已存在","err")
            return redirect(url_for("home.user"))
        user.name = data["name"]
        phone_count = User.query.filter_by(phone=data["phone"]).count()
        if user.phone != data["phone"] and phone_count == 1:
            flash("手机号码已存在",'err')
            return redirect(url_for("home.user"))
        user.phone = data["phone"]
        email_count = User.query.filter_by(email=data["email"]).count()
        if user.email != data["email"] and email_count == 1:
            flash("邮箱已经存在",'err')
            return redirect(url_for("home.user"))
        user.email = data["email"]
        user.info = data["info"]
        if not os.path.exists(app.config["FC_DIR"]):
            os.makedirs(app.config["FC_DIR"])
            os.chmod(app.config["FC_DIR"],"rw")
        try:
            form.face.data.save(app.config["FC_DIR"] + user.face)
        except AttributeError:
            form.face.save(app.config["FC_DIR"] + user.face)
        db.session.add(user)
        db.session.commit()
        flash("修改资料成功！", "OK")
        return redirect(url_for("home.user"))
    return render_template("home/user.html", form = form, user = user)

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



