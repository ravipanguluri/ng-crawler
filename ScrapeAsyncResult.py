
from bs4 import BeautifulSoup
from bs4.element import Comment
import re


class ScrapeAsyncResult:
    def __init__(self, root_link: str, cname: str, num_employees: str, description: str):
        self.root_link: str = root_link
        self.raw_html: str = ''
        self.links = []
        self.cancelled = False
        self.cname = cname
        self.num_employees = num_employees
        self.description = description

    def set_raw_html(self, raw_html: str):
        self.raw_html = raw_html
        soup = BeautifulSoup(raw_html, "html.parser")
        for tag in soup.find_all():
            if tag.name == 'a':
                try:
                    self.links.append(str(tag['href']))
                except KeyError:
                    pass

    @staticmethod
    def tag_visible(element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def get_raw_html(self):
        if not self.cancelled:
            # return self.raw_html
            soup = BeautifulSoup(self.raw_html, 'html.parser')
            # try:
            #     print(type(soup.findAll(text=True)))
            #     print(soup.findAll(text=True)[0])
            #     print(''.join(soup.findAll(text=True)))
            #     texts = str(re.sub(' {2,}', ' ', ''.join(soup.findAll(text=True))))
            # except:
            #     texts = ''
            texts = soup.findAll(text=True)
            visible_texts = filter(ScrapeAsyncResult.tag_visible, texts)
            # return u" ".join(t.strip() for t in visible_texts)
            return re.sub(' {2,}', ' ', u" ".join(t.strip() for t in visible_texts))
        else:
            return 'n/a'

    def get_all_links(self):
        return self.links
