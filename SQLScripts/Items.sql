Drop Table Items;

Create Table Items(
	id INT PRIMARY KEY NOT NULL auto_increment, 
    retailerID INT, 
    itemName VARCHAR(255), 
    availabiltyStartDate TIMESTAMP, 
    availabiltyEndDate TIMESTAMP, 
    isCurrentlyAvailable Boolean, 
    brandName VARCHAR(255),
    description VARCHAR(255), 
    categoryId INT
)