SELECT COUNT(DISTINCT User_ID)
FROM (SELECT User_ID
        FROM Seller
    UNION
    SELECT User_ID
        FROM Bidder);