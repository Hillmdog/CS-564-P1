drop table if exists Item;
drop table if exists Seller;
drop table if exists Bidder;
drop table if exists Auction;
drop table if exists Bid;

create table Item(
    Name TEXT,
    Category TEXT, 
    Description TEXT,
    Item_ID INTEGER,
    PRIMARY KEY (Item_ID, Category)
);

create table Seller(
    User_ID TEXT PRIMARY KEY,
    Rating INTEGER,
    Location TEXT,
    Country TEXT
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
    Category TEXT,
    FOREIGN KEY (Seller_ID)
        REFERENCES Seller(User_ID),
    FOREIGN KEY (Item_ID)
        REFERENCES Item(Item_ID),
    FOREIGN KEY (Category)
        REFERENCES Item(Category),
    PRIMARY KEY (Start, End, Seller_ID, Item_ID, Category)
);

create table Bid(
    Time DATE,
    Amount REAL,
    Item_ID INTEGER,
    Bidder_ID TEXT,
    Category TEXT,
    FOREIGN KEY (Item_ID)
        REFERENCES Item(Item_ID),
    FOREIGN KEY (Bidder_ID)
        REFERENCES Bidder(User_ID),
    FOREIGN KEY (Category)
        REFERENCES Item(Category)
    PRIMARY KEY (Time, Amount, Item_ID, Bidder_ID, Category)
);