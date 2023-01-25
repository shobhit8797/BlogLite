from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from datetime import datetime
from application import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String(128))
    phn = db.Column(db.Integer(), nullable=True)
    bio = db.Column(db.Text, nullable = True)
    profile_picture = db.Column(db.String(500), nullable=True)
    password = db.Column(db.String(128), nullable= False)
    # Defining the authors of the posts by linking the post to the specific user
    posts = db.relationship('Post'  , backref='author', lazy=True, cascade='all, delete')
    # All the comments that a particular user has posted
    comments = db.relationship('Comment', backref='commenter', lazy=True, cascade='all, delete')
    # All the posts that this user has liked
    likes = db.relationship('Like', backref='liker', lazy=True, cascade='all, delete') 
    
    
    following = db.relationship("User",
                            secondary='follow',
                            primaryjoin="User.id==Follow.follower_id",
                            secondaryjoin="User.id==Follow.following_id",
                            backref="followers")

    def is_following(self, user2)->bool:
        if self is None or user2 is None:
            raise ValueError(f"user1 or user2 do not exist")
        follow = Follow.query.filter_by(follower_id=self.id, following_id=user2.id).first()
        if follow:
            return True
        else:
            return False
    
    def __repr__(self):
        return f"User('{self.username}'"

class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=True)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(50), db.ForeignKey('user.username'))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    likes = db.relationship("Like", backref='postid', lazy=True, cascade='all, delete')
    comments = db.relationship('Comment', backref='postid', lazy=True, cascade='all, delete')
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', backref=db.backref('images', lazy='dynamic'))

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    following_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', backref=db.backref('videos', lazy='dynamic'))

class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String(300), nullable=False)
    # post for which this comment has been added
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    # owner of the comment
    author = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
    
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Comment('{self.comment}', '{self.date_posted}')"

class Like(db.Model):
    __tablename__ = 'like'

    id = db.Column(db.Integer, primary_key=True)
    # user taht liked that post
    author = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
    # post that the user liked
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Like('{self.author}', '{self.date_posted}')"

