from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
app = Flask(__name__)
app.debug = True
#Database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SECRET_KEY'] = '13c144f006b7411aa39365a5d7d42da1'
app.config['UPLOAD_FOLDER'] = ".\Images"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
from flask_wtf.csrf import CsrfProtect
from flask_login import LoginManager
csrf = CsrfProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)
from bench import routes, models