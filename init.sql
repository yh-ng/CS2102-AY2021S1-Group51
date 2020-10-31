--dbname protest
DROP TABLE IF EXISTS CareTakerSalary, dummy, FullTimePriceList, PartTimePriceList, DefaultPriceList, Bids, CareTakerAvailability, RequireSpecialCare, SpecialCare, OwnedPets, Category;
DROP TABLE IF EXISTS PreferredModeOfPayment, ModeOfPayment, PreferredTransport, ModeOfTransport, PCSAdmin, PetOwners, PartTime, FullTime, CareTakers, users;

CREATE TABLE users(
    username VARCHAR PRIMARY KEY,
    email VARCHAR NOT NULL,
    area VARCHAR NOT NULL,
    gender VARCHAR NOT NULL,
    password VARCHAR NOT NULL
);

CREATE TABLE PCSAdmin (
    username VARCHAR PRIMARY KEY REFERENCES users(username) ON DELETE CASCADE
);

CREATE TABLE PetOwners (
    username VARCHAR PRIMARY KEY REFERENCES users(username) ON DELETE CASCADE
);

CREATE TABLE CareTakers (
    username VARCHAR PRIMARY KEY REFERENCES users(username) ON DELETE CASCADE,
    rating INTEGER DEFAULT 0
);

CREATE TABLE ModeOfTransport (
    transport VARCHAR PRIMARY KEY
);

INSERT INTO ModeOfTransport VALUES ('Pet Owner Deliver');
INSERT INTO ModeOfTransport VALUES ('Care Taker Pick Up');
INSERT INTO ModeOfTransport VALUES ('Transfer through PCS Building');

CREATE TABLE PreferredTransport (
    username VARCHAR REFERENCES CareTakers(username) ON DELETE CASCADE,
    transport VARCHAR REFERENCES ModeOfTransport(transport),
    PRIMARY KEY (username, transport)
);

CREATE TABLE ModeOfPayment (
  modeOfPayment VARCHAR PRIMARY KEY
);

INSERT INTO ModeOfPayment VALUES ('Credit Card');
INSERT INTO ModeOfPayment VALUES ('Cash');
INSERT INTO ModeOfPayment VALUES ('Either');


CREATE TABLE PreferredModeOfPayment (
  username VARCHAR REFERENCES CareTakers(username) ON DELETE CASCADE,
  modeOfPayment VARCHAR REFERENCES ModeOfPayment(modeOfPayment),
  PRIMARY KEY (username, modeOfPayment)
);

CREATE TABLE FullTime (
    username VARCHAR PRIMARY KEY REFERENCES CareTakers(username) ON DELETE CASCADE
);

CREATE TABLE PartTime (
    username VARCHAR PRIMARY KEY REFERENCES CareTakers(username) ON DELETE CASCADE
);

--INSERT INTO users VALUES ('abc', 'abc@abc.com', 'North', 'Male', 'abc');
--INSERT INTO PetOwners VALUES ('abc');
--INSERT INTO CareTakers VALUES ('abc');
--INSERT INTO FullTime VALUES ('abc');

-- TO INSERT INTO HERE WHENEVER THERE IS A NEW CATEGORY IN OWNED PETS
CREATE TABLE Category (
    pettype VARCHAR PRIMARY KEY
);

INSERT INTO Category VALUES ('Dog');
INSERT INTO Category VALUES ('Cat');
INSERT INTO Category VALUES ('Rabbit');
INSERT INTO Category VALUES ('Hamster');
INSERT INTO Category VALUES ('Guinea Pig');
INSERT INTO Category VALUES ('Fish');
INSERT INTO Category VALUES ('Mice');
INSERT INTO Category VALUES ('Terrapin');
INSERT INTO Category VALUES ('Bird');

CREATE TABLE OwnedPets (
    owner VARCHAR references PetOwners(username) ON DELETE CASCADE,
    pet_name VARCHAR NOT NULL UNIQUE,
    category VARCHAR NOT NULL,
    age INTEGER NOT NULL,
    --gender VARCHAR NOT NULL,
    Primary Key(owner, pet_name)
);

CREATE TABLE SpecialCare(
    care VARCHAR PRIMARY KEY
);

CREATE TABLE RequireSpecialCare(
    owner VARCHAR,
    pet_name VARCHAR,
    care VARCHAR REFERENCES SpecialCare(care),
    FOREIGN KEY(owner, pet_name) REFERENCES OwnedPets(owner, pet_name) ON DELETE CASCADE,
    PRIMARY KEY(owner, pet_name, care)
);

CREATE TABLE CaretakerAvailability(
    date DATE,
    pet_count INTEGER DEFAULT 0,
    leave BOOLEAN DEFAULT False,
    username VARCHAR REFERENCES CareTakers(username) ON DELETE CASCADE,
    available BOOLEAN NOT NULL DEFAULT True,
    PRIMARY KEY(username, date)
);

-- is bid_date)time actually necessary? dosent seem liek so (not necessary)
--if you want we can rename owner with POusername also like what i've done with caretaker so both are same format)
CREATE TABLE Bids (
    CTusername VARCHAR,
    owner VARCHAR,
    pet_name VARCHAR,
    FOREIGN KEY(owner, pet_name) REFERENCES OwnedPets(owner, pet_name),
    review VARCHAR DEFAULT NULL,
    rating INTEGER DEFAULT NULL, --to be updated after the bid
    mode_of_transport VARCHAR NOT NULL,
    mode_of_payment VARCHAR NOT NULL,
    credit_card VARCHAR,
    completed BOOLEAN DEFAULT FALSE,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    FOREIGN KEY (CTusername, start_date) REFERENCES CareTakerAvailability(username, date),
    FOREIGN KEY (CTusername, end_date) REFERENCES CaretakerAvailability(username, date)
    -- no need start date and end date like what tutor said, so maybe just update the CaretakerAvailability table whenever a bid is made.
    -- other attributes that might need: price (of bid),
);

CREATE TABLE PartTimePriceList (
  pettype VARCHAR REFERENCES Category(pettype),
  username VARCHAR REFERENCES CareTakers(username) ON DELETE CASCADE,
  price NUMERIC,
  PRIMARY KEY (pettype, username, price)
);

CREATE TABLE DefaultPriceList (
  pettype VARCHAR REFERENCES Category(pettype),
  price NUMERIC,
  PRIMARY KEY (pettype, price)
);

INSERT INTO DefaultPriceList VALUES ('Dog', 100);
INSERT INTO DefaultPriceList VALUES ('Cat', 80);
INSERT INTO DefaultPriceList VALUES ('Rabbit', 110);
INSERT INTO DefaultPriceList VALUES ('Hamster', 70);
INSERT INTO DefaultPriceList VALUES ('Guinea Pig', 150);
INSERT INTO DefaultPriceList VALUES ('Fish', 50);
INSERT INTO DefaultPriceList VALUES ('Mice', 50);
INSERT INTO DefaultPriceList VALUES ('Terrapin', 80);
INSERT INTO DefaultPriceList VALUES ('Bird', 80);


CREATE TABLE FullTimePriceList(
  username VARCHAR REFERENCES CareTakers(username) ON DELETE CASCADE,
  price NUMERIC,
  pettype VARCHAR,
  FOREIGN KEY (pettype, price) REFERENCES DefaultPriceList(pettype, price),
  PRIMARY KEY (pettype, username, price)
);

CREATE TABLE dummy(
  date DATE
);

-- THIS TABLE WILL BE USEFUL TO GET SOME OF THE SUMMARY INFORMATION AT POINT 4 OF THE PROJECT REQUIREMENTS.
CREATE TABLE CareTakerSalary (
  year INTEGER,
  month INTEGER,
  username VARCHAR REFERENCES CareTakers(username),
  petdays INTEGER NOT NULL DEFAULT 0,
  earnings NUMERIC NOT NULL DEFAULT 0,
  final_salary NUMERIC NOT NULL DEFAULT 0,
  PRIMARY KEY (year, month, username)
);


--TABLES NEEDED FOR THE SUMMARY OF SALARY OF CARETAKER
--FOR FULL TIME - FINAL SALARY IS $3000 for any total pet days <= 60
--              - IF pet days > 60, receive 80% of them as bonus
--              - so i guess, for example, total earnings he got $5000, and
--                his total pet days is 75, he will get $3000 + (5000 - 3000) * 80%?
--FOR PART TIME - FINAL SALARY IN A MONTH IS 75% OF TOTAL EARNINGS. (25% TO PCS)
--####################################################################
--YEAR # MONTH # USERNAME # PETDAYS # TOTAL EARNINGS # FINAL SALARY #
--####################################################################
