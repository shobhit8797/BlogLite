from datetime import datetime
from .database import db


class User(db.Model):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(128), nullable= False)
    name = db.Column(db.String(128))
    email = db.Column(db.String, unique=True, nullable= False)
    phn = db.Column(db.String(10), unique=True, nullable= True)

    def __repr__(self):
        return f"User('{self.username}'"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Comment('{self.comment}', '{self.date_posted}')"

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Like('{self.author}', '{self.date_posted}')"

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
    following = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Follow('{self.follower}', '{self.following}', '{self.date_posted}')"
