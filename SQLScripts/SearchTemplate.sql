
CREATE OR REPLACE View Popularity as
		Select itemId, count(itemId) as itemCount
		From Purchases Left Join  Items On Purchases.itemId = Items.id
		Where Items.retailerID = 1 and Items.itemName is Not NULL and Items.itemName != "" and Items.id is Not NULL
		Group By itemId;

(Select *, "ItemName"
From Items Left Join Popularity On Popularity.itemId = Items.id
Where (SOUNDEX(Items.itemName) like SOUNDEX("manshu") or Items.itemName Like "%manshu%") and Items.itemName != "" and Popularity.itemId 
order By Popularity.itemCount)
Union
(Select *, "Brand"
From Items Left Join Popularity On Popularity.itemId = Items.id
Where (SOUNDEX(Items.brandName) like SOUNDEX("dyson") or Items.brandName Like "%dyson%") and Items.itemName != "" and Popularity.itemId 
order By Popularity.itemCount)


