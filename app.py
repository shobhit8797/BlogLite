# Import Flask modules
from flask import Flask
from flask import render_template, request, redirect, url_for, flash, session

from flask_migrate import Migrate
from application.database import db 
from application.models import *    


# Initialize Flask app with the template folder address
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# Initialize the database
db.init_app(app)
migrate = Migrate(app, db)
app.app_context().push()

from application.controllers import *

if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0',port=8080, debug=True)
