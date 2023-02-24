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
        headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
        result = requests.get(url, headers = headers, timeout = 10)
        domain = re.match("(?:http://|https://)?(?:www.)?([a-z0-9A-Z-]+)(?:.[a-z]+)",url).groups()[0]

        if result.status_code == 200:
            soup = BeautifulSoup(result.text, 'html.parser')
            soup_str = str(soup)
            print(soup.find_all("a"))
            #using a set for internal links so that I do not get repeats
            internal_links = {link.get('href') for link in soup.find_all('a') if link.get('href') and domain in link.get('href')}
            # print(internal_links)
            # html_strings = []
            # for link in internal_links:
            #     if link and bool(re.search('^https?://', link)):
            #         print(link)
            #         try:
            #             print(requests.get(link).text)
            #             html_strings.append(requests.get(link).text)
            #         except:
            #             print("could not parse internal link")
            html_strings = [requests.get(link, headers = headers, timeout = 10).text for link in internal_links if link and bool(re.search('^https?://', link))]
            print(html_strings)
            html_strings.insert(0, soup_str)
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
        # sys.exit()
        return None

def main():
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