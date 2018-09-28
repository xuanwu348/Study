#coding:utf8

from . import admin
from flask import render_template, redirect, url_for, flash, session, request, abort
from app.admin.forms import LoginForm, TagForm, MovieForm, PreviewForm, PwdForm, AuthForm, RoleForm, AdminForm
from app.models import Admin, Tag, Movie, Preview, User, Comment, Moviecol, Userlog, Oplog, Adminlog, Auth, Role
from functools import wraps
from app import db, app
from werkzeug.utils import secure_filename
import uuid
import datetime
import os

@admin.context_processor
def tpl_extra():
    data = dict(online_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return data

def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function 

def admin_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin = Admin.query.join(Role).filter(
                   Admin.id == session["admin_id"],
                   Admin.role_id == Role.id
                ).first()
        if admin:
            auths = admin.role.auths
            auths_list = list(map(int, auths.split(",")))
            auth = Auth.query.all()
            url_list = [v.url for i in auths_list for v in auth if i == v.id]
            print(url_list, request.url_rule)
            if str(request.url_rule) not in url_list:
                abort(404)
            return f(*args, **kwargs)
        abort(404)
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
            flash("账号或者密码错误！","err")
            return redirect(url_for("admin.login"))
        session["admin"] = data["account"]
        session["admin_id"] = admin.id
        adminlog = Adminlog(
                admin_id = admin.id,
                ip = request.remote_addr
                )
        db.session.add(adminlog)
        db.session.commit()
        return redirect(request.args.get("next") or url_for("admin.index"))
    return render_template("admin/login.html", form=form)

@admin.route("/logout/", methods=["POST","GET"])
@admin_login_req
def logout():
    session.pop("admin", None)
    session.pop("admin_id", None)
    return redirect(url_for("admin.login"))

@admin.route("/pwd/", methods=["GET", "POST"])
@admin_login_req
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=session["admin"]).first()
        from werkzeug.security import generate_password_hash
        admin.pwd = generate_password_hash(data["new_pwd"])
        db.session.add(admin)
        db.session.commit()
        flash("修改密码成功，请重新登录！","OK")
        return redirect(url_for("admin.logout"))
    return render_template("admin/pwd.html", form = form)

@admin.route("/tag/tag_add/", methods=["POST","GET"])
@admin_login_req
@admin_auth
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
        oplog = Oplog(
                admin_id = session["admin_id"],
                ip = request.remote_addr,
                reason = "添加标签:%s" % data['name']
                )
        db.session.add(oplog)
        db.session.commit()
        redirect(url_for("admin.tag_add"))
    return render_template("admin/tag_add.html", form = form)

@admin.route("/tag/tag_list/<int:page>/", methods=["GET"])
@admin_login_req
@admin_auth
def tag_list(page=None):
    if page is None:
        page = 1
    page_data = Tag.query.order_by(
            Tag.addtime.desc()
            ).paginate(page=page, per_page=10)
    return render_template("admin/tag_list.html", page_data = page_data)

@admin.route("/tag/del/<int:id>", methods=["GET"])
@admin_login_req
@admin_auth
def tag_del(id=None):
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash("删除标签%s成功" % tag.name,"OK")
    oplog = Oplog(
            admin_id = session["admin_id"],
            ip = request.remote_addr,
            reason = "删除标签:%s" % tag.name
            )
    db.session.add(oplog)
    db.session.commit()
    return redirect(url_for("admin.tag_list", page=1))

@admin.route("/tag/edit/<int:id>/", methods=["POST", "GET"])
@admin_login_req
@admin_auth
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
    db.session.commit()
    flash("删除用户%s成功" % user.name, "OK")
    return redirect(url_for('admin.user_list', page=1))

@admin.route("/comment/list/<int:page>/", methods=["GET"])
@admin_login_req
def comment_list(page=None):
    if page is None:
        page = 1
    page_data = Comment.query.join(User).join(Movie).filter(
                    Movie.id == Comment.movie_id,
                    User.id == Comment.user_id 
               ).order_by(
                  Comment.addtime.desc()
               ).paginate(page=page, per_page=10) 
    print(page_data)
    return render_template("admin/comment_list.html", page_data=page_data)

@admin.route("/comment/del/<int:id>", methods=["GET"])
@admin_login_req
def comment_del(id=None):
    comment = Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    flash("删除评论成功","OK")
    return redirect(url_for("admin.comment_list",page=1))

@admin.route("/moviecol/list/<int:page>",methods=["GET"])
@admin_login_req
def moviecol_list(page=None):
    if page is None:
        page = 1
    page_data = Moviecol.query.join(User).join(Movie).filter(
        Movie.id == Moviecol.movie_id,
        User.id == Moviecol.user_id
    ).order_by(
        Moviecol.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/moviecol_list.html", page_data=page_data)

@admin.route("/movivecol/edit/<int:id>/", methods=["POST", "GET"])
@admin_login_req
def moviecol_edit(id=None):
    moviecol = Moviecol.query.get_or_404(id)
    if request.method == "GET":
        pass
        
@admin.route("/moviecol/del/<int:id>/", methods=["GET"])
@admin_login_req
def moviecol_del(id=None):
    moviecol = Moviecol.query.get_or_404(id)
    db.session.delete(moviecol)
    db.session.commit()
    flash("删除收藏电影成功", "OK")
    return redirect(url_for("admin.moviecol_list", page=1))

@admin.route("/oplog/list/<int:page>/", methods=["GET"])
@admin_login_req
def oplog_list(page=None):
    if page is None:
        page = 1
    page_data = Oplog.query.join(Admin).filter(
               Admin.id == Oplog.admin_id
            ).order_by(
                    Oplog.addtime.desc()
                    ).paginate(page=page, per_page=10)
    return render_template("admin/oplog_list.html", page_data=page_data)

@admin.route("adminloginlog/list/<int:page>/",methods=["GET"])
@admin_login_req
def adminloginlog_list(page=None):
    if page is None:
        page = 1
    page_data = Adminlog.query.join(Admin).filter(
                    Admin.id == Adminlog.admin_id
                ).order_by(
                    Adminlog.addtime.desc()
                ).paginate(page=page, per_page=10)
    return render_template("admin/adminloginlog_list.html", page_data=page_data)

@admin.route("userloginlog/list/<int:page>/", methods=["GET"])
@admin_login_req
def userloginlog_list(page=None):
    if page is None:
        page = 1
    page_data = Userlog.query.join(User).filter(
                   User.id == Userlog.user_id
               ).order_by(
                   Userlog.addtime.desc()
               ).paginate(page=page, per_page=10)
    return render_template("admin/userloginlog_list.html", page_data=page_data)

@admin.route("/role/add", methods=["GET", "POST"])
@admin_login_req
def role_add():
    form = RoleForm()
    if form.validate_on_submit():
        data = form.data
        role_name_count = Role.query.filter_by(name=data["role_name"]).count()
        if role_name_count > 0:
            flash("该角色已经添加","err")
            return redirect(url_for("admin.role_add"))
        """
        auth_temp = []
        for auth_id in data["auths"]:
            auth = Auth.query.filter(Auth.id==auth_id).first()
            auth_temp.append(auth.name) 
        """
        role = Role(
            name = data["role_name"],
            auths =  ",".join(map(str,data["auths"]))
        )
        db.session.add(role)
        db.session.commit()
        flash("添加角色成功!", "OK")
        return redirect(url_for("admin.role_add"))
    return render_template("admin/role_add.html", form = form)

@admin.route("/role/list/<int:page>/", methods=["GET"])
@admin_login_req
def role_list(page=None):
    if page is None:
        page = 1
    page_data = Role.query.order_by(
                   Role.addtime.desc()
                   ).paginate(page=page, per_page=10)
    return render_template("admin/role_list.html", page_data = page_data)

@admin.route("/role/del/<int:id>/",methods=["GET"])
@admin_login_req
def role_del(id=None):
    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash("删除角色成功", "OK")
    return redirect(url_for("admin.role_list", page=1))

@admin.route("/role/edit/<int:id>/", methods=["GET", "POST"])
@admin_login_req
def role_edit(id=None):
    form = RoleForm()
    role = Role.query.get_or_404(id)
    if request.method == "GET":
        form.auths.data = list(map(int,(role.auths).split(", ")))
    if form.validate_on_submit():
        data = form.data
        role.name = data["role_name"]
        role.auths = ",".join(map(str,data["auths"]))
        print(role.auths)
        db.session.add(role)
        db.session.commit()
        flash("修改角色成功！", "OK")
    return render_template("admin/role_edit.html", form=form, role= role)

@admin.route("/auth/add/", methods=["GET", "POST"])
@admin_login_req
def auth_add():
    form = AuthForm()
    if form.validate_on_submit():
        data = form.data
        auth = Auth(
                   name = data["auth_name"],
                   url = data["auth_url"]
               )
        db.session.add(auth)
        db.session.commit()
        flash("添加权限成功！", "OK")
        return redirect(url_for("admin.auth_add"))
    return render_template("admin/auth_add.html", form = form)

@admin.route("/auth/list/<int:page>/",methods=["GET"])
@admin_login_req
def auth_list(page=None):
    if page is None:
        page = 1
    page_data = Auth.query.order_by(Auth.addtime).paginate(page=page, per_page=10)

    return render_template("admin/auth_list.html", page_data = page_data)

@admin.route("/auth/edit/<int:id>/", methods=["GET", "POST"])
@admin_login_req
def auth_edit(id=None):
    form = AuthForm()
    form.auth_name.validators.clear()
    form.auth_url.validators.clear()
    auth = Auth.query.get_or_404(id)
    if request.method == "GET":
        form.auth_name.data = auth.name
        form.auth_url.data = auth.url
    if form.validate_on_submit():
        data = form.data
        auth_name_count =  Auth.query.filter_by(name = data['auth_name']).count()
        auth_url_count = Auth.query.filter_by(url = data['auth_url']).count()
        if auth_name_count > 0 and auth_url_count > 0 and auth.name != data['auth_name'] and auth.url != data['auth_url']:
            flash("权限名称或者url已经存在","err")
            return redirect(url_for("admin.auth_edit",id = id))
        auth.name = data["auth_name"]
        auth.url = data["auth_url"]
        db.session.add(auth)
        db.session.commit()
        flash("修改权限成功", "OK")
        return redirect(url_for("admin.auth_list", page=1))    
    return render_template("admin/auth_edit.html", form=form)

@admin.route("/auth/del/<int:id>/", methods=["GET"])
@admin_login_req
def auth_del(id=None):
    auth = Auth.query.get_or_404(id)
    db.session.delete(auth)
    db.session.commit()
    flash("删除权限成功","OK")
    return redirect(url_for("admin.auth_list", page=1))

@admin.route("/admin/add/", methods=["GET","POST"])
@admin_login_req
def admin_add():
    form = AdminForm()
    if form.validate_on_submit():
        data = form.data
        from werkzeug.security import generate_password_hash
        pwd = generate_password_hash(data["pwd"])
        admin = Admin(
                name = data['name'],
                pwd = pwd,
                is_super = data["issuper"],
                role_id = data["roleid"]
                )
        db.session.add(admin)
        db.session.commit()
        flash("添加管理员成功", "OK")
        return redirect(url_for("admin.admin_add"))
    return render_template("admin/admin_add.html", form=form)

@admin.route("/admin/list/<int:page>/", methods=["GET"])
@admin_login_req
def admin_list(page=None):
    if page is None:
        page = 1
    page_data = Admin.query.join(Role).filter(
            Role.id == Admin.role_id
            ).order_by(
                    Admin.addtime.desc()
                    ).paginate(page=page, per_page=10)
    return render_template("admin/admin_list.html", page_data=page_data)



