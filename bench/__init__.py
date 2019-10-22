from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
app = Flask(__name__)
app.debug = True
#Database
POSTGRES = {
    'user': 'postgres',
    'pw': 'test',
    'db': 'benchmarkpc',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SECRET_KEY'] = '13c144f006b7411aa39365a5d7d42da1'
app.config['UPLOAD_FOLDER'] = r".\bench\static\Images"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
from flask_wtf.csrf import CsrfProtect
from flask_login import LoginManager
csrf = CsrfProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)
from bench import routes, models