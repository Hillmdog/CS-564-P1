drop table if exists Item;
drop table if exists Seller;
drop table if exists Bidder;
drop table if exists Auction;
drop table if exists Bid;

create table Item(
    Name TEXT,
    Category TEXT, 
    Description TEXT,
    Item_ID INTEGER PRIMARY KEY
);

create table Seller(
    User_ID TEXT PRIMARY KEY,
    Rating INTEGER,
    Location TEXT NOT NULL,
    Country TEXT NOT NULL
);

create table Bidder(
    Country TEXT,
    User_ID TEXT PRIMARY KEY,
    Rating INTEGER,
    Location TEXT
);

create table Auction(
    Start DATE,
    End DATE,
    First_Bid REAL, 
    Currently REAL,
    Number_of_Bids INTEGER,
    Buy_Price REAL,
    Seller_ID TEXT,
    Item_ID INTEGER,
    FOREIGN KEY (Seller_ID)
        REFERENCES Seller(User_ID),
    FOREIGN KEY (Item_ID)
        REFERENCES Item(Item_ID),
    PRIMARY KEY (Start, End, Seller_ID, Item_ID)
);

create table Bid(
    Time DATE,
    Amount REAL,
    Bidder_ID TEXT,
    Item_ID INTEGER,
    FOREIGN KEY (Item_ID)
        REFERENCES Item(Item_ID),
    FOREIGN KEY (Bidder_ID)
        REFERENCES Bidder(User_ID),
    PRIMARY KEY (Time, Amount, Item_ID, Bidder_ID)
);