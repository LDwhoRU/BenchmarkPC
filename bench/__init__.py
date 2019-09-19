from flask import Flask, render_template
app = Flask(__name__)
app.debug = True
app.secret_key = '13c144f006b7411aa39365a5d7d42da1'
from bench import routes