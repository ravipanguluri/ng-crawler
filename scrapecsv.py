import os
import pandas as pd
import numpy as np
from pymongo import MongoClient


def load_data(data_path):
    return (os.listdir(data_path))

def process_csvs():
    all_objects = []

    data_path = "./data"
    csvs = load_data(data_path)
    print(csvs)
    for i in csvs:
        df = pd.read_csv(data_path + "/" + i)
        df.drop(index = range(0 ,6), inplace = True)
        df['cname'] = df.Vendor
        df['website'] = df.URL
        df['industry'] = df['Sub Category']

        keep_cols = ['cname', 'website', 'industry']
        df.drop(columns = ([i for i in list(df.columns) if i not in keep_cols]), axis = 1, inplace = True)

        company_objects = df.to_dict(orient = 'records')
        all_objects.extend(company_objects)
        print(len(company_objects))
    return all_objects

def get_database():
    user = "samg54"  # NEED TO ADD UR OWN USER
    passw = "mongo999"          # NEED TO ADD UR OWN PASS

    client = MongoClient(f"mongodb+srv://{user}:{passw}@ngcluster.sbambjh.mongodb.net/?retryWrites=true&w=majority&socketTimeoutMS=100000&connectTimeoutMS=100000&serverSelectionTimeoutMS=100000")

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    # CONNECTION_STRING = "mongodb+srv://" + user + ":" + passw + "@ngcluster.sbambjh.mongodb.net/test"
    
    # # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    # client = MongoClient(CONNECTION_STRING)
    
    # Create the database for our example (we will use the same database throughout the tutorial
    return client.companiesDB

def main():
    dbname = get_database()
    res = process_csvs()
    collection_name = dbname.govcompanies
    # collection_name.delete_many({})          # RESET DATABASE IF NEEDED
    collection_name.insert_many(res)
    print("Uploaded ", len(res), "documents")
    return res


 
main()
