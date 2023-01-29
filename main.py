from bs4 import BeautifulSoup
import requests
import time 
import datetime
import pandas as pd


#Connect to WebSite
URL = "https://www.tesco.com/groceries/en-GB/products/255810019?selectedUrl=https://digitalcontent.api.tesco.com/v2/media/ghs/b1abfc12-9d21-4d66-a4e3-55ea706ddfbb/6b0aa485-2ba2-483f-9e2b-60b867051641.jpeg?h=540&w=540&preservedReferrer=https://www.tesco.com/"

def get_item_from_URL(URL):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}

    # create page variable 
    page = requests.get(URL, headers=headers)

    #pull the page with bs4 
    soup1 = BeautifulSoup(page.content, "html.parser")

    #prettyfied version of soup1 = soup2
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    #collect Title and Price 
    title = soup2.find("h1", {"class": "product-details-tile__title"}).get_text()
    price = soup2.find("span", {"class": "value"}).get_text()

    price = price.replace('\n','').replace(' ','')
    title = title.replace('\n','').strip(' ')

    #print the Data  
    print(title)
    print(price)
    return title, price


basket = pd.read_excel('basket_first_pick.xlsx', sheet_name = 'data')

for i in basket.index:
    URL = basket.loc[i, 'Link']
    try:
        title, price = get_item_from_URL(URL)
        basket.loc[i, 'Quoted title'] = title
        basket.loc[i, 'Price'] = price
    except:
        print('failed' , basket.loc[i, 'Item'], basket.loc[i, 'Link'])
        

now = datetime.datetime.now()
current_time = now.strftime("%y%m%d_%H_%M_%S")
print("Current Time =", current_time)


basket.to_csv(f'dumps/dump_{current_time}.csv')



