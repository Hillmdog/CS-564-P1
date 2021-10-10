SELECT COUNT(Category)
FROM Auction
    LEFT JOIN Item On Auction.Item_ID = Item.Item_ID
WHERE Category LIKE '.%, %, %, %.';