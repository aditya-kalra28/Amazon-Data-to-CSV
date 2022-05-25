import re
from unicodedata import name
from bs4 import BeautifulSoup
import requests
from nltk.corpus import stopwords
from collections import Counter
from urllib.parse import urljoin
import pandas as pd

HEADERS = {
        'Host': 'www.amazon.in',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers'
    }

def product(URL,HEADERS):
    if URL=="":
        return None, None, None
    webpage = requests.get(URL, headers=HEADERS)
    parsed = BeautifulSoup(webpage.content, "html5lib")
    # print(parsed)
    # product_name = parsed.find("span", id='productTitle').string.strip()
    desc = parsed.select("#featurebullets_feature_div li")
    spans = parsed.select("#detailBullets_feature_div .a-list-item span")

    details = []
    for i in spans:
        str=i.text
        output = ''.join([i if i.isalnum() else ' ' for i in str])
        output = ' '.join(output.split())
        details.append(output)

    asin = ''
    manufacturer = ''
    for i in range(len(details)):
        if len(asin)>0 and len(manufacturer)>0:
            break
        if details[i]=="ASIN":
            asin = details[i+1]
        if details[i]=="Manufacturer":
            manufacturer = details[i+1]
    dess=[]
    for i in desc:
        dess.append(i.text.strip())            
    # print("Product Name: ", product_name,"\n\n")
    # print("\n\nASIN: ", asin)
    # print("\n\nManufacturer: ", manufacturer)
    # print("\n\n Details:", details)


    return asin, manufacturer, dess

df = pd.DataFrame(columns=['name', 'price', 'rating', 'number_of_rating', 'url',"asin", "manufacturer", "desc"])

url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
webpage = requests.get(url, headers=HEADERS)
parsed = BeautifulSoup(webpage.content, "html5lib")


cards = parsed.select(".s-card-container")
for  i in cards:

    u = i.select_one(".a-link-normal.s-no-outline")
    product_name = i.select_one("h2")
    price = i.select_one(".a-price .a-offscreen")
    rating_span = i.select(".a-size-small span")

    if len(rating_span)>4:
        rating = rating_span[0].get('aria-label')
        number_of_ratings = rating_span[3].get('aria-label')
    else:
        rating = ""
        number_of_ratings = ""

    if price==None:
        price=''
    else:
        price = price.text
    
    if u!=None:
        url = ("https://www.amazon.com" + u.get('href'))
    else:
        url = ""
    
    if product_name==None:
        product_name = ""
    else:
        product_name = product_name.text
    

    print(product_name)
    print(price)
    print(rating)
    print(number_of_ratings)
    asin, manufacturer,desc = product(url)

    df = df.append({"name": product_name,"price": price,"rating": rating, "number_of_rating": number_of_ratings,"url": url ,"asin":asin, "manufacturer": manufacturer, "desc":desc}, ignore_index=True)
print(df.head())
df.to_csv(r'C:/Users/Aditya Kalra/Desktop/product.csv', index=False)





