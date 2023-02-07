import pandas as pd
import urllib
from bs4 import BeautifulSoup
import requests
import time 
import datetime

basket = pd.read_excel('cpi_basket.xlsx')

i=0
item = basket.loc[i, 'Item']
search_URL = 'https://www.tesco.com/groceries/en-GB/search?'+urllib.parse.urlencode({'query':item})
URLout = 0

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}

# create page variable 
page = requests.get(search_URL, headers=headers)

#pull the page with bs4 
soup1 = BeautifulSoup(page.content, "html.parser")

#prettyfied version of soup1 = soup2
soup2 = BeautifulSoup(soup1.prettify(), "html.parser")
URLout = 'https://www.tesco.com' + soup2.find("a", {'class':'product-image-wrapper'})['href']

item = soup2.find_all("a", {'class':'product-image-wrapper'})[0]

item = 'bread rolls'
redundancy = 5


for i in range(redundancy):
    basket[f'Link_{i}']=None


for i in basket.index:
    item = basket.loc[i, 'Item']
    search_URL = 'https://www.tesco.com/groceries/en-GB/search?'+urllib.parse.urlencode({'query':item})
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}

    # create page variable 
    page = requests.get(search_URL, headers=headers)

    #pull the page with bs4 
    soup1 = BeautifulSoup(page.content, "html.parser")

    #prettyfied version of soup1 = soup2
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")
    URL = 'https://www.tesco.com'
    try:
        items = soup2.find_all("a", {'class':'product-image-wrapper'})
        for j in range(redundancy):
            try:
                link = items[j]['href']
                basket.loc[i, f'Link_{j}'] = URL + link
                print(basket.loc[i, 'Item'], f'item {j}', link)
            except:
                basket.loc[i, f'Link_{j}'] = None
                print(f'Could not find item {j}')
    except:
        #print(f'No links found for item {basket.loc[i, 'Item']}')
        pass

now = datetime.datetime.now()
current_time = now.strftime("%y%m%d_%H_%M_%S")
print("Current Time =", current_time)
basket.to_csv(f'dumps/dump_{current_time}.csv')

basket.to_csv('basket_redundancies.csv')