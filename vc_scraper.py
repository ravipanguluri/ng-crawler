import pandas as pd
import re
import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup

def get_vcs(url):
    # Webpage url    
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}                                                                                                           
    html = requests.get(url,headers = headers)
    soup = BeautifulSoup(html.text, 'html.parser')

    companies = []
    i = 0
    for link in soup.find_all('a'):
        if 'a16' not in link.get('href'):
            if(i > 34):  # skip 35 junk lines
                url = (link.get('href'))
                cname = re.match("(?:http://|https://)?(?:www.)?([a-z0-9A-Z-]+)(?:.[a-z]+)",url).groups()[0]
                companies.append({'cname': cname, 'website': url})
            i= i+1

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
    url = 'https://a16z.com/portfolio/'
    res = get_vcs(url)
    collection_name = dbname.venture_capital
    # collection_name.delete_many({})          # RESET DATABASE IF NEEDED
    collection_name.insert_many(res)
    print("Uploaded ", len(res), "documents")
   
    return res

    
 
main()


