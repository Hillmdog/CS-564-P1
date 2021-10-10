SELECT Item_ID
FROM Auction
WHERE Currently = (SELECT MAX(Currently)
                    FROM Auction);