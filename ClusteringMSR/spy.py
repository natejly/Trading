#find better method other than scraping 
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
def get_spy():
    url = 'https://www.slickcharts.com/sp500'
    request = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = bs(request.text, "lxml")
    
    stats = soup.find('table', class_='table table-hover table-borderless table-sm')
    df = pd.read_html(str(stats))[0]
    
    symbols_list = df['Symbol'].tolist()
    
    symbols_list_with_hyphens = [symbol.replace('.', '-') for symbol in symbols_list]
    symbols_list_with_hyphens = [symbol for symbol in symbols_list_with_hyphens if symbol != 'VLTO']

    return symbols_list_with_hyphens
