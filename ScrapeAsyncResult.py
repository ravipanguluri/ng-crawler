
from bs4 import BeautifulSoup
import re


class ScrapeAsyncResult:
    def __init__(self, root_link: str, cname: str, industry: str, host: str):
        self.root_link: str = root_link
        self.raw_html: str = ''
        self.site_text: str = ''
        self.links = []
        self.cancelled = False
        self.cname = cname
        self.industry = industry
        self.host = host

    def set_raw_html(self, raw_html: str):
        self.raw_html = raw_html
        soup = BeautifulSoup(raw_html, "html.parser")
        #get the site text and remove extra spaces to maximize storage on db
        self.site_text = re.sub("\s{2,}", " ", soup.get_text(separator= ' '))
        for a_tag in soup.find_all("a"):
            link = a_tag.get('href')
            if link and self.host in link and bool(re.search('^https?://', link)):
                self.links.append(link)

    def get_raw_html(self):
        if not self.cancelled:
            return self.raw_html
        else:
            return 'n/a'

    def get_all_links(self):
        return self.links
    
    def append_link_text(self, raw_html: str):
        soup = BeautifulSoup(raw_html, "html.parser")
        self.site_text += " " + re.sub("\s{2,}", " ", soup.get_text(separator= ' '))

