from application import db
from application.models import Post, User
from application.request_code import *
from flask import request
from flask_login import login_required, current_user, login_user, logout_user
from flask_restful import Resource, fields, marshal_with, reqparse

class UserLogin(Resource):
    def get(self):
        raise request_not_allowed(status_code=404, messasge='Not a valid request method')
    
    def post(self):

        username = request.get_json()['username']
        password = request.get_json()['password']

        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                login_user(user)
                return 'Logged in successfully', 200
            else:
                raise incorrect_login(status_code=404, errorin='Password')
        else:
            raise incorrect_login(status_code=404, errorin='Username')

    def put(self):
        raise request_not_allowed(status_code=404, messasge='Not a valid request method')
    
    def delete(self):
        raise request_not_allowed(status_code=404, messasge='Not a valid request method')

class UserSignup(Resource):
    def get(self):
        raise request_not_allowed(status_code=404, messasge='Not a valid request method')

    def post(self):
        username = request.get_json()['username']
        email = request.get_json()['email']
        password = request.get_json()['password']
        name = request.get_json()['name']
       
        phn = request.get_json()['phn']
    
        # Check if user already exists
        user = User.query.filter_by(username=username).first()
        if user:
           raise UserExists(status_code=404, errorin='Username')

        emailval = User.query.filter_by(email=email).first()
        if emailval:
            raise UserExists(status_code=404, errorin='Email')
            
        # Create new user
        new_user = User(username=username, email=email, name=name, phn=phn, password=password)
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        return 'User Created', 200
    
    def put(self):
        raise request_not_allowed(status_code=404, messasge='Not a valid request method')
    
    def delete(self):
        raise request_not_allowed(status_code=404, messasge='Not a valid request method')

class UserLogout(Resource):
    def get(self):
        raise request_not_allowed(status_code=404, messasge='Not a valid request method')
        # return 'Logged out successfully', 200
    
    def post(self):
        print(current_user)
        logout_user()
        # raise request_not_allowed(status_code=404, messasge='Not a valid request method')
        return {
            'message' : 'Logged out successfully'
        }, 200

    def put(self):
        raise request_not_allowed(status_code=404, messasge='Not a valid request method')
    
    def delete(self):
        raise request_not_allowed(status_code=404, messasge='Not a valid request method')


# for get request for user api
user_get = {
    'username': fields.String,
    'email': fields.String,
    'name': fields.String,
}
# for post request for user api
parser = reqparse.RequestParser()
parser.add_argument('username', required=True)
parser.add_argument('email')
parser.add_argument('name')
parser.add_argument('phn')
parser.add_argument('bio')
parser.add_argument('password')


class UserAPI(Resource):
    # to get user details
    @marshal_with(user_get)
    def get(self,username):
        user = User.query.filter_by(username=username).first()
        if user:
            return user
        else:
            raise UserNotFound(status_code=404)

    def post(self,username):
        args = parser.parse_args()
        user = User(username=args['username'], email=args['email'], name=args['name'], phn=args['phn'], bio=args['bio'], password=args['password'])
        db.session.add(user)
        db.session.commit()
        return '', 200

    def put(self,username):
        args = parser.parse_args()

        user = User.query.filter_by(username=username).first()
        if user:
            for i in args:
                if args[i]:
                    setattr(user, i, args[i])
            
            db.session.add(user)
            db.session.commit()
        return '', 200
 
    def delete(self,username):
        user = User.query.filter_by(username=username).first()
        db.session.delete(user)
        db.session.commit()
        return '', 200


post_get = {
    'title': fields.String,
    'content': fields.String,
    'author': fields.String,
}
# Url: /api/posts, /api/posts/<post_id>
class PostAPI(Resource):
    @marshal_with(post_get)
    def get(self,post_id):
        post = Post.query.filter_by(id=post_id).first()
        if post:
            return post
        else:
            return '', 404

    def post(self):
        title = request.get_json()['title']
        content = request.get_json()['content']
        author = current_user
        post = Post(title=title, content=content, author=author)
        db.session.add(post)
        db.session.commit()
        return '', 200

    def put(self,post_id):
        print(current_user.username)
        return {'post_id': post_id}

    def delete(self,post_id):
        pass

class Follow(Resource):
    def get(self):
        raise request_not_allowed(status_code=404, messasge='Not a valid request method')
    
    def post(self):
        try:
            username = request.get_json()['follow_user']
            follow_toggle = request.get_json()['follow_toggle']
            user = User.query.filter_by(username=username).first()
            if user:
                if follow_toggle == 'follow':
                    current_user.follow(user)
                else:
                    current_user.unfollow(user)
                db.session.commit()
                return f'{follow_toggle}ed', 200
            else:
                raise UserNotFound(status_code=404)
        except:
            return "somethig went wrong", 404
    
    def put(self):
        raise request_not_allowed(status_code=404, messasge='Not a valid request method')
    
    def delete(self):
        raise request_not_allowed(status_code=404, messasge='Not a valid request method')