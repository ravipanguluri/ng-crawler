
from bs4 import BeautifulSoup


class ScrapeAsyncResult:
    def __init__(self, raw_html: str):
        self.raw_html: str = raw_html
        self.links = []
        soup = BeautifulSoup(raw_html, "html.parser")
        for tag in soup.find_all():
            if tag.name == 'a':
                self.links.append(str(tag['href']))

    def get_raw_html(self):
        return self.raw_html

    def get_all_links(self):
        return self.links
