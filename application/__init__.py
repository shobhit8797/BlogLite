# Import Flask modules
from flask import Flask

from flask_migrate import Migrate  
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager
from flask_restful import Resource, Api


# Initialize Flask app with the template folder address
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'

# Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
app.app_context().push()

login_manager = LoginManager(app)
# login_manager.login_view = "login"
# login_manager.login_message_category = "info"

from application import controllers

from application.apis import *
api.add_resource(UserSignup,'/api/signup')
api.add_resource(UserLogin, '/api/login')
api.add_resource(UserLogout, '/api/logout')
api.add_resource(UserAPI, '/api/<string:username>')
api.add_resource(PostAPI, '/api/posts', '/api/posts/<int:post_id>')
api.add_resource(Follow, '/api/follow')