from bench import app, db
from bench.models import User, Listing, Case, Memory, CPUCooler, Motherboard, CPU, GPU, PowerSupply, Images
from flask import render_template, request, flash, redirect
from forms import LoginForm, RegisterForm, newListingForm
from flask_login import current_user, login_user, logout_user
from werkzeug.utils import secure_filename
import os

def UpdateListing(request, idL):
    print("Updating Listing")
    name = request.form.get('ListingName')
    price = request.form.get('Price')
    description = request.form.get('ListingDescription')

    print("Request")
    print(request.form)
    print("End Request")
    print("Listing Name: " + name)
    listing = Listing.query.filter_by(id=idL).first()
    listingType = listing.ListingType

    if(name == ""):
        name = listing.ListingName
    if(price == ""):
        price = listing.ListingPrice

    listing.ListingName = name
    listing.ListingPrice = price
    listing.ListingDescription = description

    if(listingType == "Case"):
        values = getCaseValues(request)

        case = Case.query.filter_by(caseListing=listing.id).first()
        case.manufacturer=values.get('manufacturer')
        case.colour=values.get('Colour')
        case.sidePanel=values.get('SidePanel')
        case.internal25Bays=values.get('Bays25')
        case.internal35Bays=values.get('Bays35')

        db.session.commit()

    elif(listingType == "Memory"):
        values = getMemoryValues(request)
        memory = Memory.query.filter_by(memoryListing=listing.id).first()

        memory.manufacturer = values.get('manufacturer')
        memory.colour = values.get('colour')
        memory.memoryType=values.get('memoryType')
        memory.speed=values.get('memorySpeed')
        memory.modules=values.get('modules')

        db.session.commit()
    elif(listingType == "CPU"):
        cpu = CPU.query.filter_by(CPUListing=listing.id).first()
        values = getCPUValues(request)
        

        cpu.manufacturer=values.get('manufacturer')
        cpu.TDP=values.get('TDP')
        cpu.CoreCount=values.get('CoreCount')
        cpu.CoreClock=values.get('CoreClock')
        cpu.BoostClock=values.get('BoostClock')
        cpu.Series=values.get('Series')
        cpu.Microarchitecture=values.get('Microarchitecture')
        cpu.Socket=values.get('Socket')
        cpu.IntegratedGraphics=values.get('IntegratedGraphics')
        cpu.IncludesCPUCooler=values.get('IncludesCPUCooler')
        
        db.session.commit()
    elif(listingType == "CPU Cooler"):

        print(request.args)
        cooler = CPUCooler.query.filter_by(CPUCoolerListing=listing.id).first()
        print(cooler)
        print(CPUCooler.query.all())
        values = getCPUCoolerValues(request)      
        cooler.manufacturer=values.get('manufacturer')
        cooler.FanRPM=values.get('RPM')
        cooler.NoiseLevel=values.get('Noise')
        cooler.Height=values.get('Height')
        cooler.WaterCooled=values.get('WaterCooled')
        cooler.Fanless=values.get('Fanless')
        cooler.Socket=values.get('socket')

        db.session.commit()
    elif(listingType == "Graphics Card"):
        values = getGPUValues(request)
        gpu = GPU.query.filter_by(GPUListing=listing.id).first()
        
        gpu.manufacturer=values.get('manufacturer')
        gpu.Chipset=values.get('Chipset')
        gpu.MemoryType=values.get('MemoryType')
        gpu.CoreClock=values.get('CoreClock')
        gpu.BoostClock=values.get('BoostClock')
        gpu.colour=values.get('colour')
        gpu.Length=values.get('Length')
        gpu.TDP=values.get('TDP')
        gpu.DVIPorts=values.get('DVIPorts')
        gpu.HDMIPorts=values.get('HDMIPorts')
        gpu.MiniHDMIPorts=values.get('MiniHDMIPorts')
        gpu.DisplayPortPorts=values.get('DisplayPortPorts')
        gpu.MiniDisplayPortPorts=values.get('MiniDisplayPortPorts')
        gpu.CoolingType=values.get('CoolingType')

        db.session.commit()
    elif(listingType == "Power Supply"):
        values = getPowerSupplyValues(request)
        powerSupply = PowerSupply.query.filter_by(PowerSupplyListing=listing.id).first()
        powerSupply.manufacturer=values.get('manufacturer')
        powerSupply.EffiencyRating=values.get('EffiencyRating')
        powerSupply.Wattage=values.get('Wattage')
        powerSupply.Modular=values.get('Modular')
        powerSupply.SATAConnectors=values.get('SATAConnectors')
        db.session.commit()
    elif(listingType == "Motherboard"):
        values = getMotherboardValues(request)
        motherboard = Motherboard.query.filter_by(MotherboardListing=listing.id).first()

        motherboard.manufacturer=values.get('manufacturer')
        motherboard.Socket=values.get('Socket')
        motherboard.RAMslots=values.get('RamSlots')
        motherboard.MaxRAM=values.get('MaxRam')
        motherboard.colour=values.get('colour')
        motherboard.Chipset=values.get('Chipset')
        motherboard.MemoryType=values.get('MemoryType')
        motherboard.SLISupport=values.get('SLI')
        motherboard.CrossFireSupport=values.get('CrossFire')
        motherboard.PCIEx16Slots=values.get('x16')
        motherboard.PCIEx8Slots=values.get('x8')
        motherboard.PCIEx4Slots=values.get('x4')
        motherboard.PCIEx1Slots=values.get('x1')
        motherboard.PCISlots=values.get('PCI')
        motherboard.SATAPorts=values.get('SATA')
        motherboard.M2Slots=values.get('M2')
        motherboard.mSata=values.get('mSATA')
        motherboard.OnboardUSB3Headers=values.get('USB3')
        motherboard.OnboardWifi=values.get('Wifi')
        motherboard.RAIDSupport=values.get('RAID')

        db.session.commit()










def processListing(request):
    print("Creating New Lisiting")
    type = request.form.get('productType')
    price = request.form.get('productPrice')
    description = request.form.get('productDescription')
    name = request.form.get('productName')

    detailList = { "type" : type, "price" : price, "description" : description, "name" : name}
    
    cpuScore = request.form.get('cpuScore')
    

    

    listing = Listing(
        ListingName=detailList["name"], 
        ListingPrice=detailList["price"],
        ListingType=detailList["type"], 
        ListingDescription=detailList["description"],
        userId=current_user.id, ListingScore=cpuScore)

    db.session.add(listing)
    db.session.commit()

    ListingID = listing.id


    error = notNull(detailList)
    if(error == False):
        pass
    else:
        return [error,ListingID]
    if(priceCheck(detailList['price']) == False):
        return ["Price Error", ListingID ]

    error = upload_image(ListingID,request)
    if(error != "Passed"):
        Listing.query.filter_by(id=ListingID).delete()
        db.session.commit()
        return [error, ListingID]
    
    if(type == "Case"):
        return [processCase(request,ListingID),ListingID] 
    elif(type == "Memory"):
        return [processMemory(request, ListingID), ListingID]
    elif(type == "CPU Cooler"):
        return [processCPUCooler(request, ListingID), ListingID]
    elif(type == "Motherboard"):
        return [processMotherBoard(request, ListingID), ListingID ]
    elif(type == "CPU"):
        return [processCPU(request, ListingID), ListingID]
    elif(type == "Graphics Card"):
        return [processGPU( request, ListingID), ListingID] 
    elif(type == "Power Supply"):
        return [processPowerSupply(request, ListingID), ListingID]
    else:
        return ["No Type Selected", ListingID]






def getCPUCoolerValues(request):
    return {
        "manufacturer": request.form.get('Manufacturer'),
        "RPM": request.form.get('Fan RPM'),
        "Noise": request.form.get('Fan Noise Level'),
        "Height": request.form.get('Cooler Height'),
        "socket": request.form.get('Socket'),
        "WaterCooled": request.form.get('WaterCooled'),
        "Fanless": request.form.get('Fanless')
    }

def allowed_image(filename):
    if not "." in filename:
        return False
    if(filename.lower().endswith(('.png','.jpg','.jpeg'))):
        return True
    else:
        return False


def upload_image(id, request):
    print(request.files)
    if request.files:
        image = request.files["file"]
        if image.filename == "":
            return "Passed"
        if allowed_image(image.filename):
            if(image.filename.lower().endswith('.png')):
                image.filename = str(id) + '.png'
            elif(image.filename.lower().endswith('.jpg')):
                image.filename = str(id) + '.jpg'
            elif(image.filename.lower().endswith('.jpeg')):
                image.filename = str(id) + '.jpeg'
                
            filename = secure_filename(image.filename)
            
            image.save(os.path.join(app.config["UPLOAD_FOLDER"],filename ))
            image = Images(ImageName=filename,ImageListing=id)
            db.session.add(image)
            db.session.commit()
            
            return "Passed"
        else:
            return "Not Correct File Type"

def getCaseValues(request):
    return {
        "manufacturer": request.form.get('Manufacturer'),
        "Colour": request.form.get('CaseColour'),
        "SidePanel": request.form.get('SidePanel'),
        "Bays25": request.form.get('2.5Bays'),
        "Bays35": request.form.get('3.5Bays')
    }


def getCPUValues(request):
    return {
        "manufacturer": request.form.get('Manufacturer'),
        "TDP": request.form.get('TDP'),
        "CoreCount": request.form.get('Core Count'),
        "CoreClock": request.form.get('Core Clock'),
        "BoostClock": request.form.get('Boost Clock'),
        "Series": request.form.get('Series'),
        "Microarchitecture": request.form.get('Microarchitecture'),
        "Socket": request.form.get('Socket'),
        "IntegratedGraphics": request.form.get('IntegratedGraphics'),
        "IncludesCPUCooler": request.form.get('CPUCooler')
    }


def getGPUValues(request):
    return {
        "manufacturer": request.form.get('Manufacturer'),
        "Chipset": request.form.get('Chipset'),
        "MemoryType": request.form.get('MemoryType'),
        "CoreClock": request.form.get('CoreClock'),
        "BoostClock": request.form.get('BoostClock'),
        "colour": request.form.get('GPUColour'),
        "Length": request.form.get('Length'),
        "TDP": request.form.get('TDP'),
        "DVIPorts": request.form.get('DVI'),
        "HDMIPorts": request.form.get('HDMI'),
        "MiniHDMIPorts": request.form.get('Mini-HDMI'),
        "DisplayPortPorts": request.form.get('DisplayPort'),
        "MiniDisplayPortPorts": request.form.get('Mini-DisplayPort'),
        "CoolingType": request.form.get('CoolingType')
    }


def getPowerSupplyValues(request):

    return {
        "manufacturer": request.form.get('Manufacturer'),
        "EffiencyRating": request.form.get('Effiency Rating'),
        "Wattage": request.form.get('Wattage'),
        "Modular": request.form.get('Modular'),
        "SATAConnectors": request.form.get('SATA')
    }


def getMotherboardValues(request):

    return {
        "manufacturer": request.form.get('Manufacturer'),
        "Socket": request.form.get('Socket'),
        "RamSlots": request.form.get('RAMSlots'),
        "MaxRam": request.form.get('RAMMax'),
        "SATAConnectors": request.form.get('SATA'),
        "colour": request.form.get('Colour'),
        "Chipset": request.form.get('Chipset'),
        "MemoryType": request.form.get('MemoryType'),
        "SLI": request.form.get('SLI'),
        "CrossFire": request.form.get('CrossFire'),
        "x16": request.form.get('x16'),
        "x8": request.form.get('x8'),
        "x4": request.form.get('x4'),
        "x1": request.form.get('x1'),
        "PCI": request.form.get('PCI'),
        "SATA": request.form.get('SATA'),
        "mSATA": request.form.get('mSATA'),
        "M2": request.form.get('M.2'),
        "USB3": request.form.get('USB3'),
        "WiFi": request.form.get('WiFi'),
        "RAID": request.form.get('RAID')
    }


def getMemoryValues(request):
    return {
        "manufacturer": request.form.get('Manufacturer'),
        "memoryType": request.form.get('MemoryType'),
        "memorySpeed": request.form.get('RAMSpeed'),
        "modules": request.form.get('Modules'),
        "colour": request.form.get('RAMColour')}


def priceCheck(price):
    if(isDecimal(price) == False or float(price) < 0):
        return False
    else:
        return True


def notNull(detailList):
    if(detailList["type"] == ""):
        return "Invalid Type"
    elif(detailList["price"] == ""):
        return "Invalid Price"
    elif(detailList["name"] == ""):
        return "Invalid Name"
    return False




def processCase(request, id):
    values = getCaseValues(request)
    
    error = manufacturerError(values.get('manufacturer'))
    if(error != "Passed"):
        return error

    if(values.get('Bays25').isdigit() == False or values.get('Bays35').isdigit() == False):
        values.update({'Bays25': 0})
        values.update({'Bays35': 0})
    else:
        values.update({'Bays25': int(values.get('Bays25'))})
        values.update({'Bays35': int(values.get('Bays35'))})    

        

    case = Case(manufacturer=values.get('manufacturer'), colour=values.get('Colour'), sidePanel=values.get('SidePanel'),
                internal25Bays=values.get('Bays25'),
                internal35Bays=values.get('Bays35'),
                caseListing=id)
    db.session.add(case)
    db.session.commit()

    return "Passed"

def manufacturerError(manufacturer):
    if(manufacturer == ""):
        return "No Value For Manufacturer Provided"
    else:
        return "Passed"
def processMemory(request, id):
    values = getMemoryValues(request)

    error = manufacturerError(values.get('manufacturer'))
    if(error != "Passed"):
        return error
        
    if(values.get('modules').isdigit() == False):
        values.update({'modules' : 1})

    if(values.get('memorySpeed').isdigit() == False):
        return "Memory Speed Not Provided Or In Incorrect Format"

    values.update({'modules': int(values.get('modules'))})
    values.update({'memorySpeed': int(values.get('memorySpeed'))})

    

    memory = Memory(
        manufacturer=values.get('manufacturer'),
        colour=values.get('colour'),
        memoryType=values.get('memoryType'),
        speed=values.get('memorySpeed'),
        modules=values.get('modules'),
        memoryListing=id)
    db.session.add(memory)
    db.session.commit()

    return "Passed"


def processCPUCooler(request, id):
    values = getCPUCoolerValues(request)
    
    error = manufacturerError(values.get('manufacturer'))
    if(error != "Passed"):
        return error

    if(isDecimal(values.get('Height')) == False):
        return "Height Not Provided In Decimal Form"

    if(values.get('Noise').isdigit() == False):
        return "Noise Was Not Provided In Integer Form"


    if(values.get('RPM').isdigit() == False):
        return "RPM Not Provided As An Integer"
        
    values.update({'Height':  int(values.get('Height'))})
    values.update({'Noise':  int(values.get('Noise'))})
    values.update({'RPM': int(values.get('RPM'))})

    

    Cooler = CPUCooler(
        manufacturer=values.get('manufacturer'),
        FanRPM=values.get('RPM'),
        NoiseLevel=values.get('Noise'),
        Height=values.get('Height'),
        WaterCooled=values.get('WaterCooled'),
        Fanless=values.get('Fanless'),
        CPUCoolerListing=id,
        Socket=values.get('socket'))
    db.session.add(Cooler)
    db.session.commit()

    return "Passed"


def processMotherBoard(request, id):
    values = getMotherboardValues(request)

    error = manufacturerError(values.get('manufacturer'))
    if(error != "Passed"):
        return error

    IntegerKeys = [
        'RamSlots',
        'MaxRam',
        'SATAConnectors',
        'x16',
        'x8',
        'x4',
        'x1',
        'PCI',
        'SATA',
        'mSATA',
        'M2'
    ]
    for key in IntegerKeys:
        if(values.get(key).isdigit() == False
           or int(values.get(key)) < 0):
            values.update({key: 0})

    

    # Create The Motherboard Object And Add It To The Database
    MotherBoard = Motherboard(
        manufacturer=values.get('manufacturer'),
        Socket=values.get('Socket'),
        RAMslots=values.get('RamSlots'),
        MaxRAM=values.get('MaxRam'),
        colour=values.get('colour'),
        Chipset=values.get('Chipset'),
        MemoryType=values.get('MemoryType'),
        SLISupport=values.get('SLI'),
        CrossFireSupport=values.get('CrossFire'),
        PCIEx16Slots=values.get('x16'),
        PCIEx8Slots=values.get('x8'),
        PCIEx4Slots=values.get('x4'),
        PCIEx1Slots=values.get('x1'),
        PCISlots=values.get('PCI'),
        SATAPorts=values.get('SATA'),
        M2Slots=values.get('M2'),
        mSata=values.get('mSATA'),
        OnboardUSB3Headers=values.get('USB3'),
        OnboardWifi=values.get('Wifi'),
        RAIDSupport=values.get('RAID'),
        MotherboardListing=id
    )
    db.session.add(MotherBoard)
    db.session.commit()

    return "Passed"


def processCPU(request, id):
    values = getCPUValues(request)

    error = manufacturerError(values.get('manufacturer'))
    if(error != "Passed"):
        return error
    elif(values.get('CoreCount') == None or values.get('CoreCount').isdigit() == False):
        return "Core Count Not Proivded, Or Is Not Proivded In The Correct Format"
    elif(values.get('CoreClock') == None or not isDecimal(values.get('CoreClock'))):
        return "Core Clock Not Provided, Or Is Proivded In The Correct Format"
    elif(values.get('BoostClock') == None or not isDecimal(values.get('BoostClock'))):
        return "Boost Clock Value Is Not Proivded, Or Is Provided In The Wrong Format"
    elif(values.get('TDP') == None or not values.get('TDP').isdigit()):
        values.update({'TDP' : "Unknown"})
    elif(values.get('IntegratedGraphics') not in ["Yes", "No"]):
        values.update({"IntegratedGraphics" : "No"})
    elif(values.get('IncludesCPUCooler') not in ["Yes", "No"]):
        values.update({"IncludesCPUCooler" : "No"})

    cpu = CPU(
        manufacturer=values.get('manufacturer'),
        TDP=values.get('TDP'),
        CoreCount=values.get('CoreCount'),
        CoreClock=values.get('CoreClock'),
        BoostClock=values.get('BoostClock'),
        Series=values.get('Series'),
        Microarchitecture=values.get('Microarchitecture'),
        Socket=values.get('Socket'),
        IntegratedGraphics=values.get('IntegratedGraphics'),
        IncludesCPUCooler=values.get('IncludesCPUCooler'),
        CPUListing=id)

    db.session.add(cpu)
    db.session.commit()

    return "Passed"


def processGPU(request, id):
    values = getGPUValues(request)

    error = manufacturerError(values.get('manufacturer'))
    if(error != "Passed"):
        return error
    elif(not isDecimal(values.get('CoreClock')) or float(values.get('CoreClock')) <= 0):
        return "Core Clock Is Not A Decimal Or Is Equal To Or Less Than 0"
    elif(not isDecimal(values.get('BoostClock')) or float(values.get('BoostClock')) <= 0):
        return "Boost Clock Is Not A Decimal Or Is Equal To Or Less Than 0"
    elif(not isDecimal(values.get('Length')) or float(values.get('Length')) <= 0):
        return "Length Is Not A Decimal Or Is Equal To Or Less Than 0"
    elif(not values.get('TDP').isdigit() or int(values.get('TDP')) < 0):
        return "TDP Is Not A Integer Or Is Less Than 0"
    elif(not values.get('DVIPorts').isdigit() or int(values.get('DVIPorts')) < 0):
        values.update({"DVIPorts" : 0})
    elif(not values.get('HDMIPorts').isdigit() or int(values.get('HDMIPorts')) < 0):
        values.update({"HDMIPorts" : 0})
    elif(not values.get('MiniHDMIPorts').isdigit() or int(values.get('MiniHDMIPorts')) < 0):
        values.update({"MiniHDMIPorts" : 0})
    elif(not values.get('DisplayPortPorts').isdigit() or int(values.get('DisplayPortPorts')) < 0):
        values.update({"DisplayPortPorts" : 0})
    elif(not values.get('MiniDisplayPortPorts').isdigit() or int(values.get('MiniDisplayPortPorts')) < 0):
        values.update({"MiniDisplayPortPorts" : 0})
    elif(values.get('CoolingType') not in ["Blower", "Fan"]):
        values.update({"CoolingType" : "Fan"})

    
    gpu = GPU(
        manufacturer=values.get('manufacturer'),
        Chipset=values.get('Chipset'),
        MemoryType=values.get('MemoryType'),
        CoreClock=values.get('CoreClock'),
        BoostClock=values.get('BoostClock'),
        colour=values.get('colour'),
        Length=values.get('Length'),
        TDP=values.get('TDP'),
        DVIPorts=values.get('DVIPorts'),
        HDMIPorts=values.get('HDMIPorts'),
        MiniHDMIPorts=values.get('MiniHDMIPorts'),
        DisplayPortPorts=values.get('DisplayPortPorts'),
        MiniDisplayPortPorts=values.get('MiniDisplayPortPorts'),
        CoolingType=values.get('CoolingType'),
        GPUListing=id)

    db.session.add(gpu)
    db.session.commit()
    
    return "Passed"


def processPowerSupply(request, id):
    values = getPowerSupplyValues(request)

    error = manufacturerError(values.get('manufacturer'))
    if(error != "Passed"):
        return error
    elif(values.get('Wattage') == None or not values.get('Wattage').isdigit() or int(values.get('Wattage')) < 1):
        return "Wattage Not Given As An Interger Or Is Less Than 1"
    elif(values.get('SATAConnectors') == None or not values.get('SATAConnectors').isdigit() or int(values.get('SATAConnectors')) < 0):
        return "Sata Connectors Not Given As An Interger Or Less Than 0"
    elif(values.get('EffiencyRating') == None):
        return "Effiency Rating Not Given"
    elif(values.get('Modular') == None or values.get('Modular') not in ["Full", "Semi", "None"]):
        return "Modular Status Not Given Or Does Not Match Any Of The Dropdown Values"

   

    powerSupply = PowerSupply(
        manufacturer=values.get('manufacturer'),
        EffiencyRating=values.get('EffiencyRating'),
        Wattage=values.get('Wattage'),
        Modular=values.get('Modular'),
        SATAConnectors=values.get('SATAConnectors'),
        PowerSupplyListing=id)

    db.session.add(powerSupply)
    db.session.commit()

    return "Passed"


def isDecimal(number):
    try:
        float(number)
        return True
    except ValueError:
        return False
