SELECT COUNT(Start, End, Seller_ID, Item_ID)
FROM Auction
WHERE Category LIKE '%,%,%,%,';