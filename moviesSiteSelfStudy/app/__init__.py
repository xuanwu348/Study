#_*_ encoding:utf-8 _*_

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app/MyMovies.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = True
db = SQLAlchemy(app)
from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint


app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")
