#!/usr/bin/env python
# coding: utf-8

# In[12]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

def make_detailed_df(url):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    houses = soup.find_all(lambda tag: tag.name == 'article' and 
                                       tag.get('class') == ['displaypanel'])
    prices = []
    ttl_squ_feet = []
    maintance = []
    gross_taxes = []
    bedrooms = []
    bathrooms = []
    property_type = []
    year_built = []
    styles = []
    title_list = []
    features_list = []
    amenities_list = []
    appliances_list = []
    neighborhood_list = []
    hyperlink = []
    for house in houses: 
        house_href = house.div.div.a['href']
        house_url = requests.get(f'https://www.rew.ca/{house_href}').text
        soup = BeautifulSoup(house_url,'lxml')
        
        ul = soup.find_all('ul',class_='listingheader-details l-pipedlist l-pipedlist--breathe')
        area = ul[0].find_all('li')[2].text
        house_details = soup.find_all('tbody')
        price_details = house_details[0].find_all('tr')
        list_price = price_details[0].td.text
        if 'Gross Taxes' not in str(price_details):
            gross_t = 'NaN'
        else: gross_t = price_details[1].td.text
        if 'Maintenance Fees' not in str(price_details):
            maintenance_fees = 'NaN'
        elif 'Gross Taxes' not in str(price_details): 
            maintenance_fees = price_details[1].td.text.replace('\n','')
        else: maintenance_fees = price_details[2].td.text.replace('\n','')
        
        home_facts = house_details[1].find_all('tr')
        home_facts_list = [str(i) for i in list(home_facts)]
        home_facts_labels_list = ['Bedrooms','Bathrooms','Property Type','Year Built','Title','Style','Amenities'
                      'Appliances','Community','Features']
        if 'Bedrooms' not in ''.join(home_facts_list):
            bdrms = None
        if 'Bathrooms' not in ''.join(home_facts_list):
            bthrms = None
        if 'Property Type' not in ''.join(home_facts_list):
            ppty_type = None
        if 'Year Built' not in ''.join(home_facts_list):
            yr_built = None
        if 'Title' not in ''.join(home_facts_list):
            title = None
        if 'Style' not in ''.join(home_facts_list):
            style = None
        if 'Amenities' not in ''.join(home_facts_list):
            amenities = None
        if 'Appliances' not in ''.join(home_facts_list):
            appliances = None
        if 'Community' not in ''.join(home_facts_list):
            neighborhood = None
        if 'Features' not in ''.join(home_facts_list):
            features = None
        for i in list(range(len(home_facts_list))):
            if 'Community' in home_facts_list[i]: 
                neighborhood = home_facts[i].td.text
            if 'Bedrooms' in home_facts_list[i]: 
                bdrms = home_facts[i].td.text
            if 'Bathrooms' in home_facts_list[i]: 
                bthrms = home_facts[i].td.text
            if 'Property Type' in home_facts_list[i]: 
                ppty_type = home_facts[i].td.text
            if 'Year Built' in home_facts_list[i]:
                yr_built = home_facts[i].td.text.replace('Built in ','')
            if 'Style' in home_facts_list[i]: 
                style = home_facts[i].td.text
            if 'Title' in home_facts_list[i]: 
                title = home_facts[i].td.text
            if 'Amenities' in home_facts_list[i]: 
                amenities = home_facts[i].td.text
            if 'Appliances' in home_facts_list[i]: 
                appliances = home_facts[i].td.text
            if 'Features' in home_facts_list[i]: 
                features = home_facts[i].td.text
            
        prices.append(list_price)
        ttl_squ_feet.append(area)
        maintance.append(maintenance_fees)
        gross_taxes.append(gross_t)
        bedrooms.append(bdrms)
        bathrooms.append(bthrms)
        property_type.append(ppty_type)
        year_built.append(yr_built)
        styles.append(style)
        amenities_list.append(amenities)
        appliances_list.append(appliances)
        neighborhood_list.append(neighborhood)
        title_list.append(title)
        features_list.append(features)
        hyperlink.append(f'https://www.rew.ca/{house_href}')

    my_columns = ['List Price', 
                  'Total Square Feet',
                  'Maintenance Fees', 
                  'Gross Tax', 
                  'Bedrooms', 
                  'Bathrooms',
                  'Property Type', 
                  'Year Built', 
                  'Title', 
                  'Style',
                  'Features', 
                  'Amenities',
                  'Appliances',
                  'Neighborhood', 
                  'Link'
                 ]
    list_of_str = list(zip(prices,
                           ttl_squ_feet,
                           maintance,
                           gross_taxes,
                           bedrooms,
                           bathrooms,
                           property_type,
                           year_built,
                           title_list,
                           styles,
                           features_list,
                           amenities_list,
                           appliances_list,
                           neighborhood_list,
                           hyperlink
                          ))
    df = pd.DataFrame(list_of_str,columns=my_columns)
    return df  

def save_df(df,filename):
    df.to_csv(fr'/Users/veliristimaki/Downloads/data_scaping/{filename}.csv', index = False)

print('Setup Complete')


# In[13]:


for page in list(range(1,26)):
    url = f'https://www.rew.ca/properties/areas/vancouver-bc/type/apartment-condo/sort/latest/desc/page/{page}?query=Vancouver%2C+BC'
    df = make_detailed_df(url)
    save_df(df,f'housing_{page}')
    print(f'Housing data from page {page} has been successfully extracted')
    

