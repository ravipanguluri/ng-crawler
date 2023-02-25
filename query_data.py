
from pymongo import MongoClient

import pymongo

user = "samg54"  # NEED TO ADD UR OWN USER
passw = "mongo999"  # NEED TO ADD UR OWN PASS

client = MongoClient(
    f"mongodb+srv://{user}:{passw}@ngcluster.sbambjh.mongodb.net/?retryWrites=true&w=majority&socketTimeoutMS=100000&connectTimeoutMS=100000&serverSelectionTimeoutMS=100000")

# Provide the mongodb atlas url to connect python to mongodb using pymongo
# CONNECTION_STRING = "mongodb+srv://" + user + ":" + passw + "@ngcluster.sbambjh.mongodb.net/test"

# # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
# client = MongoClient(CONNECTION_STRING)

# Create the database for our example (we will use the same database throughout the tutorial
db = client.companiesDB
collection = db['aidan_gov_companies']


myquery = { "html": { "$regex": "fpga" } }

# myquery = {'cname': {'$regex': '3T-INNOVATIONS, LLC'}}

mydoc = collection.find(myquery)

i = 0
for x in mydoc:
    if i == 4:
        break
    i = i + 1
    print(x['_id'], x['cname'], x['website'], x['industry'])
