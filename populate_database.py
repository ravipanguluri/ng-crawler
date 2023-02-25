import os
import pandas as pd
import numpy as np
from pymongo import MongoClient
from ScrapeAsync import ScrapeAsync

# what do I want to do:
#   for every company without blank website:
#       get that company's HTML


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
    collection = dbname.aidan_gov_companies

    scrape_obj = ScrapeAsync([(a['website'], a['cname'], a['industry']) for a in res])
    results = scrape_obj.scrape_all()

    array_to_insert = []
    for result in results:
        collection.insert_one({'cname': result.cname, 'website': result.root_link,
                               'industry': result.industry, 'html': result.get_raw_html()})

    # collection.insert_many(res)
    print("Uploaded ", len(res), "documents")

main()
