
# Startup Search - Our Web Crawling Tool

To run the frontend: 
1. `cd frontend`
2. `npm i` (you only have to do this once to install the packages)
3. `npm start`

To run the backend:
1. `export FLASK_APP=hello`
2. `export FLASK_ENV=development`
3. `flask run`



## Repository Directory

- **Final Product**
  - searching.py
  - hello.py (Flask App)
- **Company Data Scraping Tools**
  - fortune500scrape.py
  - scrapeyc.py
  - scrape_csv_git.py
  - scrape andreessen_horowitz.py
  - scrape_angellist.py
  - upload_angellist.py
- **Html Scraping**
  - ScrapeAsync.py
  - ScrapeAsyncResult.py
  - populate_database_gov.py
  - populate_database_general.py
- **Frontend**
  - ./frontend
- **Environment**
  - ng_env.yml
  
  ## Description
  
  Startup Search is a collection of distinct web scraping and web crawling tools, combined with our internal database and searching technique. Setup using MongoDB, our script-based database creation is designed to be easily expandable to new data sources. Some of our scripts incorporate different datasources into our database, and then our multithreaded ScrapeAsync and populate_database scripts build out the database by crawling through each URL to add the html for each company. Our internal searching algorithm then searches the text on each webpage and matches it to a keyword search, which is expanded using a prebuilt NLP package and synonym matcher.
  
  Altogether, Startup Search allows its users to quickly find reputable companies in specialized technology areas, where typical search engines such as Google will only reveal articles with their own lists of companies, that are often repeated over each additional search entry. Startup Search can easily be changed to show as many search results as neccessary, although we only display 10 in our current frontend for ease-of-display. While google searches will yield ad-heavy results, Startup Search goes to each company's website directly and sees what they have to say about themselves - allowing the user to find hidden gyms in different industries that may be difficult to find by traditional means.
  
  Run the frontend react app and backend flask app simutaneously to give it a try!
  
