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