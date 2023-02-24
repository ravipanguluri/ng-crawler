
from bs4 import BeautifulSoup


class ScrapeAsyncResult:
    def __init__(self, root_link: str, cname: str, industry: str):
        self.root_link: str = root_link
        self.raw_html: str = ''
        self.links = []
        self.cancelled = False
        self.cname = cname
        self.industry = industry

    def set_raw_html(self, raw_html: str):
        self.raw_html = raw_html
        soup = BeautifulSoup(raw_html, "html.parser")
        for tag in soup.find_all():
            if tag.name == 'a':
                try:
                    self.links.append(str(tag['href']))
                except KeyError:
                    pass

    def get_raw_html(self):
        if not self.cancelled:
            return self.raw_html
        else:
            return 'n/a'

    def get_all_links(self):
        return self.links
