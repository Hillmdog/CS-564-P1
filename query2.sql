SELECT COUNT(DISTINCT User_ID)
FROM (SELECT User_ID, Location
        FROM Seller
    UNION
    SELECT User_ID, Location
        FROM Bidder)
WHERE Location = 'New York';