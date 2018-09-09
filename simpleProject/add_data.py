import random
import datetime
from main import Tag, User, Post, db


user = User.query.get(1)
taglist = [Tag("Python"), Tag('Flask'), Tag("SQLAlchemy"), Tag('jinja')]

s = "Example text"

for i in range(100):
    new_post = Post("Post " + str(i))
    new_post.user = user
    new_post.publish_date = datetime.datetime.now()
    new_text = s
    new_post.tags = random.sample(taglist, random.randint(1,3))
    db.session.add(new_post)

db.session.commit()
