
from requests_futures.sessions import FuturesSession
from ScrapeAsyncResult import ScrapeAsyncResult
import time
import re
import sys


# this class will be the base framework used to scrape large numbers of
# URLs at the same time
class ScrapeAsync:
    def __init__(self, urls):
        self.urls = urls
        # increase the max concurrent workers a little bit
        self.session = FuturesSession(max_workers=50)
        self.ignore_urls = {
            'www.ams1.net',
            'http://52networks.com',
            'www.advantageoptics.com',
            'http://www.aesupply.org',
            'http://www.xicomputer.com',
            'www.affinitechinc.com',
            'www.aitacs.com',
            'http:///www.allcomgs.com',
            'nan',
            'www.aocconnect.com',
            'www.abmfederal.com',
            'www.archivedata.com/',
            'http://https://www.archivedata.com/',
            'http://https://arkhamtechnology.com/',
            'www.ascomwireless.com',
            'www.asymmetric.com',
            'http:///www.avidsys.com',
            'www.bahfed.com',
            'http://www.best-ent.com',
            'www.bpstechnologies.com',
            'http://www.fivepointsservices.com',
        }
        self.scrape_results = [] * len(self.urls) #need to store 

    def blacklist(self):
        pass

    def scrape_all(self):
        # create all the background promises
        promises = []
        for i in range(len(self.urls)):
            url = self.urls[i] #extract url
            if url[0].replace('\t', '').strip() != '' and url[0].strip().lower() not in self.ignore_urls \
                                                    and 'http://https:' not in url[0]:
                try:
                    promises.append(self.session.get(url[0], timeout=4))
                    host = re.match("(?:http://|https://)?(?:www.)?([a-z0-9A-Z-]+)(?:.[a-z]+)",url[0]).groups()[0]
                    self.scrape_results.append(ScrapeAsyncResult(url[0], url[1], url[2], host + ".com"))
                except:
                    print(f'error on {url}')

        # resolve all the promises
        i = -1
        print(f'total that need to be completed: {len(promises)}')
        for promise in promises:
            i = i + 1
            print(i)
            if promise.running():
                time.sleep(2)
                # if the promise is still running after sleeping for 2 seconds...
                if promise.running():
                    promises[i].set_exception(BaseException())
                    self.scrape_results[i].cancelled = True

                else:
                    try:
                        self.scrape_results[i].set_raw_html(promise.result().content.decode('utf-8'))
                    except Exception as e:
                        print(f'{e}')
                        self.scrape_results[i].cancelled = True
            else:
                try:
                    self.scrape_results[i].set_raw_html(promise.result().content.decode('utf-8'))
                except Exception as e:
                    print(f'{e}')
                    self.scrape_results[i].cancelled = True

    def get_scrape_results(self):
        return self.scrape_results

    def crawl_urls(self):
        self.session = FuturesSession(max_workers=50) #reset the session

        promises = [[]] * 10 #testing a small number of links (replace with the length of scrape_results when working)
        for i in range(len(self.scrape_results)):
            scrape = self.scrape_results[i]
            for link in scrape.get_all_links()[:75]:
                try:
                    promises[i].append(self.session.get(link, timeout = 4)) #make all promises for all the internal links on the scrape results
                except:
                    print(f"error on {link}")

        counter = 1
        for i in range(len(promises)):
            promise_list = promises[i] 
            for j, promise in enumerate(promise_list): #iterate over list of promises
                print(counter)
                counter += 1
                if promise.running():
                    time.sleep(2)
                    # if the promise is still running after sleeping for 2 seconds...
                    if promise.running():
                        promises[i][j].set_exception(BaseException())

                    else:
                        try:
                            print(promise.result().url) #print urls to show that the same ones repeat over and over again
                            self.scrape_results[i].append_link_text(promise.result().content.decode('utf-8'))
                        except Exception as e:
                            print(f'{e}')
                else:
                    try:
                        print(promise.result().url)
                        self.scrape_results[i].append_link_text(promise.result().content.decode('utf-8'))
                    except Exception as e:
                        print(f'{e}')
        

        
