SELECT COUNT(*)
FROM (SELECT Item_ID
    FROM Auction
    GROUP BY Item_ID
    Having COUNT(Category) = 4);