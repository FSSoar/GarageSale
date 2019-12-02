
CREATE OR REPLACE View Popularity as
		Select itemId, count(itemId) as itemCount
		From Purchases Left Join  Items On Purchases.itemId = Items.id
		Where Items.retailerID = 1 and Items.itemName is Not NULL and Items.itemName != "" and Items.id is Not NULL
		Group By itemId;

Select itemId, itemName, brandName, price, count(itemId)
From  

	(
	(Select *
	From Items Left Join Popularity On Popularity.itemId = Items.id
	Where (SOUNDEX(Items.itemName) like SOUNDEX("manshu") or Items.itemName Like "%manshu%") and Items.itemName != "" and Popularity.itemId 
	order By Popularity.itemCount)
	Union
	(Select *
	From Items Left Join Popularity On Popularity.itemId = Items.id
	Where (SOUNDEX(Items.brandName) like SOUNDEX("dyson") or Items.brandName Like "%dyson%") and Items.itemName != "" and Popularity.itemId 
	order By Popularity.itemCount)
	Union
	(Select *
	From Items Left Join Popularity On Popularity.itemId = Items.id
	Where (SOUNDEX(Items.description) like SOUNDEX("cleaner") or Items.description Like "%cleaner%") and Items.itemName != "" and Popularity.itemId 
	order By Popularity.itemCount)
	Union
	(
	Select *
	From	(
		Select Items.id as id, retailerID, itemName, availabiltyStartDate, availabiltyEndDate, isCurrentlyAvailable, brandName, description, categoryId, price 
		from Metadata Left Join Items on Metadata.itemId = Items.id
		Where (SOUNDEX(Items.description) like SOUNDEX("dyson") or Items.description Like "%dyso%")
		) as metadata  Left Join Popularity On Popularity.itemId = metadata.id

	) 
    
    )  as allReturned 
Group by itemId, itemName, brandName, price

