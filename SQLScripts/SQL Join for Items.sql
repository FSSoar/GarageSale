Select * 
From (SELECT retailerId, itemName, brandName, description, Items.id as itemId, firstname, lastName, email, phoneNumber, zipCode
		from Items  Left Join Users on Items.retailerId = Users.id
		where retailerID = 1 and ItemName != "") as retailerItems
        Left Join 
		(Select itemId, count(itemId) as itemCount
		From Purchases Left Join Items On Purchases.itemId = Items.id
		Where Items.retailerID = 1 
		Group By itemId) as itemCount On itemCount.itemId = retailerItems.itemId
Where itemCount.itemCount IS NOT NULL