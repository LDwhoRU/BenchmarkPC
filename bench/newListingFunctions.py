from bench import app, db
from bench.models import User, Listing, Case, Memory, CPUCooler
from flask import render_template, request, flash, redirect
from forms import LoginForm, RegisterForm, newListingForm
from flask_login import current_user, login_user, logout_user

def processListing(request):
    print("Test")
    type = request.form.get('productType')
    price = request.form.get('productPrice')
    description = request.form.get('productDescription')
    name = request.form.get('productName')
    detailList = [type, price, description, name]

    if notNull(detailList) == False:
        return False
    if priceCheck == False:
        return False
    if(type == "Case"):
        if(processCase(detailList, request) == False):
            return False
    elif(type == "Memory"):
        if(processMemory(detailList,request) == False):
            return False
    elif(type == "CPU Cooler"):
            if(processCPUCooler(detailList,request) == False):
                return False
    return True

def priceCheck(price):
    if(price.isdigit() == False or int(price) < 0):
        return False
    else:
        return True
def notNull(detailList):
     for detail in detailList:
        if detail == "":
            return False

def processCase(detailList, request):
    manufacturer = request.form.get('Manufacturer')
    print("Manufacturer: " + manufacturer)
    Colour = request.form.get('CaseColour')
    SidePanel = request.form.get('SidePanel')
    Bays25 = request.form.get('2.5Bays')
    Bays35 = request.form.get('3.5Bays')
    if(manufacturer == ""):
        return False
    if(Bays25.isdigit() == False or Bays35.isdigit() == False):
        return False
    Bays25 = int(Bays25)
    Bays35 = int(Bays35)
    
    listing = Listing(ListingName=detailList[3],ListingPrice=detailList[1],
    ListingType=detailList[0],ListingDescription=detailList[2],
    userId=current_user.id )
    db.session.add(listing)
    db.session.commit()
    listingID = listing.id
    
    case = Case(manufacturer=manufacturer,colour=Colour,sidePanel=SidePanel,
     internal25Bays=Bays25,internal35Bays=Bays35, caseListing=listingID)
    db.session.add(case)
    db.session.commit()

def processMemory(detailList,request):
    print("Memory")
    manufacturer = request.form.get('Manufacturer')
    memoryType = request.form.get('MemoryType')
    memorySpeed = request.form.get('RAMSpeed')
    modules = request.form.get('Modules')
    colour = request.form.get('RAMColour')

    if(manufacturer == ""):
        return False
    if(modules.isdigit() == False or memorySpeed.isdigit() == False):
        return False
    modules = int(modules)
    memorySpeed = int(memorySpeed)
    
    listing = Listing(ListingName=detailList[3],ListingPrice=detailList[1],
    ListingType=detailList[0],ListingDescription=detailList[2],
    userId=current_user.id)
    db.session.add(listing)
    db.session.commit()
    id_ = listing.id

    memory = Memory(manufacturer=manufacturer,colour=colour,memoryType=memoryType, speed=memorySpeed, modules=modules, memoryListing=id_)
    db.session.add(memory)
    db.session.commit()

def processCPUCooler(detailList,request):
    print("COol")
    manufacturer = request.form.get('Manufacturer')
    RPM = request.form.get('Fan RPM')
    Noise = request.form.get('Fan Noise Level')
    Height = request.form.get('Cooler Height')
    Socket = request.form.get('Socket')
    WaterCooled = request.form.get('WaterCooled')
    Fanless = request.form.get('Fanless')
    if(manufacturer == ""):
            return False
    if(Height.isdigit() == False or Noise.isdigit() == False or RPM.isdigit() == False):
            return False
    Height = int(Height)
    Noise = int(Noise)
    RPM = int(RPM)

    listing = Listing(ListingName=detailList[3],ListingPrice=detailList[1],
    ListingType=detailList[0],ListingDescription=detailList[2],
    userId=current_user.id)
    db.session.add(listing)
    db.session.commit()
    id_ = listing.id

    Cooler = CPUCooler(manufacturer=manufacturer,FanRPM=RPM, NoiseLevel=Noise, Height=Height, WaterCooled=WaterCooled, Fanless=Fanless, CPUCoolerListing=id_)
    db.session.add(Cooler)
    db.session.commit()