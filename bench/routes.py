from bench import app
from flask import render_template, request
from forms import LoginForm

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')
@app.route('/newListing')
def newListing():
    return render_template('createNewListing.html')
@app.route('/manage')
def manageListing():
    return render_template('manageListing.html')
@app.route('/listing')
def viewListing():
    return render_template("view.html")
@app.route('/register')
def register():
    return render_template("register.html")
@app.route('/login', methods=['post', 'get'])
def login():
    form = LoginForm()
   
    return render_template("login.html", form=form)

@app.errorhandler(404)
def not_found(e):
    return render_template('404Error.html')