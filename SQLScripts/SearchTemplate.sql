
Select Items.id, count(Items.id) as itemCount
		From Items Left Join  Purchases On Purchases.itemId = Items.id
        Group By Items.id;
        
-- Select * from Items;
CREATE OR REPLACE View Popularity as
		Select Items.id as itemId, count(Items.id) as itemCount
		From Items Left Join  Purchases On Purchases.itemId = Items.id
		Group By Items.id;

-- drop view Popularity; 
Select * from Popularity;


Select itemId, itemName, brandName, price, count(itemId)
From  

	(
	(Select *
	From Items Left Join Popularity On Popularity.itemId = Items.id
	Where (SOUNDEX(Items.itemName) like SOUNDEX("screwdriver") or Items.itemName Like "%screwdriver%") and Items.itemName != "" and Popularity.itemId and Items.isCurrentlyAvailable
	order By Popularity.itemCount)
	Union
	(Select *
	From Items Left Join Popularity On Popularity.itemId = Items.id
	Where (SOUNDEX(Items.brandName) like SOUNDEX("screwdriver") or Items.brandName Like "%screwdriver%") and Items.itemName != "" and Popularity.itemId and Items.isCurrentlyAvailable
	order By Popularity.itemCount)
	Union
	(Select *
	From Items Left Join Popularity On Popularity.itemId = Items.id
	Where (SOUNDEX(Items.description) like SOUNDEX("screwdriver") or Items.description Like "%screwdriver%") and Items.itemName != "" and Popularity.itemId and Items.isCurrentlyAvailable
	order By Popularity.itemCount)
	Union
	(
	Select *
	From	(
		Select Items.id as id, retailerID, itemName, availabiltyStartDate, availabiltyEndDate, isCurrentlyAvailable, brandName, description, categoryId, price 
		from Metadata Left Join Items on Metadata.itemId = Items.id
		Where (SOUNDEX(Items.description) like SOUNDEX("screwdriver") or Items.description Like "%screwdriver%") and Items.isCurrentlyAvailable
		) as metadata  Left Join Popularity On Popularity.itemId = metadata.id

	) 
    
    )  as allReturned 
Group by itemId, itemName, brandName, price

