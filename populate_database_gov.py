import os
import pandas as pd
import numpy as np
from pymongo import MongoClient
from ScrapeAsync import ScrapeAsync

# what do I want to do:
#   for every company without blank website:
#       get that company's HTML
#       get that company's sub pages HTML


def process_csv():
    all_objects = []
    data_path = "./data/schedule_MAS.csv"
    df = pd.read_csv(data_path)
    df = df[df['Large Category'] == 'Information Technology']
    df['cname'] = df.Vendor
    df['website'] = df.URL
    df['industry'] = df['Sub Category']

    keep_cols = ['cname', 'website', 'industry']
    df.drop(columns=([i for i in list(df.columns) if i not in keep_cols]), axis=1, inplace=True)
    df = df.astype({'website': str})

    company_objects = df.to_dict(orient='records')
    all_objects.extend(company_objects)
    return all_objects


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


def main():
    dbname = get_database()
    res = process_csv()
    collection_name = dbname.aidan_gov_companies
    # collection_name.delete_many({})          # RESET DATABASE IF NEEDED
    i = 0
    scrape_obj = ScrapeAsync([(a['website'], a['cname'], a['industry']) for a in res])
    results = scrape_obj.scrape_all()

    for result in results:
        pass
    # collection_name.insert_many(res)
    print("Uploaded ", len(res), "documents")
    return res


def test():
    dbname = get_database()
    print(dbname)
    collection = dbname['aidan_gov_companies']
    print(collection)
    # inserted_id = collection.insert_many([{'a': '4', 'b': '2', 'c': '3'}, {'a': '0', 'b': '0', 'c': '0'}]).inserted_ids
    inserted_id = collection.insert_many([{'a': '4', 'b': '2', 'c': '3'}]).inserted_ids

    print(inserted_id)


test()
# main()
# process_csv()
