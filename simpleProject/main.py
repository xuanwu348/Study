from flask import Flask
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)

@app.route("/")
def home():
    return '<h1>Hello World!</h1>'

class User(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(255))
    passwd = db.Column(db.String(255))
    posts = db.relationship(
               'Post',
               backref = 'user',
               lazy = 'dynamic'
            )

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return "<User '{}'>".format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_data = db.Column(db.DateTime())
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Post '{}'>".format(self.title)



if __name__ == "__main__":
    app.run()
