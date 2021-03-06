from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp
from app.models import User

class RegistForm(FlaskForm):
    name = StringField(
            label = "昵称",
            validators = [
                   DataRequired("请输入昵称")
                ],
            description = "昵称",
            render_kw = {
                "id":"input_name",
                "class":"form-control input-lg",
                "placeholder":"昵称"
                }
            )
    email = StringField(
            label = "邮箱",
            validators = [
                DataRequired("请输入邮箱"),
                Email("请输入邮箱地址")
                ],
            description = "邮箱",
            render_kw = {
                "id":"input_email",
                "class":"form-control input-lg",
                "placeholder":"邮箱"
                },
            )
    phone = StringField(
            label = "手机",
            validators = [
                DataRequired("请输入手机号码!"),
                Regexp("1[3|5|7|8]\\d{9}",message="请输入正确的手机号码！")
                ],
            description = "手机",
            render_kw = {
                "id":"input_phone",
                "class":"form-control input-lg",
                "placeholder":"手机"
                }
            )
    pwd = PasswordField(
            label = "密码",
            validators = [
                DataRequired("请输入密码！")
                ],
            description = "密码",
            render_kw = {
                "id":"input_password",
                "class":"form-control input-lg",
                "placeholder":"密码"
                }
            )
    repwd = PasswordField(
            label = "确认密码",
            validators = [
                DataRequired("请输入确认密码！"),
                EqualTo('pwd', message="两次密码输入不一致")
                ],
            description = "确认密码",
            render_kw = {
                "id":"input_password",
                "class":"form-control input-lg",
                "placeholder":"密码"
                }
            )
    submit = SubmitField(
            "注册",
            render_kw = {
                "class":"btn btn-lg btn-success btn-block",
                }
            )
    def validate_name(self, field):
        name = field.data
        user = User.query.filter_by(name=name).count()
        if user != 0:
            return ValidationError("昵称已经存在！")
    def validate_email(self, field):
        email = field.data
        user = User.query.filter_by(email=email).count()
        if user != 0:
            raise ValidationError("邮箱已被注册！")
    def validate_phone(self, field):
        phone = field.data
        user = User.query.filter_by(phone=phone).count()
        if user != 0:
            raise ValidationError("手机号码已被注册！")

class LoginForm(FlaskForm):
    account = StringField(
            label = "账号",
            validators = [
                DataRequired("请输入账号")
                ],
            description="账号",
            render_kw = {
                "id":"input_contact",
                "class":"form-control input-lg", 
                "placeholder":"用户名/邮箱/手机号码"
                }
            )
    pwd = PasswordField(
            label = "密码",
            validators = [
                DataRequired("请输入密码！")
                ],
            description = "密码",
            render_kw = {
                "id":"input_password",
                "class":"form-control input-lg" ,
                "placeholder":"密码"
                }
            )
    submit = SubmitField(
            "登录",
            render_kw = {
                   "class":"btn btn-lg btn-success btn-block",
                }
            )

class UserdetailForm(FlaskForm):
    name = StringField(
            label = "昵称",
            validators = [
                DataRequired("请输入昵称！")
                ],
            description = "昵称",
            render_kw = {
                "id":"input_name",
                "class":"form-control" ,
                "placeholder":"昵称" 
                }
            )
    email = StringField(
            label = "邮箱",
            validators = [
                DataRequired("请输入邮箱"),
                Email("邮箱地址不正确！")
                ],
            description = "邮箱",
            render_kw = {
                "id":"input_email",
                "class":"form-control",
                "placeholder":"邮箱"
                }
            )
    phone = StringField(
            label = "手机",
            validators = [
                DataRequired("请输入手机号码"),
                Regexp("1[3|5|7|8]\\d{9}", message="手机号码格式不对！")
                ],
            description = "手机",
            render_kw = {
                "id":"input_phone",
                "class":"form-control" ,
                "placeholder":"手机"
                }
            )
    face = FileField(
            label = "头像",
            validators = [
                DataRequired("请选择头像文件！")
                ],
            description = "头像"
            )
    info = TextAreaField(
            label = "简介",
            validators = [
                DataRequired("请输入简介")
                ],
            description = "请输入简介",
            render_kw = {
                "class":"form-control",
                "rows":"10",
                "id":"input_info"
                }
            )
    submit = SubmitField(
            "保存修改",
            render_kw = {
                "class":"btn btn-success",
                "span class":"glyphicon glyphicon-saved",
                }
            )

class PwdForm(FlaskForm):
    pwd = PasswordField(
           label = "请输入旧密码",
           validators = [
              DataRequired("请输入旧密码")
           ],
           description = "请输入旧密码",
           render_kw = {
                "id":"input_password",
                "class":"form-control input-lg",
                "placeholder":"密码"
           }
        )
    repwd = PasswordField(
           label = "请输入新密码",
           validators = [
              DataRequired("请输入新密码")
           ],
           description = "请输入密码",
           render_kw = {
                "id":"input_password",
                "class":"form-control input-lg",
                "placeholder":"密码"
           }
        )
    submit = SubmitField(
           "提交修改",
           render_kw = {
                "class":"btn btn-success",
                "span class":"glyphicon glyphicon-saved"
           }
        )

class CommentForm(FlaskForm):
    content = TextAreaField(
        label = "内容",
        validators = [
                DataRequired("请输入评论内容"),
            ],
        description = "内容",
        render_kw = {
            "id":"input_content",
            }
        )
    submit_com = SubmitField(
        "提交评论",
        render_kw = {
            "class":"btn btn-success",
            "id:":"btn-sub",
            "span class":"glyphicon glyphicon-edit"
            }
        )

