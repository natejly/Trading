import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import yfinance as yf
import datetime
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import indicators
def get_spy():
    url = 'https://www.slickcharts.com/sp500'
    request = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = bs(request.text, "lxml")
    
    stats = soup.find('table', class_='table table-hover table-borderless table-sm')
    df = pd.read_html(str(stats))[0]
    
    # Assuming the tickers are in a column named 'Symbol'. Adjust if the column name is different.
    symbols_list = df['Symbol'].tolist()
    
    # Replace periods with hyphens for each ticker symbol
    symbols_list_with_hyphens = [symbol.replace('.', '-') for symbol in symbols_list]
    
    return symbols_list_with_hyphens


end_date = '2023-09-27'
start_date = pd.to_datetime(end_date)-pd.DateOffset(365*8)

df = yf.download(tickers=get_spy(),start=start_date,end=end_date).stack()
df.index.names = ['date', 'ticker']
df.columns = df.columns.str.lower()
df['gkv'] = indicators.gkv(df)
df['rsi'] = indicators.rsi(df)
df['bbl'] = indicators.bbl(df)
df['bbm'] = indicators.bbm(df)
df['bbh'] = indicators.bbh(df)
print(df)