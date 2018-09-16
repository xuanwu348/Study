#_*_ encoding:utf-8 _*_

from flask import Flask

app = Flask(__name__)
from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint


app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")
