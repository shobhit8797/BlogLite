import os
import werkzeug
from application import db, app
from application.models import Follow, Image, Post, User
from application.request_code import *
from flask import request, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from flask_restful import Resource, fields, marshal_with, reqparse
from werkzeug.utils import secure_filename

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
    'phn': fields.String,
    'bio': fields.String,
}
class UserAPI(Resource):
    # to get user details
    @marshal_with(user_get)
    def get(self,username):
        user = User.query.filter_by(username=username).first()
        if user:
            return user
        else:
            raise UserNotFound(status_code=404)
    
    @marshal_with(user_get)
    def get(self):
        return current_user, 200

    def put(self):
        username = request.get_json()['username']
        user = User.query.filter_by(username=username).first()
        if user:
            user.email = request.get_json()['email']
            user.name = request.get_json()['name']
            user.phn = request.get_json()['phn']
            user.bio = request.get_json()['bio']
            db.session.commit()
            return '', 200
        else:
            return '', 404
 
    def delete(self):
        user = User.query.filter_by(username=current_user.username).first()
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
        title = request.form['title']
        content = request.form['post_content']
        author = current_user

        post = Post(title=title, content=content, author=author)
        db.session.add(post)
        db.session.flush()
        
        image = request.files['post_pic']
        # print('--------------------')
        # print(image.filename)
        # print('--------------------')
        if image.filename:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            image_url = f"static/uploads/{filename}"
            image = Image(url=image_url, post_id=post.id)
            db.session.add(image)

        db.session.commit()
        return '', 200

    def put(self,post_id):
        print(current_user.username)
        return {'post_id': post_id}

    def delete(self,post_id):
        pass

# Url: /api/follow
class FollowApi(Resource):
    def get(self):
        raise request_not_allowed(status_code=404, messasge='Not a valid request method')
    
    def post(self):
        try:
            username = request.get_json()['follow_user']
            follow_toggle = request.get_json()['follow_toggle']
            following_user = User.query.filter_by(username=username).first()

            print('-------',follow_toggle,'--------')
            

            if follow_toggle == 'Follow':
                try:
                    if current_user is None or following_user is None:
                        raise ValueError(f"current_user or following_user do not exist")
                    
                    follow = Follow()
                    follow.follower_id=current_user.id
                    follow.following_id=following_user.id
                    db.session.add(follow)
                    db.session.commit()
                    return {'message':"Successfully followed user"}, 200
                except Exception as e:
                    print('Error occured here:',str(e))
                    return {'message':str(e)}, 400
                
            else:
                try:
                    unfollow = Follow.query.filter_by(follower_id=current_user.id, following_id=following_user.id).first()
                    db.session.delete(unfollow)
                    db.session.commit()
                    return {'message':"Successfully unfollowed user"}, 200
                except Exception as e:
                    print('Error occured here:',str(e))
                    return {'message':"Successfully unfollowed user"}, 400
                # except:
                #     return {'message':"Error while trying to unfollow user"}, 500
        except:
            return "somethig went wrong", 404
    
    def put(self):
        raise request_not_allowed(status_code=404, messasge='Not a valid request method')
    
    def delete(self):
        raise request_not_allowed(status_code=404, messasge='Not a valid request method')

# path: /api/user/<username>
class SearchUser(Resource):
    @marshal_with(user_get)
    def get(self, username):
        try:
            usernames = User.query.filter(User.username.like('%' + username + '%')).all()
            return usernames, 200
        except:
            return 'worng Input', 404


# path: /api/feed
class Feed(Resource):
    @marshal_with(post_get)
    def get(self):
        try:
           
            user = User.query.filter_by(username=current_user.username).first()
            if not user:
                return {'message':f"user with name {current_user} does not exist"}, 404
            
            
            following = user.following
           
            posts = []
            for follow in following:
                for post in follow.posts:
                    posts.append(post)
            print(posts)
            print('-------------------------')
            try:
                sorted_posts = sorted(posts, key=lambda post: post.date_posted, reverse=True)
            except Exception as e:
                    print('Error occured here:',str(e))
                    return {'message':"Successfully unfollowed user"}, 400

            print('-------------------------')
            return sorted_posts, 200
        except Exception as e:
            return jsonify(message=f"Error while trying to fetch feed: {e}"), 500
