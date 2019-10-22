from bench import db, login_manager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
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


class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ListingID = db.Column(db.Integer, db.ForeignKey('listing.id'))
    BuyerID = db.Column(db.Integer, db.ForeignKey('user.id'))
    SalePrice = db.Column(db.Numeric, unique=False, nullable=False)
    SaleTimeStamp = db.Column(db.DateTime, default=datetime.datetime.utcnow(), nullable=False)


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ListingScore = db.Column(db.Integer, nullable=True)
    ListingState = db.Column(db.String(80), nullable=True, server_default="Open")
    ListingName = db.Column(db.String(80), unique=False, nullable=False)
    ListingPrice = db.Column(db.Numeric, unique=False, nullable=False)
    ListingType = db.Column(db.String(80), unique=False, nullable=False)
    ListingDescription = db.Column(
        db.String(80), unique=False, nullable=False, default="Empty")
    ListingTimeStamp = db.Column(
        db.DateTime, default=datetime.datetime.utcnow(), nullable=False)

    userId = db.Column(db.Integer, db.ForeignKey('user.id'))


class Bids(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bidAmount = db.Column(db.String(80), nullable=False)
    bidUser = db.Column(db.Integer, db.ForeignKey('user.id'))
    bidListing = db.Column(db.Integer, db.ForeignKey('listing.id'))
    bidTimeStamp = db.Column(db.DateTime, default=datetime.datetime.utcnow())





class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(80), nullable=False)
    colour = db.Column(db.String(80), nullable=True)
    sidePanel = db.Column(db.String(80), nullable=True)
    internal25Bays = db.Column(db.Integer, nullable=True)
    internal35Bays = db.Column(db.Integer, nullable=True)
    caseListing = db.Column(db.Integer, db.ForeignKey('listing.id'))


class Memory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(80), nullable=False)
    memoryType = db.Column(db.String(80), nullable=True)
    modules = db.Column(db.Integer, nullable=True)
    colour = db.Column(db.String(80), nullable=True)
    speed = db.Column(db.Integer, nullable=True)

    memoryListing = db.Column(db.Integer, db.ForeignKey('listing.id'))


class CPU(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(80), nullable=False)
    TDP = db.Column(db.Numeric, nullable=True)
    CoreCount = db.Column(db.Numeric, nullable=True)
    CoreClock = db.Column(db.Numeric, nullable=True)
    BoostClock = db.Column(db.Numeric, nullable=True)
    Series = db.Column(db.String(80), nullable=True)
    Microarchitecture = db.Column(db.String(80), nullable=True)
    Socket = db.Column(db.String(80), nullable=True)
    IntegratedGraphics = db.Column(db.String(80), nullable=True)
    IncludesCPUCooler = db.Column(db.String(80), nullable=True)
    CPUListing = db.Column(db.Integer, db.ForeignKey('listing.id'))


class CPUCooler(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(80), nullable=False)
    FanRPM = db.Column(db.String(80), nullable=True)
    NoiseLevel = db.Column(db.String(80), nullable=True)
    Height = db.Column(db.Integer, nullable=True)
    WaterCooled = db.Column(db.String(80), nullable=True)
    Socket = db.Column(db.String(80), nullable=True)
    Fanless = db.Column(db.String(80), nullable=True)
    CPUCoolerListing = db.Column(db.Integer, db.ForeignKey('listing.id'))


class Motherboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Done
    manufacturer = db.Column(db.String(80), nullable=False)
    # Done
    Socket = db.Column(db.String(80), nullable=True)
    # Done
    RAMslots = db.Column(db.Integer, nullable=False, default=0)
    # Done
    MaxRAM = db.Column(db.Integer, nullable=False, default=0)
    # Done
    colour = db.Column(db.String(80), nullable=True)
    # Done
    Chipset = db.Column(db.String(80), nullable=True)

    # Done
    MemoryType = db.Column(db.String(80), nullable=True)
    # Done
    SLISupport = db.Column(db.String(80), nullable=True)
    # Done
    CrossFireSupport = db.Column(db.String(80), nullable=True)

    # Done
    PCIEx16Slots = db.Column(db.Integer, nullable=False, default=0)
    PCIEx8Slots = db.Column(db.Integer, nullable=False, default=0)
    PCIEx4Slots = db.Column(db.Integer, nullable=False, default=0)
    PCIEx1Slots = db.Column(db.Integer, nullable=False, default=0)
    PCISlots = db.Column(db.Integer, nullable=False, default=0)
    SATAPorts = db.Column(db.Integer, nullable=False, default=0)
    M2Slots = db.Column(db.Integer, nullable=False, default=0)
    mSata = db.Column(db.Integer, nullable=False, default=0)
    # Here
    # Done
    OnboardUSB3Headers = db.Column(db.String(80), nullable=True)
    OnboardWifi = db.Column(db.String(80), nullable=True)

    RAIDSupport = db.Column(db.String(80), nullable=True)
    MotherboardListing = db.Column(db.Integer, db.ForeignKey('listing.id'))


class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ImageName = db.Column(db.String(80), nullable=False)
    ImageListing = db.Column(db.Integer, db.ForeignKey('listing.id'))


class GPU(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(80), nullable=False)
    Chipset = db.Column(db.String(80), nullable=True)
    MemoryType = db.Column(db.String(80), nullable=True)
    CoreClock = db.Column(db.Numeric, nullable=True)
    BoostClock = db.Column(db.Numeric, nullable=True)
    colour = db.Column(db.String(80), nullable=True)
    Length = db.Column(db.Integer, nullable=True)
    TDP = db.Column(db.Numeric, nullable=True)
    DVIPorts = db.Column(db.Integer, nullable=True)
    HDMIPorts = db.Column(db.Integer, nullable=True)
    MiniHDMIPorts = db.Column(db.Integer, nullable=True)
    DisplayPortPorts = db.Column(db.Integer, nullable=True)
    MiniDisplayPortPorts = db.Column(db.Integer, nullable=True)
    CoolingType = db.Column(db.String(80), nullable=True)
    GPUListing = db.Column(db.Integer, db.ForeignKey('listing.id'))


class PowerSupply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(80), nullable=False)
    EffiencyRating = db.Column(db.String(80), nullable=True)
    Wattage = db.Column(db.Integer, nullable=True)
    Modular = db.Column(db.String(20), nullable=True)
    SATAConnectors = db.Column(db.Integer, nullable=True)
    PowerSupplyListing = db.Column(db.Integer, db.ForeignKey('listing.id'))
