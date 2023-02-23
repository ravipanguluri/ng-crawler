
from requests_futures.sessions import FuturesSession
from ScrapeAsyncResult import ScrapeAsyncResult


# this class will be the base framework used to scrape large numbers of
# URLs at the same time
class ScrapeAsync:
    def __init__(self, urls):
        self.urls = urls
        # increase the max concurrent workers a little bit
        self.session = FuturesSession(max_workers=15)

    def scrape_all(self):
        # create all the background promises
        promises = []
        for url in self.urls:
            promises.append(self.session.get(url))

        # resolve all the promises
        results = []
        for promise in promises:
            results.append(ScrapeAsyncResult(promise.result().content.decode('utf-8')))

        return results
