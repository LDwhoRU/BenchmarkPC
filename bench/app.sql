BEGIN TRANSACTION;
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
INSERT INTO alembic_version VALUES('6ac36df74dc9');
CREATE TABLE "user" (
	id SERIAL NOT NULL, 
	username VARCHAR(80) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	phone VARCHAR(120) NOT NULL, 
	password_hash VARCHAR(128), 
	PRIMARY KEY (id), 
	UNIQUE (email), 
	UNIQUE (phone), 
	UNIQUE (username)
);
CREATE TABLE listing (
	id SERIAL NOT NULL, 
	"ListingScore" INTEGER, 
	"ListingState" VARCHAR(80) DEFAULT 'Open', 
	"ListingName" VARCHAR(80) NOT NULL, 
	"ListingPrice" NUMERIC NOT NULL, 
	"ListingType" VARCHAR(80) NOT NULL, 
	"ListingDescription" VARCHAR(80) NOT NULL, 
	"ListingTimeStamp" TIMESTAMP NOT NULL, 
	"userId" INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY("userId") REFERENCES "user" (id)
);
CREATE TABLE IF NOT EXISTS "CPU" (
	id SERIAL NOT NULL, 
	manufacturer VARCHAR(80) NOT NULL, 
	"TDP" NUMERIC, 
	"CoreCount" NUMERIC, 
	"CoreClock" NUMERIC, 
	"BoostClock" NUMERIC, 
	"Series" VARCHAR(80), 
	"Microarchitecture" VARCHAR(80), 
	"Socket" VARCHAR(80), 
	"IntegratedGraphics" VARCHAR(80), 
	"IncludesCPUCooler" VARCHAR(80), 
	"CPUListing" INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY("CPUListing") REFERENCES listing (id)
);
CREATE TABLE IF NOT EXISTS "GPU" (
	id SERIAL NOT NULL, 
	manufacturer VARCHAR(80) NOT NULL, 
	"Chipset" VARCHAR(80), 
	"MemoryType" VARCHAR(80), 
	"CoreClock" NUMERIC, 
	"BoostClock" NUMERIC, 
	colour VARCHAR(80), 
	"Length" INTEGER, 
	"TDP" NUMERIC, 
	"DVIPorts" INTEGER, 
	"HDMIPorts" INTEGER, 
	"MiniHDMIPorts" INTEGER, 
	"DisplayPortPorts" INTEGER, 
	"MiniDisplayPortPorts" INTEGER, 
	"CoolingType" VARCHAR(80), 
	"GPUListing" INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY("GPUListing") REFERENCES listing (id)
);
CREATE TABLE bids (
	id SERIAL NOT NULL, 
	"bidAmount" VARCHAR(80) NOT NULL, 
	"bidUser" INTEGER, 
	"bidListing" INTEGER, 
	"bidTimeStamp" TIMESTAMP, 
	PRIMARY KEY (id), 
	FOREIGN KEY("bidListing") REFERENCES listing (id), 
	FOREIGN KEY("bidUser") REFERENCES "user" (id)
);
CREATE TABLE IF NOT EXISTS "case" (
	id SERIAL NOT NULL, 
	manufacturer VARCHAR(80) NOT NULL, 
	colour VARCHAR(80), 
	"sidePanel" VARCHAR(80), 
	"internal25Bays" INTEGER, 
	"internal35Bays" INTEGER, 
	"caseListing" INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY("caseListing") REFERENCES listing (id)
);
CREATE TABLE cpu_cooler (
	id SERIAL NOT NULL, 
	manufacturer VARCHAR(80) NOT NULL, 
	"FanRPM" VARCHAR(80), 
	"NoiseLevel" VARCHAR(80), 
	"Height" INTEGER, 
	"WaterCooled" VARCHAR(80), 
	"Socket" VARCHAR(80), 
	"Fanless" VARCHAR(80), 
	"CPUCoolerListing" INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY("CPUCoolerListing") REFERENCES listing (id)
);
CREATE TABLE images (
	id SERIAL NOT NULL, 
	"ImageName" VARCHAR(80) NOT NULL, 
	"ImageListing" INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY("ImageListing") REFERENCES listing (id)
);
CREATE TABLE memory (
	id SERIAL NOT NULL, 
	manufacturer VARCHAR(80) NOT NULL, 
	"memoryType" VARCHAR(80), 
	modules INTEGER, 
	colour VARCHAR(80), 
	speed INTEGER, 
	"memoryListing" INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY("memoryListing") REFERENCES listing (id)
);
CREATE TABLE motherboard (
	id SERIAL NOT NULL, 
	manufacturer VARCHAR(80) NOT NULL, 
	"Socket" VARCHAR(80), 
	"RAMslots" INTEGER NOT NULL, 
	"MaxRAM" INTEGER NOT NULL, 
	colour VARCHAR(80), 
	"Chipset" VARCHAR(80), 
	"MemoryType" VARCHAR(80), 
	"SLISupport" VARCHAR(80), 
	"CrossFireSupport" VARCHAR(80), 
	"PCIEx16Slots" INTEGER NOT NULL, 
	"PCIEx8Slots" INTEGER NOT NULL, 
	"PCIEx4Slots" INTEGER NOT NULL, 
	"PCIEx1Slots" INTEGER NOT NULL, 
	"PCISlots" INTEGER NOT NULL, 
	"SATAPorts" INTEGER NOT NULL, 
	"M2Slots" INTEGER NOT NULL, 
	"mSata" INTEGER NOT NULL, 
	"OnboardUSB3Headers" VARCHAR(80), 
	"OnboardWifi" VARCHAR(80), 
	"RAIDSupport" VARCHAR(80), 
	"MotherboardListing" INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY("MotherboardListing") REFERENCES listing (id)
);
CREATE TABLE power_supply (
	id SERIAL NOT NULL, 
	manufacturer VARCHAR(80) NOT NULL, 
	"EffiencyRating" VARCHAR(80), 
	"Wattage" INTEGER, 
	"Modular" VARCHAR(20), 
	"SATAConnectors" INTEGER, 
	"PowerSupplyListing" INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY("PowerSupplyListing") REFERENCES listing (id)
);
CREATE TABLE sales (
	id SERIAL NOT NULL, 
	"ListingID" INTEGER, 
	"BuyerID" INTEGER, 
	"SalePrice" NUMERIC NOT NULL, 
	"SaleTimeStamp" TIMESTAMP NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY("BuyerID") REFERENCES "user" (id), 
	FOREIGN KEY("ListingID") REFERENCES listing (id)
);
COMMIT;
