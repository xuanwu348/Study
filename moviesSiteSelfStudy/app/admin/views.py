#coding:utf8

from . import admin
from flask import render_template, redirect, url_for, flash, session, request
from app.admin.forms import LoginForm, TagForm, MovieForm, PreviewForm
from app.models import Admin, Tag, Movie, Preview, User
from functools import wraps
from app import db, app
from werkzeug.utils import secure_filename
import uuid
import datetime
import os

def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function 

def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename



@admin.route("/")
@admin_login_req
def index():
    return render_template("admin/index.html")

@admin.route("/login/", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data["account"]).first()
        if not admin.check_pwd(data["pwd"]):
            flash("账号或者密码错误！")
            return redirect(url_for("admin.login"))
        session["admin"] = data["account"]
        return redirect(request.args.get("next") or url_for("admin.index"))
    return render_template("admin/login.html", form=form)

@admin.route("/logout/", methods=["POST","GET"])
@admin_login_req
def logout():
    session.pop("admin", None)
    return redirect(url_for("admin.login"))

@admin.route("/pwd/")
@admin_login_req
def pwd():
    return render_template("admin/pwd.html")

@admin.route("/tag/tag_add", methods=["POST","GET"])
@admin_login_req
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag = Tag.query.filter_by(name=data["name"]).count()
        if tag == 1:
            flash('名称"%s"已经存在' % data['name'], "err")
            return redirect(url_for("admin.tag_add"))
        tag = Tag(
                name = data["name"]
                )
        db.session.add(tag)
        db.session.commit()
        flash('标签名"%s"添加成功' % data['name'],"OK")
        redirect(url_for("admin.tag_add"))
    return render_template("admin/tag_add.html", form = form)

@admin.route("/tag/tag_list/<int:page>/", methods=["GET"])
@admin_login_req
def tag_list(page=None):
    if page is None:
        page = 1
    page_data = Tag.query.order_by(
            Tag.addtime.desc()
            ).paginate(page=page, per_page=10)
    return render_template("admin/tag_list.html", page_data = page_data)

@admin.route("/tag/del/<int:id>", methods=["GET"])
@admin_login_req
def tag_del(id=None):
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash("删除标签%s成功" % tag.name,"OK")
    return redirect(url_for("admin.tag_list", page=1))

@admin.route("/tag/edit/<int:id>/", methods=["POST", "GET"])
@admin_login_req
def tag_edit(id):
    form = TagForm()
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        tag_count = Tag.query.filter_by(name=data["name"]).count()
        if tag.name != data['name'] and tag_count == 1:
            flash("标签名称%s已经存在" % tag.name, "err")
            return redirect(url_for('admin.tag_edit', id=id))
        tag.name = data["name"] 
        db.session.add(tag)
        db.session.commit()
        flash("修改标签名%s成功" % tag.name, "OK")
        return redirect(url_for('admin.tag_add'))
    return render_template("admin/tag_edit.html", form = form, tag=tag)

@admin.route("/movie/add", methods=["POST", "GET"])
@admin_login_req
def movie_add():
    form = MovieForm()
    if form.validate_on_submit():
        data = form.data
        file_url = secure_filename(form.url.data.filename)
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")
        url = change_filename(file_url)
        logo = change_filename(file_logo)
        form.url.data.save(app.config["UP_DIR"] + url)
        form.logo.data.save(app.config["UP_DIR"] + logo)

        movie = Movie(
                title = data["title"],
                url = url,
                info = data["info"],
                logo = logo,
                star = int(data["star"]),
                playnum = 0,
                commentnum = 0,
                tag_id = int(data["tag_id"]),
                area = data["area"],
                release_time = datetime.datetime(*(list(map(int,data["release_time"].split("-"))))),
                length = data["length"]
                )
        db.session.add(movie)
        db.session.commit()
        flash("添加电影%s成功" % data["title"], "OK")
        return redirect(url_for("admin.movie_add")) 
    return render_template("admin/movie_add.html", form = form)

@admin.route("/movie/edit/<int:id>/", methods=["POST", "GET"])
@admin_login_req
def movie_edit(id=None):
    form = MovieForm()
    form.url.validators.clear() #= []
    form.logo.validators.clear() # = []
    movie = Movie.query.get_or_404(int(id))
    if request.method == "GET":
        form.info.data = movie.info
        form.tag_id.data = movie.tag_id
        form.star.data = movie.star
    if form.validate_on_submit():
        data = form.data
        movie_count = Movie.query.filter_by(title=data["title"]).count()
        if movie_count == 1 and movie.title != data["title"]:
            flash("片名%s已经存在！" % data["title"], "err")
            return redirect(url_for("admin.movie_edit",id = id))
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIT"], "rw")
        if form.url.data != "":
            file_url = secure_filename(form.url.data.filename)
            url = change_filename(file_url)
            form.url.data.save(app.config["UP_DIR"] + url)
        if form.logo.data != "":
            file_logo = secure_filename(form.logo.data.filename)
            logo = change_filename(file_logo)
            form.logo.data.save(app.config["UP_DIR"] + logo)
        movie.star = data["star"]
        movie.tag_id = data["tag_id"]
        movie_info = data["info"]
        movie.title = data["title"]
        movie.area = data["area"]
        movie.length = data["length"]
        movie.release_time = datetime.datetime(*(tuple(map(int,data["release_time"].split("-")))))
        db.session.add(movie)
        db.session.commit()
        flash("修改电影%s成功" % data["title"], "OK")
        return redirect(url_for("admin.movie_edit", id = id)) 
    return render_template("admin/movie_edit.html", form = form, movie = movie)

@admin.route("/movie/list<int:page>", methods=["POST","GET"])
@admin_login_req
def movie_list(page = None):
    if page is None:
        page = 1
    page_data = Movie.query.join(Tag).filter(
            Tag.id == Movie.tag_id
            ).order_by(
                    Movie.addtime.desc()
                    ).paginate(page=page, per_page=10)
    return render_template("admin/movie_list.html", page_data = page_data)

@admin.route("/movie/del/<int:id>", methods=["GET"])
@admin_login_req
def movie_del(id=None):
    movie = Movie.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()
    flash("删除电影%s成功" % movie.title, "OK")
    return redirect(url_for("admin.movie_list", page=1))

@admin.route("/preview/add", methods=["GET", "POST"])
@admin_login_req
def preview_add():
    form = PreviewForm()
    if form.validate_on_submit():
        data = form.data
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")
        logo = change_filename(file_logo)
        form.logo.data.save(app.config["UP_DIR"] + logo)
        preview = Preview(
                title = data["title"],
                logo = logo
                )
        db.session.add(preview)
        db.session.commit()
        flash("添加预告成功", "OK")
        return redirect( url_for("admin.preview_add"))
    return render_template("admin/preview_add.html", form = form)

@admin.route("/preview/list/<int:page>/", methods=["GET"])
@admin_login_req
def preview_list(page = None):
    if page is None:
        page = 1
    page_data = Preview.query.order_by(
            Preview.addtime.desc()
            ).paginate(page=page, per_page=10)
    return render_template("admin/preview_list.html", page_data=page_data)

@admin.route("/preview/del/<int:id>/", methods=["GET"])
@admin_login_req
def preview_del(id=None):
    preview = Preview.query.get_or_404(id)
    db.session.delete(preview)
    db.session.commit()
    flash("删除预告成功", "OK")
    return redirect(url_for("admin.preview_list", page=1))
    
@admin.route("/preview/edit/<int:id>", methods=["GET", "POST"])
@admin_login_req
def preview_edit(id=None):
    form = PreviewForm()
    form.logo.validators.clear()
    preview = Preview.query.get_or_404(id)
    if request.method == "GET":
        form.title.data = preview.title
    if form.validate_on_submit():
        data = form.data
        if form.logo.data:
            file_logo = secure_filename(form.logo.data.filename)
            preview.logo = change_filename(file_logo)
            form.logo.data.save(app.config["UP_DIR"] + preview.log)
        preview.title = data["title"]
        db.session.add(preview)
        db.session.commit()
        flash("修改预告成功", "OK")
        return redirect(url_for("admin.preview_edit", id=id))
    return render_template("admin/preview_edit.html", form=form, preview=preview)

@admin.route("/user/list/<int:page>/", methods=["GET"])
@admin_login_req
def user_list(page = None):
    if page is None:
        page = 1
    page_data = User.query.order_by(
            User.addtime.desc()
            ).paginate(page=page, per_page=10)
    return render_template("admin/user_list.html", page_data = page_data)

@admin.route("/user/view/<int:id>", methods=["GET"])
@admin_login_req
def user_view(id = None):
    user_data = User.query.get_or_404(id)
    return render_template("admin/user_view.html", user_data=user_data)

@admin.route("/user/del/<int:id>", methods=["GET"])
@admin_login_req
def user_del(id=None):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.commit()
    flash("删除用户%s成功" % user.name, "OK")
    return redirect(url_for('admin.user_list', page=1))

@admin.route("/comment/list")
@admin_login_req
def comment_list():
    return render_template("admin/comment_list.html")

@admin.route("/moviecol/list")
@admin_login_req
def moviecol_list():
    return render_template("admin/moviecol_list.html")

@admin.route("/oplog/list/")
@admin_login_req
def oplog_list():
    return render_template("admin/oplog_list.html")

@admin.route("adminloginlog/list")
@admin_login_req
def adminloginlog_list():
    return render_template("admin/adminloginlog_list.html")

@admin.route("userloginlog/list/")
@admin_login_req
def userloginlog_list():
    return render_template("admin/userloginlog_list.html")

@admin.route("/role/add")
@admin_login_req
def role_add():
    return render_template("admin/role_add.html")

@admin.route("/role/list")
@admin_login_req
def role_list():
    return render_template("admin/role_list.html")

@admin.route("/auth/add/")
@admin_login_req
def auth_add():
    return render_template("admin/auth_add.html")

@admin.route("/auth/list/")
@admin_login_req
def auth_list():
    return render_template("admin/auth_list.html")

@admin.route("/admin/add/")
@admin_login_req
def admin_add():
    return render_template("admin/admin_add.html")

@admin.route("/admin/list")
@admin_login_req
def admin_list():
    return render_template("admin/admin_list.html")



