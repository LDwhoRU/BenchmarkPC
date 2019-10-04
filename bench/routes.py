from bench import app, db
from bench.models import *
from flask import render_template, request, flash, redirect
from forms import LoginForm, RegisterForm, newListingForm
from flask_login import current_user, login_user, logout_user
from bench.newListingFunctions import processListing


@app.route('/', methods=['GET','POST'])
def index():
    title  = "Home | BenchmarkPC"
    if(current_user.is_authenticated):
        print("Good")
    return render_template('index.html',  title=title)

@app.route('/newListing', methods=['GET','POST'])
def newListing():
    if current_user.is_anonymous:
        return redirect('/login')
    form = newListingForm()
    if request.method == 'POST':
        if(processListing(request)):
            return redirect("/")
        else:
            return redirect('/manage')
        print(request.form.get('productName'))
        print(request.form.get('productPrice'))
        print(request.form.get('productDescription'))
        print(request.form.get('productType'))

    title = "New Listing | BenchmarkPC"
    return render_template('createNewListing.html', form=form, title=title)

@app.route('/manage')
def manageListing():
    title = "Manage Listings | BenchmarkPC"
    return render_template('manageListing.html', title=title)

@app.route('/listing')
def viewListing():
    title = "Listing | BenchmarkPC"

    return render_template("view.html", title=title)

@app.route('/listing/<id>')
def viewListingNumber(id):
    title = "Listing | BenchmarkPC"

    print("Viewing Listing: " + id)

    listing = Listing.query.filter_by(id=id).first_or_404()
    user = User.query.filter_by(id=listing.userId).first()
    print(user.username)
    date = str(listing.ListingTimeStamp.day) + "/" + str(listing.ListingTimeStamp.month) + "/" + str(listing.ListingTimeStamp.year)
    print(date)
    if(listing.ListingType == "CPU"):
        details = CPU.query.filter_by(CPUListing=listing.id).first()
        return render_template("ViewListingTemplates/CPUListing.html", title=title, 
        listing=listing,user=user,date=date,details=details)
    elif(listing.ListingType == "Graphics Card"):
        details = GPU.query.filter_by(GPUListing=listing.id).first()
        return render_template("ViewListingTemplates/GPUListing.html", title=title, 
        listing=listing,user=user,date=date,details=details)
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

    title = "Register | BenchmarkPC"

    return render_template("register.html",form=form, title=title)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username Or Password")
            print("failed")
            return redirect("/login")

        login_user(user)
        print("Logged IN")
        return redirect("/")

    title = "Login | BenchmarkPC"
    return render_template("login.html", form=form, title=title)

@app.errorhandler(404)
def not_found(e):
    return render_template('404Error.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")

