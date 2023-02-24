import re
import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
import signal
import sys

counter = 0

def signal_handler(signum, frame):
    raise Exception("Timed out!")

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

def main():
    dbname = get_database()
    collection_name = dbname.fortune500
    urls = collection_name.distinct("website")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(10)
    i = 0
    
    for url in urls:
        try:
            site_text = crawlURLS(url)
            collection_name.update_one({"website": url}, {"$set": {"html": site_text}})
            print(f"added html for {i} sites")
            i += 1 
        except:
            print("took too long")
        
   
    return None

    
 
main()