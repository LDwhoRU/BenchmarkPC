from bench import app, db
from bench.models import User, Listing, Case, Memory, CPUCooler, Motherboard, CPU, GPU, PowerSupply
from flask import render_template, request, flash, redirect
from forms import LoginForm, RegisterForm, newListingForm
from flask_login import current_user, login_user, logout_user


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
        case = Case.query.filter_by(id=idL).first()
        case = Case(
            manufacturer=values.get('manufacturer'),
            colour=values.get('Colour'),
            sidePanel=values.get('SidePanel'),
            internal25Bays=values.get('Bays25'),
            internal35Bays=values.get('Bays35'),
            caseListing=listing.id)

        db.session.add(case)
        db.session.commit()

    elif(listingType == "Memory"):
        values = getMemoryValues(request)
        memory = Memory.query.filter_by(id=idL).first()
        memory = Memory(
            manufacturer=values.get('manufacturer'),
            colour=values.get('colour'),
            memoryType=values.get('memoryType'),
            speed=values.get('memorySpeed'),
            modules=values.get('modules'),
            memoryListing=id_)
        db.session.add(memory)
        db.session.commit()


def processListing(request):
    print("Creating New Lisiting")
    type = request.form.get('productType')
    price = request.form.get('productPrice')
    description = request.form.get('productDescription')
    name = request.form.get('productName')
    detailList = [type, price, description, name]

    if notNull(detailList) == False:
        print("Null Values Detected")
        return False
    if priceCheck(price) == False:
        print("Error: Price Not Correct Format")
        return False
    if(type == "Case"):
        if(processCase(detailList, request) == False):
            return False
    elif(type == "Memory"):
        if(processMemory(detailList, request) == False):
            return False
    elif(type == "CPU Cooler"):
        if(processCPUCooler(detailList, request) == False):
            return False
    elif(type == "Motherboard"):
        if(processMotherBoard(detailList, request) == False):
            return False
    elif(type == "CPU"):
        print("reached Here")
        if(processCPU(detailList, request) == False):
            return False
    elif(type == "Graphics Card"):
        if(processGPU(detailList, request) == False):
            return False
    elif(type == "Power Supply"):
        if(processPowerSupply(detailList, request) == False):
            return False
    else:
        return False
    return True


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
    for detail in detailList:
        if detail == "":
            return False


def processCase(detailList, request):
    values = getCaseValues(request)
    if(values.get('manufacturer') == ""):
        return False
    if(values.get('Bays25').isdigit() == False or values.get('Bays35').isdigit() == False):
        return False
    values.update({'Bays25': int(values.get('Bays25'))})
    values.update({'Bays35': int(values.get('Bays35'))})

    listing = Listing(ListingName=detailList[3], ListingPrice=detailList[1],
                      ListingType=detailList[0], ListingDescription=detailList[2],
                      userId=current_user.id)
    db.session.add(listing)
    db.session.commit()
    listingID = listing.id

    case = Case(manufacturer=values.get('manufacturer'), colour=values.get('Colour'), sidePanel=values.get('SidePanel'),
                internal25Bays=values.get('Bays25'),
                internal35Bays=values.get('Bays35'),
                caseListing=listingID)
    db.session.add(case)
    db.session.commit()


def processMemory(detailList, request):
    print("Memory")
    print(request.form)
    values = getMemoryValues(request)

    if(values.get('manufacturer') == ""):
        return False
    if(values.get('modules').isdigit() == False or values.get('memorySpeed').isdigit() == False):
        return False
    values.update({'modules': int(values.get('modules'))})
    values.update({'memorySpeed': int(values.get('memorySpeed'))})

    listing = Listing(ListingName=detailList[3], ListingPrice=detailList[1],
                      ListingType=detailList[0], ListingDescription=detailList[2],
                      userId=current_user.id)
    db.session.add(listing)
    db.session.commit()
    id_ = listing.id

    memory = Memory(
        manufacturer=values.get('manufacturer'),
        colour=values.get('colour'),
        memoryType=values.get('memoryType'),
        speed=values.get('memorySpeed'),
        modules=values.get('modules'),
        memoryListing=id_)
    db.session.add(memory)
    db.session.commit()


def processCPUCooler(detailList, request):
    print("COol")
    values = getCPUCoolerValues(request)

    if(values.get('manufacturer') == ""):
        print("No Manufacturer")
        return False
    if(values.get('Height') == False or values.get('Noise').isdigit() == False or values.get('RPM').isdigit() == False):
        return False
    values.update({'Height':  int(values.get('Height'))})
    values.update({'Noise':  int(values.get('Noise'))})
    values.update({'RPM': int(values.get('RPM'))})

    listing = Listing(ListingName=detailList[3], ListingPrice=detailList[1],
                      ListingType=detailList[0], ListingDescription=detailList[2],
                      userId=current_user.id)
    db.session.add(listing)
    db.session.commit()
    id_ = listing.id

    Cooler = CPUCooler(
        manufacturer=values.get('manufacturer'),
        FanRPM=values.get('RPM'),
        NoiseLevel=values.get('Noise'),
        Height=values.get('Height'),
        WaterCooled=values.get('WaterCooled'),
        Fanless=values.get('Fanless'),
        CPUCoolerListing=id_,
        Socket=values.get('socket'))
    db.session.add(Cooler)
    db.session.commit()


def processMotherBoard(detailList, request):
    values = getMotherboardValues(request)

    if(values.get('manufacturer') == ""):
        return False

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
            values.update({key, 0})

    # Add The Listing First So The Listing ID Is Available
    listing = Listing(ListingName=detailList[3], ListingPrice=detailList[1],
                      ListingType=detailList[0], ListingDescription=detailList[2],
                      userId=current_user.id)
    db.session.add(listing)
    db.session.commit()
    id_ = listing.id

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
        MotherboardListing=id_
    )
    db.session.add(MotherBoard)
    db.session.commit()

    manufacturer = request.form.get('Manufacturer')


def processCPU(detailList, request):
    values = getCPUValues(request)
    print("Reached Checks")
    if(values.get('manufacturer') == ""):
        print("Error: Manufacturer Check Failed")
        return False
    elif(values.get('CoreCount') == None or values.get('CoreCount').isdigit() == False):
        print("Error: CoreCount Check Failed")
        return False
    elif(values.get('CoreClock') == None or not isDecimal(values.get('CoreClock'))):
        print("Error: Core Clock Check Failed")
        return False
    elif(values.get('BoostClock') == None or not isDecimal(values.get('BoostClock'))):
        print("Error: Boost Clock Check Failed")
        return False
    elif(values.get('TDP') == None or not values.get('TDP').isdigit()):
        return False
    elif(values.get('IntegratedGraphics') not in ["Yes", "No"]):
        print("Error: IntegratedGraphics Check Failed")
        return False
    elif(values.get('IncludesCPUCooler') not in ["Yes", "No"]):
        print("Error: IncludesCPUCooler Check Failed")
        return False
    print("Passed Checks")
    # Add The Listing First So The Listing ID Is Available
    listing = Listing(ListingName=detailList[3], ListingPrice=detailList[1],
                      ListingType=detailList[0], ListingDescription=detailList[2],
                      userId=current_user.id)
    db.session.add(listing)
    db.session.commit()
    id_ = listing.id

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
        CPUListing=id_)

    db.session.add(cpu)
    db.session.commit()


def processGPU(detailList, request):
    values = getGPUValues()

    if(manufacturer == ""):
        return False
    elif(not isDecimal(values.get('CoreClock')) or values.get('CoreClock') <= 0):
        print("Error: Core Clock Check Failed")
        print("Core Clock = " + str(values.get('CoreClock')))
        return False
    elif(not isDecimal(values.get('BoostClock')) or values.get('BoostClock') <= 0):
        print("Error: Boost Clock Check Failed")
        return False
    elif(not isDecimal(values.get('Length')) or values.get('Length') <= 0):
        print("Error: Length Check Failed")
        return False
    elif(not values.get('TDP').isdigit() or values.get('TDP') < 0):
        print("Error: TDP Check Failed")
        return False
    elif(not values.get('DVIPorts').isdigit() or values.get('DVIPorts') < 0):
        print("Error: DVIPorts Check Failed")
        return False
    elif(not values.get('HDMIPorts').isdigit() or values.get('HDMIPorts') < 0):
        print("Error: HDMIPorts Check Failed")
        return False
    elif(not values.get('MiniHDMIPorts').isdigit() or values.get('MiniHDMIPorts') < 0):
        print("Error: MiniHDMIPorts Check Failed")
        return False
    elif(not values.get('DisplayPortPorts').isdigit() or values.get('DisplayPortPorts') < 0):
        print("Error: DisplayPortPorts Check Failed")
        return False
    elif(not values.get('MiniDisplayPortPorts').isdigit() or values.get('MiniDisplayPortPorts') < 0):
        print("Error: MiniDisplayPortPorts Check Failed")
        return False
    elif(values.get('CoolingType') not in ["Blower", "Fan"]):
        print("Error: CoolingType Check Failed")
        return False

    # Add The Listing First So The Listing ID Is Available
    listing = Listing(ListingName=detailList[3], ListingPrice=detailList[1],
                      ListingType=detailList[0], ListingDescription=detailList[2],
                      userId=current_user.id)
    db.session.add(listing)
    db.session.commit()
    id_ = listing.id

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
        GPUListing=id_)

    db.session.add(gpu)
    db.session.commit()
    print("Commit GPU")


def processPowerSupply(detailList, request):
    values = getPowerSupplyValues(request)

    if(values.get('manufacturer') == ""):
        return False
    elif(values.get('Wattage') == None or not values.get('Wattage').isdigit() or values.get('Wattage') < 1):
        return False
    elif(values.get('SATAConnectors') == None or not values.get('SATAConnectors').isdigit() or values.get('SATAConnectors') < 0):
        return False
    elif(values.get('EffiencyRating') == None):
        return False
    elif(values.get('Modular') == None or values.get('Modular') not in ["Full", "Semi", "None"]):
        return False

    # Add The Listing First So The Listing ID Is Available
    listing = Listing(ListingName=detailList[3], ListingPrice=detailList[1],
                      ListingType=detailList[0], ListingDescription=detailList[2],
                      userId=current_user.id)
    db.session.add(listing)
    db.session.commit()
    id_ = listing.id

    powerSupply = PowerSupply(
        manufacturer=values.get('manufacturer'),
        EffiencyRating=values.get('EffiencyRating'),
        Wattage=values.get('Wattage'),
        Modular=values.get('Modular'),
        SATAConnectors=values.get('SATAConnectors'),
        PowerSupplyListing=id_)

    db.session.add(powerSupply)
    db.session.commit()


def isDecimal(number):
    try:
        float(number)
        return True
    except ValueError:
        return False
