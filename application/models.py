from datetime import datetime
from .database import db


class User(db.Model):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(128), nullable= False)
    fname = db.Column(db.String(128))
    lname = db.Column(db.String(128))
    email = db.Column(db.String, unique=True, nullable= False)
    phn = db.Column(db.String(10), unique=True, nullable= False)

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