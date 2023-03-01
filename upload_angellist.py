import os
import pandas as pd
import numpy as np
from pymongo import MongoClient
from ScrapeAsync import ScrapeAsync

def process_csv():
    all_objects = []
    data_path = "./data/new_csv_angel_output.csv"
    df = pd.read_csv(data_path)
    df = df.astype({'website': str})
    df = df.astype({'company_name': str})
    df = df.astype({'num_employees': str})
    df = df.astype({'description': str})

    company_objects = df.to_dict(orient='records')
    all_objects.extend(company_objects)
    return all_objects


def get_database():
    user = "samg54"  # NEED TO ADD UR OWN USER
    passw = "mongo999"  # NEED TO ADD UR OWN PASS

    client = MongoClient(
        f"mongodb+srv://{user}:{passw}@ngcluster.sbambjh.mongodb.net/?retryWrites=true&w=majority&socketTimeoutMS=100000&connectTimeoutMS=100000&serverSelectionTimeoutMS=100000")

    return client.companiesDB


def main():
    dbname = get_database()
    res = process_csv()
    collection = dbname.angel_list

    scrape_obj = ScrapeAsync([(a['website'], a['company_name'], a['num_employees'], a['description']) for a in res])
    results = scrape_obj.scrape_all()

    i = 0
    for result in results:
        collection.insert_one({'cname': result.cname, 'website': result.root_link,
                               'description': result.description,
                               'num_employees': result.num_employees, 'html': result.get_raw_html()})

    print("Uploaded ", len(res), "documents")

def delete():
    dbname = get_database()
    collection = dbname.angel_list
    collection.delete_many({})

main()
