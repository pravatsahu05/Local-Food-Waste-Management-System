-- Providers Table

CREATE TABLE IF NOT EXISTS providers(
    Provider_ID INT PRIMARY KEY,
    Name VARCHAR(255),
    Type VARCHAR(100),
    Address TEXT,
    City VARCHAR(100),
    Contact VARCHAR(100)
);

-- Receivers Table

CREATE TABLE IF NOT EXISTS receivers(
    Receiver_ID INT PRIMARY KEY,
    Name VARCHAR(255),
    Type VARCHAR(100),
    City VARCHAR(100),
    Contact VARCHAR(100)
);

-- Food Listings Table

CREATE TABLE IF NOT EXISTS food_listings(
    Food_ID INT PRIMARY KEY,
    Food_Name VARCHAR(255),
    Quantity INT,
    Expiry_Date DATE,
    Provider_ID INT,
    Provider_Type VARCHAR(100),
    Location VARCHAR(100),
    Food_Type VARCHAR(100),
    Meal_Type VARCHAR(100),

    FOREIGN KEY (Provider_ID)
    REFERENCES providers(Provider_ID)
);

-- Claims Table

CREATE TABLE IF NOT EXISTS claims(
    Claim_ID INT PRIMARY KEY,
    Food_ID INT,
    Receiver_ID INT,
    Status VARCHAR(50),
    Timestamp DATETIME,

    FOREIGN KEY (Food_ID)
    REFERENCES food_listings(Food_ID),

    FOREIGN KEY (Receiver_ID)
    REFERENCES receivers(Receiver_ID)
);
