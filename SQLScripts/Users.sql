Create Table Users(
	id int Primary Key NOT NULL auto_increment,
	firstName VARCHAR(255), 
    lastName VARCHAR(255), 
    email VARCHAR(255), 
    phoneNumber VARCHAR(255), 
    zipCode VARCHAR(255),
    isAcrive BOOL default True
); 