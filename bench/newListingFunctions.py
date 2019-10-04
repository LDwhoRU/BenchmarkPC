from bench import app, db
from bench.models import User, Listing, Case, Memory, CPUCooler, Motherboard, CPU, GPU, PowerSupply
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

    listing = Listing(ListingName=detailList[3], ListingPrice=detailList[1],
                      ListingType=detailList[0], ListingDescription=detailList[2],
                      userId=current_user.id)
    db.session.add(listing)
    db.session.commit()
    listingID = listing.id

    case = Case(manufacturer=manufacturer, colour=Colour, sidePanel=SidePanel,
                internal25Bays=Bays25, internal35Bays=Bays35, caseListing=listingID)
    db.session.add(case)
    db.session.commit()


def processMemory(detailList, request):
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

    listing = Listing(ListingName=detailList[3], ListingPrice=detailList[1],
                      ListingType=detailList[0], ListingDescription=detailList[2],
                      userId=current_user.id)
    db.session.add(listing)
    db.session.commit()
    id_ = listing.id

    memory = Memory(manufacturer=manufacturer, colour=colour, memoryType=memoryType,
                    speed=memorySpeed, modules=modules, memoryListing=id_)
    db.session.add(memory)
    db.session.commit()


def processCPUCooler(detailList, request):
    print("COol")
    manufacturer = request.form.get('Manufacturer')
    RPM = request.form.get('Fan RPM')
    Noise = request.form.get('Fan Noise Level')
    Height = request.form.get('Cooler Height')
    Socket = request.form.get('Socket')
    WaterCooled = request.form.get('WaterCooled')
    Fanless = request.form.get('Fanless')
    if(manufacturer == ""):
            print("No Manufacturer")
            return False
    if(Height.isdigit() == False or Noise.isdigit() == False or RPM.isdigit() == False):
            return False
    Height = int(Height)
    Noise = int(Noise)
    RPM = int(RPM)

    listing = Listing(ListingName=detailList[3], ListingPrice=detailList[1],
                      ListingType=detailList[0], ListingDescription=detailList[2],
                      userId=current_user.id)
    db.session.add(listing)
    db.session.commit()
    id_ = listing.id

    Cooler = CPUCooler(manufacturer=manufacturer, FanRPM=RPM, NoiseLevel=Noise,
                       Height=Height, WaterCooled=WaterCooled, Fanless=Fanless, CPUCoolerListing=id_)
    db.session.add(Cooler)
    db.session.commit()


def processMotherBoard(detailList, request):

    print("Motherboard")
    manufacturer = request.form.get('Manufacturer')
    Socket = request.form.get('Socket')
    RamSlots = request.form.get('RAMSlots')
    MaxRam = request.form.get('RAMMax')
    colour = request.form.get('Colour')
    Chipset = request.form.get('Chipset')
    MemoryType = request.form.get('MemoryType')
    SLI = request.form.get('SLI')
    CrossFire = request.form.get('CrossFire')
    x16 = request.form.get('x16')
    x8 = request.form.get('x8')
    x4 = request.form.get('x4')
    x1 = request.form.get('x1')
    PCI = request.form.get('PCI')
    SATA = request.form.get('SATA')
    mSATA = request.form.get('mSATA')
    M2 = request.form.get('M.2')
    USB3 = request.form.get('USB3')
    WiFi = request.form.get('WiFi')
    RAID = request.form.get('RAID')
    IntegerDetailList = [RamSlots, MaxRam,
                         x16, x8, x4, x1, PCI, SATA, mSATA, M2]
    OtherDetailList = [MemoryType, SLI, CrossFire, USB3, WiFi, RAID]
    if(manufacturer == ""):
            return False

    #Set Default Values If Certain Fields Are Empty
    for i in range(len(IntegerDetailList)):
        if(IntegerDetailList[i] == "" or IntegerDetailList[i] == None):
            IntegerDetailList[i] = 0
        if(str(IntegerDetailList[i]).isdigit() == False):
            return False
        print(IntegerDetailList[i])
    for i in range(len(OtherDetailList)):
        if(OtherDetailList[i] == "Choose..."):
            OtherDetailList[i] = ""

    #Add The Listing First So The Listing ID Is Available
    listing = Listing(ListingName=detailList[3], ListingPrice=detailList[1],
                      ListingType=detailList[0], ListingDescription=detailList[2],
                      userId=current_user.id)
    db.session.add(listing)
    db.session.commit()
    id_ = listing.id

    #Create The Motherboard Object And Add It To The Database
    MotherBoard = Motherboard(manufacturer=manufacturer, Socket=Socket, RAMslots=IntegerDetailList[0],
                              MaxRAM=IntegerDetailList[1], colour=colour, Chipset=Chipset, MemoryType=OtherDetailList[0],
                              SLISupport=OtherDetailList[1], CrossFireSupport=OtherDetailList[2], PCIEx16Slots=IntegerDetailList[2],
                              PCIEx8Slots=IntegerDetailList[3], PCIEx4Slots=IntegerDetailList[
                                  4], PCIEx1Slots=IntegerDetailList[5],
                              PCISlots=IntegerDetailList[6], SATAPorts=IntegerDetailList[
                                  7], M2Slots=IntegerDetailList[9], mSata=IntegerDetailList[8],
                              OnboardUSB3Headers=OtherDetailList[3], OnboardWifi=OtherDetailList[4],
                              RAIDSupport=OtherDetailList[5], MotherboardListing=id_
                              )
    db.session.add(MotherBoard)
    db.session.commit()

    manufacturer = request.form.get('Manufacturer')


def processCPU(detailList, request):
        manufacturer = request.form.get('Manufacturer')
        TDP = request.form.get('TDP')
        CoreCount = request.form.get('Core Count')
        CoreClock = request.form.get('Core Clock')
        BoostClock = request.form.get('Boost Clock')
        Series = request.form.get('Series')
        Microarchitecture = request.form.get('Microarchitecture')
        Socket = request.form.get('Socket')
        IntegratedGraphics = request.form.get('IntegratedGraphics')
        IncludesCPUCooler = request.form.get('CPUCooler')
        print("Reached Checks")
        if(manufacturer == ""):
            print("Error: Manufacturer Check Failed")
            return False
        elif(CoreCount == None or CoreCount.isdigit() == False):
            print("Error: CoreCount Check Failed")
            return False
        elif(CoreClock == None or not isDecimal(CoreClock)):
            print("Error: Core Clock Check Failed")
            return False
        elif(BoostClock == None or not isDecimal(BoostClock)):
            print("Error: Boost Clock Check Failed")
            return False
        elif(TDP == None or not TDP.isdigit()):
            return False
        elif(IntegratedGraphics not in ["Yes", "No"]):
            print("Error: IntegratedGraphics Check Failed")
            return False
        elif(IncludesCPUCooler not in ["Yes", "No"]):
            print("Error: IncludesCPUCooler Check Failed")
            return False
        print("Passed Checks")
        #Add The Listing First So The Listing ID Is Available
        listing = Listing(ListingName=detailList[3], ListingPrice=detailList[1],
                          ListingType=detailList[0], ListingDescription=detailList[2],
                          userId=current_user.id)
        db.session.add(listing)
        db.session.commit()
        id_ = listing.id

        cpu = CPU(manufacturer=manufacturer, TDP=TDP, CoreCount=CoreClock,
                  CoreClock=CoreClock, BoostClock=BoostClock, Series=Series, Microarchitecture=Microarchitecture,
                  Socket=Socket, IntegratedGraphics=IntegratedGraphics, IncludesCPUCooler=IncludesCPUCooler,
                  CPUListing=id_)

        db.session.add(cpu)
        db.session.commit()


def processGPU(detailList, request):
        manufacturer = request.form.get('Manufacturer')
        Chipset = request.form.get('Chipset')
        MemoryType = request.form.get('MemoryType')
        CoreClock = request.form.get('CoreClock')
        BoostClock = request.form.get('BoostClock')
        colour = request.form.get('GPUColour')
        Length = request.form.get('Length')
        TDP = request.form.get('TDP')
        DVIPorts = request.form.get('DVI')
        HDMIPorts = request.form.get('HDMI')
        MiniHDMIPorts = request.form.get('Mini-HDMI')
        DisplayPortPorts = request.form.get('DisplayPort')
        MiniDisplayPortPorts = request.form.get('Mini-DisplayPort')
        CoolingType = request.form.get('CoolingType')

        if(manufacturer == ""):
            return False
        elif(not isDecimal(CoreClock) or CoreClock <= 0):
            print("Error: Core Clock Check Failed")
            print("Core Clock = " + str(CoreClock))
            return False
        elif(not isDecimal(BoostClock) or BoostClock <= 0):
            print("Error: Boost Clock Check Failed")
            return False
        elif(not isDecimal(Length) or Length <= 0):
            print("Error: Length Check Failed")
            return False
        elif(not TDP.isdigit() or TDP < 0):
            print("Error: TDP Check Failed")
            return False
        elif(not DVIPorts.isdigit() or DVIPorts < 0):
            print("Error: DVIPorts Check Failed")
            return False
        elif(not HDMIPorts.isdigit() or HDMIPorts < 0):
            print("Error: HDMIPorts Check Failed")
            return False
        elif(not MiniHDMIPorts.isdigit() or MiniHDMIPorts < 0):
            print("Error: MiniHDMIPorts Check Failed")
            return False
        elif(not DisplayPortPorts.isdigit() or DisplayPortPorts < 0):
            print("Error: DisplayPortPorts Check Failed")
            return False
        elif(not MiniDisplayPortPorts.isdigit() or MiniDisplayPortPorts < 0):
            print("Error: MiniDisplayPortPorts Check Failed")
            return False
        elif(CoolingType not in ["Blower", "Fan"]):
            print("Error: CoolingType Check Failed")
            return False

        #Add The Listing First So The Listing ID Is Available
        listing = Listing(ListingName=detailList[3], ListingPrice=detailList[1],
                          ListingType=detailList[0], ListingDescription=detailList[2],
                          userId=current_user.id)
        db.session.add(listing)
        db.session.commit()
        id_ = listing.id

        gpu = GPU(manufacturer=manufacturer, Chipset=Chipset, MemoryType=MemoryType,
                  CoreClock=CoreClock, BoostClock=BoostClock, colour=colour,
                  Length=Length, TDP=TDP, DVIPorts=DVIPorts, HDMIPorts=HDMIPorts,
                  MiniHDMIPorts=MiniHDMIPorts, DisplayPortPorts=DisplayPortPorts,
                  MiniDisplayPortPorts=MiniDisplayPortPorts, CoolingType=CoolingType,
                  GPUListing=id_)

        db.session.add(gpu)
        db.session.commit()
        print("Commit GPU")


def processPowerSupply(detailList, request):
        manufacturer = request.form.get('Manufacturer')
        EffiencyRating = request.form.get('Effiency Rating')
        Wattage = request.form.get('Wattage')
        Modular = request.form.get('Modular')
        SATAConnectors = request.form.get('SATA')

        if(manufacturer == ""):
            return False
        elif(Wattage == None or not Wattage.isdigit() or Wattage < 1):
            return False
        elif(SATAConnectors == None or not SATAConnectors.isdigit() or SATAConnectors < 0):
            return False
        elif(EffiencyRating == None):
            return False
        elif(Modular == None or Modular not in ["Full", "Semi", "None"]):
            return False

        #Add The Listing First So The Listing ID Is Available
        listing = Listing(ListingName=detailList[3], ListingPrice=detailList[1],
                          ListingType=detailList[0], ListingDescription=detailList[2],
                          userId=current_user.id)
        db.session.add(listing)
        db.session.commit()
        id_ = listing.id

        powerSupply = PowerSupply(manufacturer=manufacturer,EffiencyRating=EffiencyRating,
        Wattage=Wattage, Modular=Modular, SATAConnectors=SATAConnectors,PowerSupplyListing=id_)
        db.session.add(powerSupply)
        db.session.commit()

def isDecimal(number):
    try:
        float(number)
        return True
    except ValueError:
        return False
