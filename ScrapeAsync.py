
from requests_futures.sessions import FuturesSession
from ScrapeAsyncResult import ScrapeAsyncResult
import time


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

    def blacklist(self):
        pass

    def scrape_all(self):
        # create all the background promises
        promises = []
        results = []
        for url in self.urls:
            if url[0].replace('\t', '').strip() != '' and url[0].strip().lower() not in self.ignore_urls \
                                                    and 'http://https:' not in url[0]:
                try:
                    promises.append(self.session.get(url[0], timeout=4))
                    results.append(ScrapeAsyncResult(url[0], url[1], url[2]))
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
                    results[i].cancelled = True

                else:
                    try:
                        results[i].set_raw_html(promise.result().content.decode('utf-8'))
                    except Exception as e:
                        print(f'{e}')
                        results[i].cancelled = True
            else:
                try:
                    results[i].set_raw_html(promise.result().content.decode('utf-8'))
                except Exception as e:
                    print(f'{e}')
                    results[i].cancelled = True

        return results
