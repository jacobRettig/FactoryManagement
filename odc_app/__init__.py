#Primary Author: Jacob Rettig

"""
This file is the main file that Flask runs to begin the application. Thus, the main libraries that are the backbone
of the application go here.
"""

#Updating modules
import pip
pip.main(['install', '-U', 'flask'])
pip.main(['install', '-U', 'sqlAlchemy'])
pip.main(['install', '-U', 'Faker'])
pip.main(['install', '-U', 'flask_bootstrap'])
pip.main(['install', '-U', 'flask_login'])
pip.main(['install', '-U', 'flask_wtf'])
pip.main(['install', '-U', 'wtforms'])
pip.main(['install', '-U', 'phonenumbers'])
pip.main(['install', '-U', 'flask_sqlalchemy'])
pip.main(['install', '-U', 'flask_admin'])


#imports
#import sqlHandler, testing -- These imports might be better suited in the main routes.py file where the frontend of the application resides
from flask import Flask, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager
from flask_admin import Admin
from flask_basicauth import BasicAuth

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
login = LoginManager(app)
login.login_view = 'login' # Name of route that user is redirected to for logging in
admin = Admin(app, name='odc_app', template_mode='bootstrap3') # Very basic admin panel setup, not finished yet

from odc_app import routes