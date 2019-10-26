from bench import app, db
from bench.models import *
from flask import render_template, request, flash, redirect
from forms import LoginForm, RegisterForm, newListingForm, bidForm, manageListingForm
from flask_login import current_user, login_user, logout_user
from bench.newListingFunctions import processListing, UpdateListing


#Route For The Landing Page
#Allows The User To View Recent Listings
#Allows The User To Search For Listings
#Has Links For New Listing And Manage Listings.
@app.route('/', methods=['GET', 'POST'])
def index():
    title = "Home | BenchmarkPC"

    #Get The Three Most Recent Listings That Are Open.
    listings = Listing.query.order_by(Listing.ListingTimeStamp.desc()).filter(
        Listing.ListingState != 'Closed').limit(3).all()
    images = []

    #Get The Images For Each Listing
    for listing in listings:
        image = Images.query.filter_by(ImageListing=listing.id)
        if(image.scalar() != None):
            images.append("/static/Images/" + image.first().ImageName)
        else:
            #If The Listing Has No Image, Insert The Placeholder Image.
            images.append("/static/placeholder.png")

    #Render Initial Page.
    return render_template('index.html',  title=title, listings=listings, images=images)


#Route For New Listing Page
#Allows The User To Create New Listings
#Lots Of Backend Stuff In newListingFunctions.py For Form Validation And Database.
@app.route('/newListing', methods=['GET', 'POST'])
def newListing():
    title = "New Listing | BenchmarkPC"

    #If The User Is Not Logged In, Redirect To The Login Page
    if current_user.is_anonymous:
        return redirect('/login')

    #Define The Listing Form
    form = newListingForm()

    #Check If POST Request
    if request.method == 'POST':
        #Get The Result Of Processing The Listing,
        #First Argument Is The Error, Second Argument Is The Listing ID.
        message = processListing(request)
        
        #If The Listing Was Processed Correctly, Redirect To The Listing Page.
        if(message[0] == "Passed"):
            return redirect("/listing/" + str(message[1]))
        else:
            #If The Process Listing Failed.
            #Delete Any Images Connected To The Listing.
            Images.query.filter_by(ImageListing=message[1]).delete()
            #Delete The Listing That Was Created.
            Listing.query.filter_by(id=message[1]).delete()
            #Commit These Changes.
            db.session.commit()

            #Give The User The Reason That The New Listing Failed.
            return render_template('createNewListing.html', form=form, title=title, message=message)

    #Render Initial Page
    return render_template('createNewListing.html', form=form, title=title, message=None)

#Manage Page
#Allows The User To Manage Their Current Items.
@app.route('/manage')
def manageListings():

    #If The User Is Not logged In Redirect To Login Page.
    if current_user.is_anonymous:
        return redirect('/login')

    title = "Manage Listings | BenchmarkPC"

    #Get The Users Listings
    listings = Listing.query.filter(
        Listing.userId == current_user.id, Listing.ListingState == 'Open').all()

    listingsAndImages = []
    #Get The Listings Images.
    for listing in listings:
        image = Images.query.filter_by(ImageListing=listing.id).first()
        if(image != None):
            listingsAndImages.append([listing, image.ImageName])
        else:
            listingsAndImages.append([listing])

    #Render The Initial Template
    return render_template('search.html', title=title, listings=listingsAndImages, viewType='manage')

#Route For Previous Page.
#Allows The User To View Their Previous Sales
@app.route('/previous')
def viewOldListings():

    #If The User Is Not Logged In, Redirect To The Login Page.
    if current_user.is_anonymous:
        return redirect('/login')

    title = "Viewing Old Listings | BenchmarkPC"

    #Get The Listings For The Current User That Are Closed.
    listings = Listing.query.filter(
        Listing.userId == current_user.id, Listing.ListingState == 'Closed').all()

    listingsAndImages = []
    listingIDS = []

    #Get The Images For Each Listing
    for listing in listings:
        print("Getting Image")
        image = Images.query.filter_by(ImageListing=listing.id).first()
        if(image != None):
            listingsAndImages.append([listing, image.ImageName])
        else:
            listingsAndImages.append([listing])
        listingIDS.append(listing.id)

    #Get The Sales Listings For Each Listings.
    sales = Sales.query.filter(Sales.ListingID.in_(listingIDS)).all()
    for sale in sales:
        user = User.query.filter_by(id=sale.BuyerID).first()
        sale.BuyerID = user.username

    #Render The Page.
    return render_template('search.html', title=title, listings=listingsAndImages, viewType='previous', sales=sales)

#Route For Manage Item Page
#This Page Allows The User To Manage One Of Their Listings.
@app.route('/manage/<id>', methods=['GET', 'POST'])
def manageListing(id):
    #Create The Form
    form = manageListingForm()

    #Check If POST Request
    if(request.method == "POST"):
        #Check If The User Is Updating The Listing,
        #Or If They Are Selecting A Bid.
        if('UpdateListing' in request.form):
            #Updates The Listing
            UpdateListing(request, id)
            #Redirects Back To The Same Page
            return redirect('/manage/' + id)
        elif('selectBid' in request.form):
            #Get The Bids For The Listing
            bid = Bids.query.filter_by(
                id=request.form.get('bidID')).first_or_404()
            
            #Check That The Bid The User Selected Is Actually One Of The Bids For The Listing.
            if(int(bid.bidListing) != int(id)):
                return redirect('/')

            #Get The Current Listing
            listing = Listing.query.filter_by(id=id).first()
            #Change The State Of The Listing To Closed.
            listing.ListingState = 'Closed'
            #Create A New Sale Using The Current Listing
            sale = Sales(ListingID=listing.id, BuyerID=bid.bidUser,
                         SalePrice=bid.bidAmount)

            #Delete All The Bids For The Listing.
            Bids.query.filter_by(bidListing=listing.id).delete()
            #Add And Commit The Sale
            db.session.add(sale)
            db.session.commit()
            #Redirect To The Viewing Page For The Listing
            return redirect('/listing/' + id)
    #If Get Request, Do This.
    else:
        title = "Managing Listing {0} | BenchmarkPC".format(id)
        #Get The Current Listing, Or 404
        listing = Listing.query.filter_by(id=id).first_or_404()
        #If The Listing Is Already Sold, Redirect To Viewing The Listing
        if(listing.ListingState == 'Closed'):
            return redirect('/listing/' + id)
        
        #Get The Bids For The Listing
        listingBids = Bids.query.filter_by(bidListing=id)
        bidUsers = []
        listingBidsLists = []
        for i in listingBids:
            bidUsers.append(User.query.filter_by(id=i.bidUser).first())
            listingBidsLists.append(i)

        combinedList = [bidUsers, listingBidsLists]
        length = len(listingBidsLists)
        #If The User Is Not Logged In Redirect To Login
        if current_user.is_anonymous:
            return redirect('/login')
        #If The Current User Is Not The Owner Of The Listing, Redirect To Index
        elif current_user.id != listing.userId:
            return redirect("/")

        #Get The Image For The Listing
        image = Images.query.filter_by(ImageListing=listing.id)
        if(image.scalar() is not None):
            image = "\\static\\Images\\" + image.first().ImageName
        else:
            image = r"\static\placeholder.png"

        #Check What Type The Listing Is And Return The Correct Tempalte.
        if(listing.ListingType == "Case"):
            case = Case.query.filter_by(caseListing=id).first_or_404()
            return render_template('manageListingTemplates/CaseHTML.html', title=title,
                                   bids=combinedList, length=length, listing=listing, case=case, form=form, image=image)
        elif(listing.ListingType == "CPU Cooler"):
            cooler = CPUCooler.query.filter_by(CPUCoolerListing=id).first()
            return render_template('manageListingTemplates/CPUCoolerHTML.html', title=title,
                                   bids=combinedList, length=length, listing=listing, cooler=cooler, form=form, image=image)
        elif(listing.ListingType == "CPU"):
            cpu = CPU.query.filter_by(CPUListing=id).first_or_404()
            print(cpu.Socket)
            print(cpu.Microarchitecture)
            return render_template('manageListingTemplates/CPUHTML.html', title=title,
                                   bids=combinedList, length=length, listing=listing, cpu=cpu, form=form, image=image)
        elif(listing.ListingType == 'Memory'):
            memory = Memory.query.filter_by(memoryListing=id).first_or_404()
            return render_template('manageListingTemplates/memoryHTML.html', title=title,
                                   bids=combinedList, length=length, listing=listing, memory=memory, form=form, image=image)
        elif(listing.ListingType == 'Graphics Card'):
            gpu = GPU.query.filter_by(GPUListing=id).first_or_404()
            return render_template('manageListingTemplates/GPUHTML.html', title=title,
                                   bids=combinedList, length=length, listing=listing, gpu=gpu, form=form, image=image)
        elif(listing.ListingType == 'Power Supply'):
            powerSupply = PowerSupply.query.filter_by(
                PowerSupplyListing=id).first_or_404()
            return render_template('manageListingTemplates/PowerSupplyHTML.html', title=title,
                                   bids=combinedList, length=length, listing=listing, powerSupply=powerSupply, form=form, image=image)
        elif(listing.ListingType == 'Motherboard'):
            motherboard = Motherboard.query.filter_by(
                MotherboardListing=id).first_or_404()
            return render_template('manageListingTemplates/MotherboardHTML.html', title=title,
                                   bids=combinedList, length=length, listing=listing, motherboard=motherboard, form=form, image=image)




#Route For Listings
#Allows The User To View A Listing
@app.route('/listing/<id>', methods=['GET', 'POST'])
def viewListingNumber(id):
    title = "Listing | BenchmarkPC"

    #Get The Listing Details
    listing = Listing.query.filter_by(id=id).first_or_404()
    #Get The Listing Owners Details
    user = User.query.filter_by(id=listing.userId).first()

    #Get The Date The Listing Was Created
    date = str(listing.ListingTimeStamp.day) + "/" + \
        str(listing.ListingTimeStamp.month) + \
        "/" + str(listing.ListingTimeStamp.year)

    #Create The Bid Form
    form = bidForm()

    #If The Request Method Is A POST Request.
    if(request.method == "POST"):
        #If The User Is Not Logged In, Redirect To Login.
        if(current_user.is_anonymous):
            return redirect('/login')
        #Check If The User Already Has A Bid.
        exists = db.session.query(Bids.bidUser).filter_by(
            bidUser=current_user.id).first()

        #Get The Bid Amount From The Form
        bidMoney = request.form.get("bid")

        #If The User Already Has A Bid, Replace That Bid
        if(exists is not None):
            bid = Bids.query.filter_by(
                bidUser=current_user.id, bidListing=id).first()
            bid.bidAmount = bidMoney
        #Else, Create A New Bid.
        else:
            bid = Bids(bidAmount=bidMoney,
                       bidUser=current_user.id, bidListing=id)
        #Commit The Bid To The Database.
        db.session.add(bid)
        db.session.commit()

    #Get Listing Image
    image = Images.query.filter_by(ImageListing=listing.id).first()
    if(image is not None):
        image = "\\static\\Images\\" + image.ImageName
    else:
        image = r"\static\placeholder.png"

    #Return Appropriate Template
    if(listing.ListingType == "CPU"):
        details = CPU.query.filter_by(CPUListing=listing.id).first()
        return render_template("ViewListingTemplates/CPUListing.html", title=title,
                               listing=listing, user=user, date=date, details=details, form=form, image=image)

    elif(listing.ListingType == "Graphics Card"):
        details = GPU.query.filter_by(GPUListing=listing.id).first()
        return render_template("ViewListingTemplates/GPUListing.html", title=title,
                               listing=listing, user=user, date=date, details=details, form=form, image=image)

    elif(listing.ListingType == "CPU Cooler"):
        details = CPUCooler.query.filter_by(
            CPUCoolerListing=listing.id).first()
        return render_template("ViewListingTemplates/CPUCooler.html", title=title,
                               listing=listing, user=user, date=date, details=details, form=form, image=image)

    elif(listing.ListingType == "Memory"):
        details = Memory.query.filter_by(memoryListing=listing.id).first()
        return render_template("ViewListingTemplates/Memory.html", title=title,
                               listing=listing, user=user, date=date, details=details, form=form)

    elif(listing.ListingType == "Case"):
        details = Case.query.filter_by(caseListing=listing.id).first()
        return render_template("ViewListingTemplates/Case.html", title=title,
                               listing=listing, user=user, date=date, details=details, form=form, image=image)

    elif(listing.ListingType == "Power Supply"):
        details = PowerSupply.query.filter_by(
            PowerSupplyListing=listing.id).first()
        return render_template("ViewListingTemplates/PowerSupply.html", title=title,
                               listing=listing, user=user, date=date, details=details, form=form, image=image)

    elif(listing.ListingType == "Motherboard"):
        details = Motherboard.query.filter_by(
            MotherboardListing=listing.id).first()
        return render_template("ViewListingTemplates/Motherboard.html", title=title,
                               listing=listing, user=user, date=date, details=details, form=form, image=image)

    else:
        return redirect("/")

#Route To The Register Page
#Allows The User To Register An Account
#Backend Ensures The User Already Doesn't Exist.
@app.route('/register', methods=['post', 'get'])
def register():

    title = "Register | BenchmarkPC"
    #If The User Is Logged In, Redirect Them To The Landing Page.
    if current_user.is_authenticated:
        return redirect('/')

    #Define The Form
    form = RegisterForm()
    if request.method == "POST":
        #Check If Form Fields Are Correct
        if form.validate_on_submit():
            
            user = User(username=form.user_name.data,
                        email=form.email.data, phone=form.phone_number.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()

            user = User.query.filter_by(id=user.id)
            login_user(user)
            return redirect("/")
        else:
            #Give The User An Error Message.
            return render_template("register.html", form=form,title=title, message="Error: Either Account Already Exists, Or Some Of The Details You Provided Are Incorrect")   
    

    #Render The Initial Page
    return render_template("register.html", form=form, title=title, message=None)

#Route To The Login Page.
#The Login Page Allows The User To Login.
#The Following Function Validates The User Values, And Returns An Appropriate Error Message.
@app.route('/login', methods=['POST', 'GET'])
def login():

    title = "Login | BenchmarkPC"
    form = LoginForm()
    #Check If The Form Is Being Submitted.
    if(request.method == 'POST'):
        #Check If The Form Fields Are Of Correct Type.
        if form.validate_on_submit():
            #Get User From Database
            user = User.query.filter_by(email=form.email.data).first()
            #Check If User Exists Or The Password Is Incorrect.
            if user is None or not user.check_password(form.password.data):
                return render_template("login.html", form=form, title=title, message="Email Or Password Is Incorrect.")

            #Log The User In.
            login_user(user)
            return redirect("/")
        else:
            #Tell The User Some Details Are Wrong.
            return render_template("login.html",title=title,message="Some Of The Values Provided Are Of The Incorrect Type.")   
    
    #Render The Initial Page.
    return render_template("login.html", form=form, title=title, message=None)


#Error Handling For Page Not Found
@app.errorhandler(404)
def not_found(e):
    return render_template('404Error.html')


#Error Handling For Internal Server Error
@app.errorhandler(500)
def not_found500(e):
    return render_template('500Error.html')


#Route For Logging The User Out Of The Website.
@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")


#Route For The Search Function
#Allows The User To Search By Text And Type
@app.route('/search')
def seach():
    #Check If The Request Has 1 Arguments,
    #Meaning That The User Is Searching By Just Text
    if(len(request.args) == 1):
        
        #Search For The Text Using Like Search
        #Only Return Non-Closed Listings
        listings = Listing.query.filter(Listing.ListingName.ilike(
            "%" + request.args.get('searchText') + "%"), Listing.ListingState != "Closed").all()

        #Get The Images For Each Listing
        listingsAndImages = []
        for listing in listings:
            image = Images.query.filter_by(ImageListing=listing.id).first()
            if(image != None):
                listingsAndImages.append([listing, image.ImageName])
            else:
                listingsAndImages.append([listing])

        #Return Page With Search Resutls
        return render_template("search.html", listings=listingsAndImages, viewType='search')

    #Check If The Request Has 2 Arguments,
    #Means User Is Searching By Text And Type.
    elif(len(request.args) == 2):

        #Get Listings
        listings = Listing.query.filter(Listing.ListingName.ilike("%" + request.args.get('searchText') + "%"), Listing.ListingState != "Closed",
                                        Listing.ListingType == request.args.get("type")).all()
        #Get The Images For The Listings
        listingsAndImages = []
        for listing in listings:
            print("Getting Image")
            image = Images.query.filter_by(ImageListing=listing.id).first()
            if(image != None):
                print("Got Image")
                listingsAndImages.append([listing, image.ImageName])
            else:
                listingsAndImages.append([listing])

        #Render The Page With The Search Results
        return render_template("search.html", listings=listingsAndImages, viewType='search')

    #Otherwise Render An Empty Search Result
    return render_template("search.html")


""" #Alternative Page For History
@app.route('/history')
def history():
    if current_user.is_anonymous:
        return redirect('/login')
    title = "Past Sales | BenchmarkPC"
    return render_template("history.html")


@app.route('/currentListings')
def current_listings():
    title = "Current Listings | BenchmarkPC"
    return render_template("currentListings.html")
 """

@app.route('/privacy-policy')
def privacy_policy():
    title = "Privacy Policy | BenchmarkPC"
    return render_template("privacy-policy.html")


@app.route('/terms-conditions')
def terms_of_usage():
    title = "Terms Of Usage | BenchmarkPC"
    return render_template("terms-conditions.html")


@app.route('/returns')
def returns_policy():
    title = "Return Policy | BenchmarkPC"
    return render_template("return-policy.html")


@app.route('/about-us')
def about_us():
    title = "About Us | BenchmarkPC"
    return render_template("about-us.html")


@app.route('/contact')
def contact_us():
    title = "Contact Us | BenchmarkPC"
    return render_template("contact-us.html")


@app.route('/careers')
def careers():
    title = "Careers | BenchmarkPC"
    return render_template("careers.html")
