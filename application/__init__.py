# Import Flask modules
from flask import Flask
from os.path import join, dirname, realpath

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager
from flask_restful import Resource, Api

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Initialize Flask app with the template folder address
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
app.app_context().push()

login_manager = LoginManager(app)

from application import controllers

# Api resource mapping with its path
from application.apis.auth_api import *
api.add_resource(UserSignup,'/api/signup')
api.add_resource(UserLogin, '/api/login')
api.add_resource(UserLogout, '/api/logout')

from application.apis.user_api import *
api.add_resource(UserAPI, '/api/user' ,'/api/<string:username>')
api.add_resource(FollowApi, '/api/follow')
api.add_resource(SearchUser, '/api/user/<username>')

from application.apis.post_api import *
api.add_resource(PostAPI, '/api/posts', '/api/posts/<int:post_id>')
api.add_resource(Feed, '/api/feed')
api.add_resource(Like, '/api/like/<post_id>')