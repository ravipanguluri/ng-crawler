import re
import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
import sys

counter = 0

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


def crawlURLS(url):
    global counter
    try:
        result = requests.get(url)
        domain = re.match("(?:http://|https://)?(?:www.)?([a-z0-9A-Z-]+)(?:.[a-z]+)",url).groups()[0]

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
    except Exception as e:
        counter += 1
        print(f"link failed = {counter}")
        print(f"This exception was thrown {repr(e)}")
        print(url)
        # sys.exit()
        return None

def vc_scrape():
    dbname = get_database()
    collection_name = dbname.venture_capital
    urls = collection_name.distinct("website")
    i = 0
    
    for url in urls:
        site_text = crawlURLS(url)
        collection_name.update_one({"website": url}, {"$set": {"html": site_text}})
        print(f"added html for {i} sites")
        i += 1 
        
   
    return None

def fortune500Scrape():
    dbname = get_database()
    collection_name = dbname.fortune500
    urls = collection_name.distinct("website")
    process_urls(urls)
    i = 0
    
    for url in urls:
        try:
            site_text = crawlURLS(url)
            if not site_text or site_text == "":
                print(f" This url yielded no text {url}")
            collection_name.update_one({"website": url}, {"$set": {"html": site_text}})
            print(f"added html for {i} sites")
            i += 1 
        except Exception as e:
            print(f"{url} took too long")
            print(f" The exception that I caught was {repr(e)}")
        
        
   
    return None

    
 
main()