from bench import app, db
from bench.models import User
from flask import render_template, request, flash, redirect
from forms import LoginForm, RegisterForm, newListingForm
from flask_login import current_user, login_user, logout_user


@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/newListing', methods=['GET','POST'])
def newListing():
    form = newListingForm()
    if request.method == 'POST':
        print(request.form.get('productName'))
        print(request.form.get('productPrice'))
        print(request.form.get('productDescription'))

    return render_template('createNewListing.html', form=form)

@app.route('/manage')
def manageListing():
    return render_template('manageListing.html')

@app.route('/listing')
def viewListing():
    return render_template("view.html")

@app.route('/register', methods=['post','get'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.user_name.data, email=form.email.data, phone=form.phone_number.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        print("registed i cant spell")
        return redirect("/")
    print("test")
    if(request.method == 'POST'):
        print("Username: " + form.user_name.data)
        print("Email: " + form.email.data)
    return render_template("register.html",form=form)


@app.route('/login', methods=['post', 'get'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username Or Password")
            print("failed")
            return redirect("/")
        login_user(user)
        return redirect("/")
    return render_template("login.html", form=form)

@app.errorhandler(404)
def not_found(e):
    return render_template('404Error.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")

