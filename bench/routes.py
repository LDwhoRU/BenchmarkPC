from bench import app
from flask import render_template

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')
@app.route('/newListing')
def newListing():
    return render_template('createNewListing.html')
@app.route('/manage')
def manageListing():
    return render_template('manageListing.html')
@app.route('/Listing')
def viewListing():
    return render_template("view.html")

@app.errorhandler(404)
def not_found(e):
    return render_template('404Error.html')