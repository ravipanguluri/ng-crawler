import os
import pandas as pd
import numpy as np
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import re

counter = 0

def load_data(data_path):
    return os.listdir(data_path)


def process_csvs():
    all_objects = []

    data_path = "./data"
    csvs = load_data(data_path)
    print(csvs)
    for i in csvs:
        df = pd.read_csv(data_path + "/" + i)
        df.drop(index=range(0, 6), inplace=True)
        df['cname'] = df.Vendor
        df['website'] = df.URL
        df['industry'] = df['Sub Category']

        keep_cols = ['cname', 'website', 'industry']
        df.drop(columns=([i for i in list(df.columns) if i not in keep_cols]), axis=1, inplace=True)

        company_objects = df.to_dict(orient='records')
        all_objects.extend(company_objects)
        print(len(company_objects))
    return all_objects

def process_urls(urls):
    for i in range(len(urls)):
        if isinstance(urls[i], str):
            urls[i] = urls[i].lower()
            groups = urls[i].split('//')
            if len(groups) == 1:
                if not groups[0].startswith("www."):
                    groups[0] = "www." + groups[0]
                urls[i] =  "http://" + groups[0]
            elif len(groups) == 2:
                if not groups[1].startswith("www."):
                    groups[1] = "www." + groups[1]
                urls[i] =  "http://" + groups[1]
            elif len(groups) == 3:
                if not groups[2].startswith("www."):
                    groups[2] = "www." + groups[2]
                urls[i]  = groups[0] + "//" + groups[2]
            else:
                print(f"reached else on {urls[i]}")
        


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


def crawlURLS(url):
    global counter
    try:
        result = requests.get(url)
        domain = re.match("http://(?:www.)?(\w+.com)", url).groups()[0]

        if result.status_code == 200:
            soup = BeautifulSoup(result.text, 'html.parser')
            soup_str = str(soup)
            print(soup.find_all("a"))
            #using a set for internal links so that I do not get repeats
            internal_links = {link.get('href') for link in soup.find_all('a') if link.get('href') and domain in link.get('href')}
            html_strings = [requests.get(link).text for link in internal_links if link and link.__contains__('^https?://')]
            html_strings.insert(0, soup_str)
            return ''.join(html_strings)
        else:
            return None
    except:
        counter += 1
        print(f"link failed = {counter}")
        return None

def main():
    dbname = get_database()
    res = process_csvs()
    collection_name = dbname.govcompanies
    urls = [res[i]['website'] for i in range(len(res))]
    process_urls(urls)
    print(urls)
    print(zip)

   
    for i, (db_site, parsed_site) in enumerate(zip(res, urls)):
        site_text = crawlURLS(parsed_site)
        collection_name.update_one({"cname": res[i]['cname']}, {"$set": {"html": site_text}})
        print(f"added html for {i} sites")
        print(res[i]['website'])
    print("Uploaded ", len(res), "documents")
    return res


 
main()
