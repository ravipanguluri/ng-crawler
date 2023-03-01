import os
import pandas as pd
import numpy as np
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup   


def process_url():
    companies = []                                  # companies list to upload to db
    url = "https://www.zyxware.com/articles/4344/list-of-fortune-500-companies-and-their-websites"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')     # html parsing
    tables = soup.find_all('tbody')                 # for each body (in table) 
    for table in tables:    
        for row in table.find_all('tr'):            # scan each row
            data = row.find_all('td')               # for each of 3 table datapoints - company number, company name, and company link
            num = data[0].text
            if(int(num) % 25 == 0):
                print("Processing Company #: ", num)
            companies.append({'cname': data[1].text, 'website': data[2].text})
    return companies
            

def get_database():
    user = "samg54"  # NEED TO ADD UR OWN USER
    passw =          # NEED TO ADD UR OWN PASS

    client = MongoClient(f"mongodb+srv://{user}:{passw}@ngcluster.sbambjh.mongodb.net/?retryWrites=true&w=majority&socketTimeoutMS=100000&connectTimeoutMS=100000&serverSelectionTimeoutMS=100000")

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    # CONNECTION_STRING = "mongodb+srv://" + user + ":" + passw + "@ngcluster.sbambjh.mongodb.net/test"
    
    # # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    # client = MongoClient(CONNECTION_STRING)
    
    # Create the database for our example (we will use the same database throughout the tutorial

    return client.companiesDB

def main():
    dbname = get_database()
    res = process_url()
    collection_name = dbname.fortune500        # store in fortune500 collection
    # collection_name.delete_many({})          # RESET DATABASE IF NEEDED
    collection_name.insert_many(res)
    print("Uploaded ", len(res), "documents")
    return res


 
main()
