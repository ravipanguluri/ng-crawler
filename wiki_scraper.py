import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://en.wikipedia.org/wiki/List_of_unicorn_startup_companies"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

table = soup.find('table', {'class': 'wikitable sortable'})
rows = table.find_all('tr')[1:]

data = []

for row in rows:
    cols = row.find_all('td')
    company = cols[0].text.strip()
    refs = cols[2].find_all('a')
    for ref in refs:
        try:
            response = requests.get(ref['href'])
            ref_soup = BeautifulSoup(response.content, 'html.parser')
            company_url = ref_soup.find('a')['href']
            break
        except:
            company_url = ''
    data.append([company, company_url])

df = pd.DataFrame(data, columns=['Company', 'URL'])
print(df)

