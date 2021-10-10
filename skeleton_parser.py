
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

sellerFile = None
auctionFile = None
itemFile = None
bidFile = None
bidderFile = None
    
"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

def openFiles():
    global sellerFile, auctionFile, itemFile, bidFile, bidderFile
    sellerFile = open('seller.dot', 'w')
    auctionFile = open('auction.dot', 'w')
    itemFile = open('item.dot', 'w')
    bidFile = open('bid.dot', 'w')
    bidderFile = open('Bidder.dot', 'w')
    
def closeFiles():
    global sellerFile, auctionFile, itemFile, bidFile, bidderFile
    sellerFile.close()
    auctionFile.close()
    itemFile.close()
    bidFile.close()
    bidderFile.close()
    
def escapeStrings(string):
    new_string = ''
    for char in string:
        if char == '"':
            char = char + '"'
        new_string = new_string + char
    
    string = '"' + new_string + '"'
    
    return string
"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    print("parse json")
    
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        
        for i,item in enumerate(items):
            item_attributes = []
            item_attr_bids = []
            buy_price_flag = 0
            #print(i)
            for key in item:
            # nail the only optional attribute 
                if 'Buy_Price' in item:
                    buy_price_flag = 1
                else:
                    buy_price_flag = 0
                # first up let's snag all these attributes
                #start with the embedded ones
                if key == 'Bids':
                    # if bids is 'None'
                    if item['Bids']is not None:
                       for i,index in enumerate(item['Bids']):
                           individualBidder = {}
                           for attr in list(index.values()):
                               bEmbededAtr = attr['Bidder']
                               for bidder in bEmbededAtr:
                                   #get this junk
                                   individualBidder[bidder] = bEmbededAtr[bidder]
                               
                               if 'Country' not in bEmbededAtr.keys():
                                   individualBidder['Country'] = 'None'
                               if 'Location' not in bEmbededAtr.keys():
                                   individualBidder['Location'] = 'None'
                                   
                               
                               individualBidder['Time'] = attr['Time']
                               individualBidder['Amount'] = attr['Amount']
                           item_attr_bids.append(individualBidder)
                    else:
                        item_attr_bids.append({'None' : 'None'})

                #next embedded one
                elif key == 'Seller':
                    seller = item['Seller']
                    
                    item_attributes.append(('Seller UserID', seller['UserID'] ))
                    item_attributes.append(('Seller Rating', seller['Rating']))
    
                else:
                    #rest of them attributes man
                    item_attributes.append((key, item[key]))
                if buy_price_flag == 0:
                    item_attributes.append(('Buy_Price', 'None'))
                    
            # add them to their respective files and repeat
            item_attributes = dict(item_attributes)
       
        
            Seller_User_ID = escapeStrings(item_attributes['Seller UserID'])
            Seller_Rating = item_attributes['Seller Rating']
            Location = escapeStrings(item_attributes['Location'])
            Country = escapeStrings(item_attributes['Country'])
            Start = escapeStrings(transformDttm(item_attributes['Started']))
            End = escapeStrings(transformDttm(item_attributes['Ends']))
            First_bid = escapeStrings(transformDollar(item_attributes['First_Bid']))
            Currently = escapeStrings(transformDollar(item_attributes['Currently']))
            Number_of_Bids = item_attributes['Number_of_Bids']
            
            Buy_Price = item_attributes['Buy_Price']
            if Buy_Price != 'None':
                Buy_Price = escapeStrings(transformDollar(Buy_Price))
            else:
                Buy_Price = escapeStrings(Buy_Price)                
            
            Item_ID = item_attributes['ItemID']
            Name = escapeStrings(item_attributes['Name'])
                
           
            if item_attributes['Description'] is not None:
                Description = escapeStrings(item_attributes['Description'])
            else:
                Description = '"None"'
                
            Bidder_UserID = None
            Bidder_Rating = None
            Bidder_Location = None
            Bidder_Country = None
            Bidder_Time = None
            Bidder_Amount = None
                
            for cats in item_attributes['Category']:
                Category = escapeStrings(cats)
            #item  
                item_row = Name + columnSeparator + Category + columnSeparator + Description + columnSeparator + Item_ID + '\n'
                itemFile.write(item_row)
            #auction  
                Auction_row = Start + columnSeparator + End + columnSeparator + First_bid + columnSeparator + Currently + columnSeparator + Number_of_Bids + columnSeparator + Buy_Price + columnSeparator + Seller_User_ID + columnSeparator + Item_ID + columnSeparator + Category + '\n'
                auctionFile.write(Auction_row)
                for bids in item_attr_bids:
                    if 'None' not in bids:
                        Bidder_UserID = escapeStrings(bids['UserID'])
                        Bidder_Rating = bids['Rating'] 
                        Bidder_Location = escapeStrings(bids['Location'])
                        Bidder_Country = escapeStrings(bids['Country'])
                        Bidder_Time = escapeStrings(transformDttm(bids['Time']))
                        Bidder_Amount = escapeStrings(transformDollar(bids['Amount']))
                   
                    #bid
                        bid_row = Bidder_Time + columnSeparator + Bidder_Amount + columnSeparator + Item_ID + columnSeparator + Bidder_UserID + '\n'
                        bidFile.write(bid_row)
                    #bidder
                        bidder_row = Bidder_Country + columnSeparator + Bidder_UserID +  columnSeparator + Bidder_Rating + columnSeparator + Bidder_Location + '\n' 
                        bidderFile.write(bidder_row)
            
            
            
                
            
            
            
        #Seller

            Seller_Row = Seller_User_ID + columnSeparator + Seller_Rating + columnSeparator + Location + columnSeparator + Country + '\n'
            sellerFile.write(Seller_Row)
        
               
       
        
        

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print('Usage: python skeleton_json_parser.py <path to json files>', file=sys.stderr)
        sys.exit(1)
    # loops over all .json files in the argument
    print("Opening files")
    openFiles()
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            #test_individual(f)
            print("Success parsing " + f)
    print('Closing files')

if __name__ == '__main__':
    main(sys.argv)
