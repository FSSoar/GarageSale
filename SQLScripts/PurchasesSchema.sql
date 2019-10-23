Drop Table Purchases; 

Create Table Purchases(
	id INT PRIMARY KEY NOT NULL auto_increment, 
    itemId Int, 
    userId INT,
    purchasePrice REAL, 
    purchase_date DATETIME default now()
)