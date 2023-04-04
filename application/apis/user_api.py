import os
from datetime import datetime
import werkzeug
from application import db, app
from application.models import Follow, Image, Post, User
from application.request_code import *
from flask import request, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from flask_restful import Resource, fields, marshal_with, reqparse
from werkzeug.utils import secure_filename


user_get = {
    'username': fields.String,
    'email': fields.String,
    'name': fields.String,
    'phn': fields.String,
    'bio': fields.String,
    'profile_picture': fields.String,
}
class UserAPI(Resource):
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
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if user:
            user.email = request.form['email']
            user.name = request.form['name']
            user.phn = request.form['phone']
            user.bio = request.form['bio']
            db.session.flush()
            image = request.files['profile_picture']
            if image.filename:
                image = request.files['profile_picture']
                filename = secure_filename(image.filename)
                user.profile_picture = f"static/uploads/{filename}"
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            db.session.commit()
            return '', 200
        else:
            db.rollback()
            return '', 404
 
    def delete(self):
        user = User.query.filter_by(username=current_user.username).first()
        db.session.delete(user)
        db.session.commit()
        return '', 200


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