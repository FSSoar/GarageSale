Select * from Purchases; 


Select itemId, sum(purchasePrice) 
from Purchases Left Join Items on Items.id = Purchases.itemId
Group By itemId; 
