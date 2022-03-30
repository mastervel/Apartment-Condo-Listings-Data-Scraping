import requests
from bs4 import BeautifulSoup
import pandas as pd

def make_detailed_df():
    url = 'https://www.rew.ca/properties/areas/vancouver-bc/sort/latest/asc/page/1?property_type=apartment-condo&query=Vancouver%2C+BC'
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    houses = soup.find_all(lambda tag: tag.name == 'article' and 
                                       tag.get('class') == ['displaypanel'])
    # This emtpy lists below are the lists that will be appended by each listing scraped. Later the list will be combined using zip()
    # and then converted into a dataframe that we want.
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
    
    # We loop through the houses variable which is a list of all the listings. However we want to gather more details of the listing like 
    # the amenities, year built, and appliances which are not on the web page with the url variable above. Therefore we loop through the
    # houses variable to get these extra details about the listings using the links in the 'a' tag of each item in the houses lists. 
    for house in houses: 
        house_href = house.div.div.a['href']
        house_url = requests.get(f'https://www.rew.ca/{house_href}').text
        soup = BeautifulSoup(house_url,'lxml')
        
        # If there are any listing on the page which was removed add this to ignore those pages
        # or else there will be an error. 
#         main_content = soup.find('div', class_='container')
#         if str(main_content.h1)!='None':
#             continue

        ul = soup.find_all('ul',class_='listingheader-details l-pipedlist l-pipedlist--breathe')
        area = ul[0].find_all('li')[2].text
        house_details = soup.find_all('tbody')
        price_details = house_details[0].find_all('tr')
        list_price = price_details[0].td.text
        
        # Some listings do not have details pertaining to gross taxes and maintenance fees 
        if 'Gross Taxes' not in str(price_details):
            gross_t = 'NaN'
        else: gross_t = price_details[1].td.text
        if 'Maintenance Fees' not in str(price_details):
            maintenance_fees = 'NaN'
        elif 'Gross Taxes' not in str(price_details): 
            maintenance_fees = price_details[1].td.text.replace('\n','')
        else: maintenance_fees = price_details[2].td.text.replace('\n','')
        
        home_facts = house_details[1].find_all('tr')
        bdrms = home_facts[0].td.text
        bthrms = home_facts[1].td.text
        ppty_type = home_facts[2].td.text
        yr_built = home_facts[3].td.text.replace('Built in ','')
        title = home_facts[4].td.text
        style = home_facts[5].td.text
        
        # This is a rather complicated if statement but it essentially replaces missing values with 'NaN' for the features seen in the if statement
        headers = soup.find_all('th')
        if 'Features' in str(headers):
            features = home_facts[6].td.text
            if 'Amenities' in str(headers):
                amenities = home_facts[7].td.text
                if 'Appliances' in str(headers):
                    appliances = home_facts[8].td.text
                    if 'Community' in str(headers):
                        neighborhood = home_facts[9].td.text
                    else: neighborhood = 'NaN'
                elif 'Community' in str(headers):
                    neighborhood = home_facts[8].td.text
                    appliances = 'NaN'
            elif 'Appliances' in str(headers):
                appliances = home_facts[7].td.text
                amenities = 'NaN'
                if 'Community' in str(headers):
                    neighborhood = home_facts[8].td.text
                else: neighborhood = 'NaN'
            elif 'Community' in str(headers):
                appliances = 'NaN'
                neighborhood = home_facts[7].td.text
            else: 
                appliances = 'NaN'
                neighborhood = 'NaN'
                amenities = 'NaN'
        elif 'Amenities' in str(headers):
            features = 'NaN'
            amenities = home_facts[6].td.text
            if 'Appliances' in str(headers):
                appliances = home_facts[7].td.text
                if 'Community' in str(headers):
                    neighborhood = home_facts[8].td.text
                else: 
                    neighborhood = 'NaN'
            elif 'Community' in str(headers):
                appliances = 'NaN'
                neighborhood = home_facts[7].td.text
            else: 
                neighborhood = 'NaN'
                appliances = 'NaN'
        elif 'Appliances' in str(headers):
            amenities = 'NaN'
            features = 'NaN'
            appliances = home_facts[6].td.text
            if 'Community' in str(headers):
                neighborhood = home_facts[7].td.text
            else: neighborhood = 'NaN'
        elif 'Community' in str(headers):
            amenities = 'NaN'
            features = 'NaN'
            appliances = 'NaN'
            neighborhood = home_facts[6].td.text
        else: 
            amenities = 'NaN'
            features = 'NaN'
            appliances = 'NaN'
            neighborhood = 'NaN'
            
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
                           amenities_list,
                           appliances_list,
                           neighborhood_list,
                           hyperlink
                          ))
    df = pd.DataFrame(list_of_str,columns=my_columns)
    return df  


def save_df(df,filename):
    df.to_csv(fr'/Users/veliristimaki/Downloads/data_scaping/{filename}.csv', index = False)
    
    
dataframe = make_detailed_df()
save_df(dataframe,'housing_pg1')
