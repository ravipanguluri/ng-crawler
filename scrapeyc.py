import os
import pandas as pd
import numpy as np
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup   



def process_url(url):
    companies = []
    r = requests.get(url)       
    soup = BeautifulSoup(r.content, 'html.parser')     # html parsing
    # tables = soup.find_all('a')                 # for each body (of a table)
    # links = []
    # print(tables    )
    # for table in tables:                
    #     links.append(table.get_all('href'))
    for table_row in soup.find_all('tr'):
        cname = table_row.get('data-company-id')
        if cname != None:
            website = None
            for row in table_row:
                a_tags = row.find_all('a')
                counter = 1
                for a in a_tags:
                    if counter ==2:
                        website = a.get('href')
                    counter += 1
            companies.append({'cname': cname, 'website': website})
    return companies

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
    urls  = ["https://www.ycombinator.com/topcompanies", "https://www.ycombinator.com/topcompanies/public   "]
    for url in urls:
        res = process_url(url)
        collection_name = dbname.test_sanfran        # access YC collecton on db
        # collection_name.delete_many({})          # RESET DATABASE IF NEEDED
        collection_name.insert_many(res)
        print("Uploaded ", len(res), "documents")
    return 

 
main()
