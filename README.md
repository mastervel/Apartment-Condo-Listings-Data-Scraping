# Apartment-Condo-Listings-Data-Scraping

This project involves data scraping the site: https://www.rew.ca/. This initial motivation for this project was simple, I wanted to apply my recent knowledge of data scraping on a website that I thought to be interesting and worthwhile for me. It is a dream of mine to own a piece of real estate of my own one day but I want to be able to leverage the use of sound data analytics in order to buy the property that is undervalued. 

The first step on this journey would involve gathering data which is what this depository will be all about. Gathering the raw data (with the use if BeautifulSoup for web scraping) and then cleaning the data to make it more readable and usable (with pandas dataframes). 

the files **data_scraping_fnc.ipynb** and **data_scraping_fnc.py** contains the code I used to data scrape the page on rew.ca corresponding to apartment/condos in Vancouver, BC sorted by the most recent entries on the site. If you want to use it you would have to change the filepaths. 

**housing_pg1.csv** contains the data from the data scraping of the first page of the webpage. Now I want to scrape more pages on the site as I don't have enough data points with only 20 listings. 

The **data_scraping_final.py** is an updated version of **data_scraping_fnc.py**. It is able to scrape all listings for apartment/condo on the rew.ca website. The data from running this is stored in the data folder. 
