
from ScrapeAsync import ScrapeAsync

my_scraper = ScrapeAsync(['https://example.com/', 'https://aidmelvin.github.io/personal-website/'])
for result in my_scraper.scrape_all():
    print(result.links)
