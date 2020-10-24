--dbname protest
DROP TABLE IF EXISTS FullTimePriceList, PartTimePriceList, DefaultPriceList, Bids, CareTakerAvailability, RequireSpecialCare, SpecialCare, OwnedPets, Category;
DROP TABLE IF EXISTS PreferredTransport, ModeOfTransport, PCSAdmin, PetOwners, PartTime, FullTime, CareTakers, users;

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
    FOREIGN KEY(owner, pet_name) REFERENCES OwnedPets(owner, pet_name),
    PRIMARY KEY(owner, pet_name, care)
);

CREATE TABLE CaretakerAvailability(
    date TIMESTAMP,
    pet_count INTEGER DEFAULT 0,
    leave BOOLEAN,
    caretaker VARCHAR REFERENCES CareTakers(username),
    available BOOLEAN NOT NULL DEFAULT true,
    PRIMARY KEY(caretaker, date)
);

CREATE TABLE Bids (
    caretaker VARCHAR,
    owner VARCHAR,
    pet_name VARCHAR,
    FOREIGN KEY(owner, pet_name) REFERENCES OwnedPets(owner, pet_name),
    review VARCHAR,
    rating INTEGER, --to be updated after the bid
    mode_of_transport VARCHAR NOT NULL,
    bid_date_time TIMESTAMP NOT NULL,
    credit_card VARCHAR,
    completed BOOLEAN DEFAULT FALSE,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    FOREIGN KEY (caretaker, start_date) REFERENCES CareTakerAvailability(caretaker, date),
    FOREIGN KEY (caretaker, end_date) REFERENCES CaretakerAvailability(caretaker, date)
    -- no need start date and end date like what tutor said, so maybe just update the CaretakerAvailability table whenever a bid is made.
    -- other attributes that might need: price (of bid),
);

CREATE TABLE PartTimePriceList (
  pettype VARCHAR REFERENCES Category(pettype),
  caretaker VARCHAR REFERENCES CareTakers(username) ON DELETE CASCADE,
  price NUMERIC,
  PRIMARY KEY (pettype, caretaker, price)
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
INSERT INTO DefaultPriceList VALUES ('Fish', 50);
INSERT INTO DefaultPriceList VALUES ('Mice', 50);
INSERT INTO DefaultPriceList VALUES ('Terrapin', 80);
INSERT INTO DefaultPriceList VALUES ('Bird', 80);


CREATE TABLE FullTimePriceList(
  caretaker VARCHAR REFERENCES CareTakers(username) ON DELETE CASCADE,
  price NUMERIC,
  pettype VARCHAR,
  FOREIGN KEY (pettype, price) REFERENCES DefaultPriceList(pettype, price),
  PRIMARY KEY (pettype, caretaker, price)
);
/*
-- should the pricelist username just reference to the caretakers rather than part time and full time seperately?
-- we could just check if he is a part time or full time. If full time, we will give option to choose price and then isnert into this TABLE
-- if full time, we will just insert the default price (from somewhere) based on the pettype.
CREATE TABLE PriceList (
    pettype VARCHAR REFERENCES Category(pettype),
    username VARCHAR REFERENCES CareTakers(username) ON DELETE CASCADE,
    price NUMERIC NOT NULL,
    PRIMARY KEY(pettype, username, price)
);
*/
--INSERT INTO users (username, email, area, password) VALUES ('a', 'a', 'a', 'a');
--INSERT INTO PetOwners (username, email, area, password) VALUES ('b', 'b', 'a', 'a');

--INSERT INTO PetOwners (username) VALUES ('b');

--CREATE FUNCTIONS AND PROCEDURES
--PUT DESCRIPTION ABOVE TO FUNCTION ON WHAT IT IS FOR
--WILL NEED TO TRANSPORT THESE STUFF INTO SOME ROUTE IN views.py later on.


--CREATE TRIGGERS
