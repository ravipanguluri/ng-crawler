import os
import pandas as pd
import numpy as np
from pymongo import MongoClient
from ScrapeAsync import ScrapeAsync
import re

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


def main(collection_name):
    res = list(collection_name.find({}))
    # collection_name.delete_many({})          # RESET DATABASE IF NEEDED
    i = 0
    scrape_obj = ScrapeAsync([(a['website'], a['cname'], "") for a in res])
    scrape_obj.scrape_all()
    # scrape_obj.crawl_urls()
    results = scrape_obj.get_scrape_results()
    total_links = 0
    
    

    for result in results:
        total_links += len(result.links)        
        # print(result.site_text)
        collection_name.update_one({"cname": result.cname }, {"$set": {"html": result.site_text}})
        # print(result.root_link)
    print(total_links)

    # collection_name.insert_many(res)
    print("Uploaded ", len(res), "documents")
    return res





dbname = get_database()
# main(dbname.venture_capital)
# main(dbname.fortune500)
main(dbname.github_sanfran)


