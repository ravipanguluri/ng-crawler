import os
import pandas as pd
import numpy as np
from pymongo import MongoClient


def load_data(data_path):
    return (os.listdir(data_path))

def process_csvs():
    all_objects = []
    data_path = "./data2"
    csvs = load_data(data_path)
    print(csvs)
    for i in csvs:
        df = pd.read_csv(data_path + "/" + i)
        df['cname'] = df.companyname
        df.year_founded = df.year_founded.astype(str)

        keep_cols = ['cname', 'website', 'min_employees', 'max_employees', 'year_founded', 'descriptors', 'description', 'total_investment']
        df.drop(columns = ([i for i in list(df.columns) if i not in keep_cols]), axis = 1, inplace = True)
        df['website'] = 'https://' + df.website
        company_objects = df.to_dict(orient = 'records')
        all_objects.extend(company_objects)
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
    collection_name = dbname.github_sanfran
    collection_name.delete_many({})          # RESET DATABASE IF NEEDED
    collection_name.insert_many(res)
    print("Uploaded ", len(res), "documents")
    return res


 
main()
