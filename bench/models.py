from bench import db, login_manager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    listings = db.relationship('Listing', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Listing(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        ListingScore = db.Column(db.Integer, nullable=True)

        ListingName = db.Column(db.String(80), unique=True, nullable=False)
        ListingPrice  = db.Column(db.String(80), unique = False, nullable=False)
        ListingType = db.Column(db.String(80), unique = False, nullable=False)
        ListingDescription = db.Column(db.String(80), unique = False, nullable=False, default="Empty")
        ListingTimeStamp = db.Column(db.DateTime, default=datetime.datetime.utcnow(), nullable=False)

        userId = db.Column(db.Integer, db.ForeignKey('user.id'))
        metadataID = db.Column(db.Integer, db.ForeignKey('metadata.id'))

class Bids(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        bidAmount = db.Column(db.String(80), nullable=False, default="Intel")
        bidUser = db.Column(db.Integer, db.ForeignKey('user.id'))
        bidListing = db.Column(db.Integer, db.ForeignKey('listing.id'))
        bidTimeStamp = db.Column(db.DateTime, default=datetime.datetime.utcnow())

class Order(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        OrderUser = db.Column(db.Integer, db.ForeignKey('user.id'))





class Metadata(db.Model):

        id = db.Column(db.Integer, primary_key=True) 
        manufacturer = db.Column(db.String(80), nullable=False, default="Intel")
        TDP = db.Column(db.Numeric, nullable=True)
        CoreCount = db.Column(db.Numeric, nullable=True)
        CoreClock = db.Column(db.Numeric, nullable=True)
        BoostClock = db.Column(db.Numeric, nullable=True)
        Series = db.Column(db.String(80), nullable=True)
        Microarchitecture = db.Column(db.String(80), nullable=True)
        Socket = db.Column(db.String(80), nullable=True)
        IntegratedGraphics = db.Column(db.String(80), nullable=True)
        IncludesCPUCooler = db.Column(db.String(80), nullable=True)
        FanRPM = db.Column(db.String(80), nullable=True)
        NoiseLevel = db.Column(db.String(80), nullable=True)
        Height = db.Column(db.Integer, nullable=True)
        WaterCooled = db.Column(db.String(80), nullable=True)
        Fanless = db.Column(db.String(80), nullable=True)
        FormFactor = db.Column(db.String(80), nullable=True)
        RAMslots = db.Column(db.Integer, nullable=True)
        MaxRAM = db.Column(db.Integer, nullable=True)
        Color = db.Column(db.String(80), nullable=True)
        Chipset = db.Column(db.String(80), nullable=True)
        MemoryType = db.Column(db.String(80), nullable=True)
        SLISupport = db.Column(db.String(80), nullable=True)
        CrossFireSupport = db.Column(db.String(80), nullable=True)

        PCIEx16Slots = db.Column(db.Integer, nullable=True)
        PCIEx8Slots = db.Column(db.Integer, nullable=True)
        PCIEx4Slots = db.Column(db.Integer, nullable=True)
        PCIEx1Slots = db.Column(db.Integer, nullable=True)

        PCISlots = db.Column(db.Integer, nullable=True)
        SATAPorts = db.Column(db.Integer, nullable=True)
        M2Slots = db.Column(db.Integer, nullable=True)
        mSata = db.Column(db.Integer, nullable=True)

        OnboardUSB3Headers = db.Column(db.String(80), nullable=True)
        OnboardWifi = db.Column(db.String(80), nullable=True)

        RAIDSupport = db.Column(db.String(80), nullable=True)

        Speed = db.Column(db.Integer, nullable=True)
        Modules = db.Column(db.Integer, nullable=True)

        Interface = db.Column(db.String(80), nullable=True)
        FrameSync = db.Column(db.String(80), nullable=True)


        Length = db.Column(db.Integer, nullable=True)
        DVIPorts = db.Column(db.Integer, nullable=True)
        HDMIPorts = db.Column(db.Integer, nullable=True)

        MiniHDMIPorts = db.Column(db.Integer, nullable=True)
        DisplayPortPorts = db.Column(db.Integer, nullable=True)
        MiniDisplayPortPorts = db.Column(db.Integer, nullable=True)

        CoolingStyle = db.Column(db.String(80), nullable=True)
        EffiencyRating = db.Column(db.String(80), nullable=True)

        Wattage = db.Column(db.Integer, nullable=True)
        Modular = db.Column(db.Integer, nullable=True)
        SATAConnectors = db.Column(db.Integer, nullable=True)

        SidePanel = db.Column(db.String(80), nullable=True)

        Internal25Bays = db.Column(db.Integer, nullable=True)
        Internal35Bays = db.Column(db.Integer, nullable=True)


       









      







    
    
