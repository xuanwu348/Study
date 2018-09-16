#_*_coding:utf-8_*_
from datetime import datetime
from app import db

#from flask import Flask



class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(11), unique=True)
    info = db.Column(db.Text)
    face = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    uuid = db.Column(db.String(255), unique=True))
    userlogs = db.relationship("Userlog", backref="user")

    def __repr__(self):
        return "<User %r>" % self.name

class Userlog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    ip = db.column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    

    def __repr__(self):
        return "<Userlog %r>" % self.id

class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    movies = db.relationship("Mopvies", backref="tag")
    def __repr__(self):
        return "<Tag %r>" % self.name

class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255),unique=True)
    url = db.Column(db.String(255), unique=True)
    info = db.Column(db.Text)
    logo = db.Column(db.String(255), unique=True)
    start = db.Column(db.SmallInteger)
    playnum = db.Column(db.BigInteger)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"))
    area = db.Column(db.String(255))
    release_time = db.Column(db.Date)
    length = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<Movie %r>" % self.title






