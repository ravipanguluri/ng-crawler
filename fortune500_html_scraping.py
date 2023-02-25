import re
import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
import signal
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
        #check if url is a string
        if isinstance(urls[i], str):
            urls[i] = urls[i].lower()
            #split urls into http/host/suffix groups 
            groups = urls[i].split('//')
            #if I have a single group, it means no http, so add it
            if len(groups) == 1:
                urls[i] =  "http://" + groups[0]
            #if I have two groups, I want to standardize http at the begining, so just add it
            elif len(groups) == 2:
                urls[i] =  "http://" + groups[1]
            #this means I have 2x http in link, so remove the second version and add // that I removed on split
            elif len(groups) == 3:
                urls[i]  = groups[0] + "//" + groups[2]
            else:
                print(f"reached else on {urls[i]}")

def crawlURLS(url):
    global counter
    try:
        headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
        #10 timeout for a request
        result = requests.get(url, headers = headers, timeout = 10)
        #extract the host name from the url
        domain = re.match("(?:http://|https://)?(?:www.)?([a-z0-9A-Z-]+)(?:.[a-z]+)",url).groups()[0]

        if result.status_code == 200:
            soup = BeautifulSoup(result.text, 'html.parser')
            soup_str = str(soup.get_text())
            #using a set for internal links so that I do not get repeats
            internal_links = {link.get('href') for link in soup.find_all('a') if link.get('href') and domain in link.get('href')}
            #crawl internal links if they are http links that I can navigate to 
            html_strings = [re.sub("\s{2,}", " ", BeautifulSoup(requests.get(link, headers = headers, timeout = 10).text, 'html.parser').get_text()) for link in internal_links if link and bool(re.search('^https?://', link))]
            #get html from home page prepended to the list of html strings
            html_strings.insert(0, soup_str)
            #concatenate the html strings to each other
            concatted = ''.join(html_strings)
            if not concatted or concatted.isspace():
                print(f"The html came out at null for {url}")
            return concatted
        else:
            print(f"This url could not be reached: {url}")
            return None
    except Exception as e:
        counter += 1
        print(f"link failed = {counter}")
        print(f"This exception was thrown {repr(e)}")
        print(url)
        return None

def scrapeSites(collection_name):
    global counter
    # get urls from db
    urls = old_urls= collection_name.distinct("website")
    process_urls(urls)
    i = 0
    
    #urls and unprocessed urls might be different so I want to crawl formatted urls, but update db entries corresponding to the old ones
    for url, old_url in zip(urls, old_urls):
        try:
            site_text = crawlURLS(url)[:100000] #limit document size so no exception is thrown when adding to db
            #check if i've returned a blank string (could be due to exception)
            if not site_text or site_text == "":
                print(f" This url yielded no text {url}")
            print(site_text)
            #update database entry corresponding to website url in the database
            collection_name.update_one({"website": old_url}, {"$set": {"html": site_text}})
            print(f"This is the old url {old_url}")
            print(f"added html for {i} sites")
            i += 1 
        except Exception as e:
            #if anything fails, catch exception and increment the number of failed links
            counter += 1
            print(f"The exception that I caught was {repr(e)}")
            print(f"link failed = {counter}")
        
        
   
    return None


dbname = get_database()
scrapeSites(dbname.venture_capital)
scrapeSites(dbname.fortune500)
