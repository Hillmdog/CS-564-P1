#!/bin/bash
python3 skeleton_parser.py ebay_data/ebay_data/items-*.json

# lets remove some duplicats, one file at a time
# seller
awk '!visited[$0]++' seller.dot > seller.dat
awk '!visited[$0]++' bid.dot > bid.dat
awk '!visited[$0]++' bidder.dot > bidder.dat
awk '!visited[$0]++' item.dot > item.dat
awk '!visited[$0]++' auction.dot > auction.dat

# remove old files
rm -fv seller.dot
rm -fv bid.dot
rm -fv bidder.dot
rm -fv item.dot
rm -fv auction.dot
