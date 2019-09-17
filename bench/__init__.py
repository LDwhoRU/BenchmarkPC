from flask import Flask, render_template
app = Flask(__name__)
app.debug = True
from bench import routes