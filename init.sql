--dbname protest
DROP TABLE IF EXISTS PriceList, Bids, CareTakerAvailability, RequireSpecialCare, SpecialCare, OwnedPets, Category;
DROP TABLE IF EXISTS  PCSAdmin, PetOwners, PartTime, FullTime, CareTakers, users;

CREATE TABLE users(
    username VARCHAR PRIMARY KEY,
    email VARCHAR NOT NULL,
    area VARCHAR NOT NULL,
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

CREATE TABLE FullTime (
    username VARCHAR PRIMARY KEY REFERENCES Users(username) ON DELETE CASCADE
);

CREATE TABLE PartTime (
    username VARCHAR PRIMARY KEY REFERENCES Users(username) ON DELETE CASCADE
);

-- TO INSERT INTO HERE WHENEVER THERE IS A NEW CATEGORY IN OWNED PETS
CREATE TABLE Category (
    pettype VARCHAR PRIMARY KEY
);

CREATE TABLE OwnedPets (
    owner_name VARCHAR references PetOwners(username) ON DELETE CASCADE,
    pet_name VARCHAR NOT NULL UNIQUE,
    category VARCHAR NOT NULL,
    age INTEGER NOT NULL,
    --gender VARCHAR NOT NULL,
    Primary Key(owner_name, pet_name)
);

CREATE TABLE SpecialCare(
    care VARCHAR PRIMARY KEY
);

CREATE TABLE RequireSpecialCare(
    owner_name VARCHAR,
    pet_name VARCHAR,
    care VARCHAR REFERENCES SpecialCare(care),
    FOREIGN KEY(owner_name, pet_name) REFERENCES OwnedPets(owner_name, pet_name),
    PRIMARY KEY(owner_name, pet_name, care)
);

CREATE TABLE CaretakerAvailability(
    date TIMESTAMP,
    pet_count INTEGER DEFAULT 0,
    leave BOOLEAN,
    caretaker_name VARCHAR REFERENCES CareTakers(username),
    PRIMARY KEY(caretaker_name, date)
);

CREATE TABLE Bids (
    owner_name VARCHAR,
    pet_name VARCHAR,
    FOREIGN KEY(owner_name, pet_name) REFERENCES OwnedPets(owner_name, pet_name),
    review VARCHAR,
    rating INTEGER, --to be updated after the bid
    mode_of_transport VARCHAR NOT NULL,
    bid_date_time TIMESTAMP NOT NULL,
    credit_card VARCHAR,
    successful BOOLEAN
    -- no need start date and end date like what tutor said, so maybe just update the CaretakerAvailability table whenever a bid is made.
    -- other attributes that might need: price (of bid),
);

CREATE TABLE PriceList (
    pettype VARCHAR REFERENCES Category(pettype),
    username VARCHAR REFERENCES CareTakers(username) ON DELETE CASCADE,
    price NUMERIC NOT NULL,
    PRIMARY KEY(pettype, username, price)
);

--INSERT INTO users (username, email, area, password) VALUES ('a', 'a', 'a', 'a');
--INSERT INTO PetOwners (username, email, area, password) VALUES ('b', 'b', 'a', 'a');

--INSERT INTO PetOwners (username) VALUES ('b');

--CREATE FUNCTIONS AND PROCEDURES
--PUT DESCRIPTION ABOVE TO FUNCTION ON WHAT IT IS FOR
--WILL NEED TO TRANSPORT THESE STUFF INTO SOME ROUTE IN views.py later on.


--CREATE TRIGGERS
