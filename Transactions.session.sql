/*CREATE TABLE IF NOT EXISTS categories(
    category_id serial PRIMARY KEY,
    category_name varchar(50)
);*/



/*INSERT INTO categories (category_name)
SELECT DISTINCT table_name
FROM information_schema.tables
WHERE table_schema = 'public';
*/
--SELECT * FROM categories;

--ALTER TABLE information_schema.tables RENAME COLUMN category TO category_id;

/*REATE TABLE Users (
    UserID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Phone VARCHAR(20),
    CreatedAt TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);*/

/*CREATE TABLE Accounts (
    AccountID SERIAL PRIMARY KEY,
    UserID INT NOT NULL,
    AccountType VARCHAR(50) NOT NULL,
    AccountNumber VARCHAR(20) UNIQUE NOT NULL,
    Balance DECIMAL(15, 2) DEFAULT 0,
    CreatedAt TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);*/
--DROP TABLE categories;

/*CREATE TABLE Categories (
    CategoryID SERIAL PRIMARY KEY,
    CategoryName VARCHAR(100) NOT NULL
);*/

/*CREATE TABLE Transactions (
    TransactionID SERIAL PRIMARY KEY,
    AccountID INT NOT NULL,
    CategoryID INT,
    Date DATE NOT NULL,
    Description VARCHAR(255),
    Amount DECIMAL(15, 2) NOT NULL,
    CreatedAt TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (AccountID) REFERENCES Accounts(AccountID),
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
);*/

/*CREATE TABLE Balances (
    BalanceID SERIAL PRIMARY KEY,
    AccountID INT NOT NULL,
    Balance DECIMAL(15, 2) NOT NULL,
    Date DATE NOT NULL,
    FOREIGN KEY (AccountID) REFERENCES Accounts(AccountID)
);*/


/*CREATE INDEX idx_userid ON Accounts(UserID);
CREATE INDEX idx_accountid ON Transactions(AccountID);
CREATE INDEX idx_categoryid ON Transactions(CategoryID);
CREATE INDEX idx_date ON Transactions(Date); */

/*INSERT INTO Users (Name, Email, Phone) VALUES
('Lefteris Gilmaz', 'lefterisyilmaz96@gmail.com, '07777771111');*/