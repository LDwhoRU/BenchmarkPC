from bench import app, db
from bench.models import *
from flask import render_template, request, flash, redirect
from forms import LoginForm, RegisterForm, newListingForm, bidForm
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
def manageListings():
    if current_user.is_anonymous:
        return redirect('/login')

    title = "Manage Listings | BenchmarkPC"

    listings = Listing.query.filter_by(userId=current_user.id) 
    entries = listings.all()
    for entry in entries:
        print(entry.ListingName)
    return render_template('manageListing.html', title=title, entries=entries)

@app.route('/manage/<id>')
def manageListing(id):
    print("Test")
    title = "Managing Listing {0} | BenchmarkPC".format(id)
    listing = Listing.query.filter_by(id=id).first_or_404()
    listingBids = Bids.query.filter_by(bidListing=id)
    bidUsers = []
    listingBidsLists = []
    for i in listingBids:
        print(i)
        bidUsers.append(User.query.filter_by(id=i.bidUser).first())
        listingBidsLists.append(i)
    combinedList = [bidUsers, listingBidsLists]
    length = len(listingBidsLists)
    if current_user.is_anonymous:
        return redirect('/login')
    elif current_user.id != listing.userId:
        return redirect("/")
        
    if(listing.ListingType == "Case"):
        case = Case.query.filter_by(caseListing=id).first()
        return render_template('manageListingTemplates/CaseHTML.html', title=title,
            bids=combinedList, length=length,listing=listing, case=case)
    
   


@app.route('/listing')
def viewListing():
    title = "Listing | BenchmarkPC"

    return render_template("view.html", title=title)

@app.route('/listing/<id>', methods=['GET','POST'])
def viewListingNumber(id):
    title = "Listing | BenchmarkPC"

    print("Viewing Listing: " + id)

    listing = Listing.query.filter_by(id=id).first_or_404()
    user = User.query.filter_by(id=listing.userId).first()
    print(user.username)
    date = str(listing.ListingTimeStamp.day) + "/" + str(listing.ListingTimeStamp.month) + "/" + str(listing.ListingTimeStamp.year)
    print(date)
    form = bidForm()
    if(request.method == "POST"):
        exists = db.session.query(Bids.bidUser).filter_by(bidUser=current_user.id)

        bidMoney = request.form.get("bid")
        if(exists is not None):
                bid = Bids.query.filter_by(bidUser=current_user.id, bidListing=id).first()
                bid.bidAmount = bidMoney
        else:
                bid = Bids(bidAmount=bidMoney, bidUser=current_user.id, bidListing=id)
        db.session.add(bid)
        db.session.commit()



    if(listing.ListingType == "CPU"):
        details = CPU.query.filter_by(CPUListing=listing.id).first()
        return render_template("ViewListingTemplates/CPUListing.html", title=title, 
        listing=listing,user=user,date=date,details=details,form=form)

    elif(listing.ListingType == "Graphics Card"):
        details = GPU.query.filter_by(GPUListing=listing.id).first()
        return render_template("ViewListingTemplates/GPUListing.html", title=title, 
        listing=listing,user=user,date=date,details=details,form=form)

    elif(listing.ListingType == "CPU Cooler"):
        details = CPUCooler.query.filter_by(CPUCoolerListing=listing.id).first()
        return render_template("ViewListingTemplates/CPUCooler.html", title=title, 
        listing=listing,user=user,date=date,details=details,form=form)

    elif(listing.ListingType == "Memory"):
        details = Memory.query.filter_by(memoryListing=listing.id).first()
        return render_template("ViewListingTemplates/Memory.html", title=title, 
        listing=listing,user=user,date=date,details=details,form=form)

    elif(listing.ListingType == "Case"):
        details = Case.query.filter_by(caseListing=listing.id).first()
        return render_template("ViewListingTemplates/Case.html", title=title, 
        listing=listing,user=user,date=date,details=details,form=form)

    elif(listing.ListingType == "Power Supply"):
        details = PowerSupply.query.filter_by(PowerSupplyListing=listing.id).first()
        return render_template("ViewListingTemplates/PowerSupply.html", title=title, 
        listing=listing,user=user,date=date,details=details,form=form)

    elif(listing.ListingType == "Motherboard"):
        details = Motherboard.query.filter_by(MotherboardListing=listing.id).first()
        return render_template("ViewListingTemplates/Motherboard.html", title=title, 
        listing=listing,user=user,date=date,details=details,form=form)

    else:
        return redirect("/")
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

