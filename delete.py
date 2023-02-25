
from pymongo import MongoClient


def get_database():
    user = "samg54"  # NEED TO ADD UR OWN USER
    passw = "mongo999"  # NEED TO ADD UR OWN PASS

    client = MongoClient(
        f"mongodb+srv://{user}:{passw}@ngcluster.sbambjh.mongodb.net/?retryWrites=true&w=majority")

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    # CONNECTION_STRING = "mongodb+srv://" + user + ":" + passw + "@ngcluster.sbambjh.mongodb.net/test"

    # # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    # client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client.companiesDB


dbname = get_database()

collection_name = dbname.aidan

# collection_name.update_one({"cname": 'a'}, {"$set": {"html": ''}})
# collection_name.insert_one({'a': 'a', 'b': 'f'})
# collection_name.delete_many({})
collection_name.drop()
print('done')
