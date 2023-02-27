from pymongo import MongoClient

def get_database():
    user = "samg54"  # NEED TO ADD UR OWN USER
    passw = "mongo999"  # NEED TO ADD UR OWN PASS

    client = MongoClient(
        f"mongodb+srv://{user}:{passw}@ngcluster.sbambjh.mongodb.net/?retryWrites=true&w=majority&socketTimeoutMS=100000&connectTimeoutMS=100000&serverSelectionTimeoutMS=100000")

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    # CONNECTION_STRING = "mongodb+srv://" + user + ":" + passw + "@ngcluster.sbambjh.mongodb.net/test"

    # # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    # client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client.companiesDB

def get_all_site_text(collection):
    site_text = []
    cnames = []
    items = collection.find()
    for item in items: 
        site_text.append(item['html'])
        cnames.append(item['cname'])
    return cnames, site_text

db = get_database()
collections = [db.aidan_gov_companies,  db.venture_capital, db.fortune500]

for collection in collections:
    for doc in collection.find():
        newvalues = { "$set": { 'length': len(doc['html']) } }
        collection.update_one({'cname' : doc['cname']}, newvalues)
