import yfinance as yf
import datetime as dt
import pandas as pd
from statsmodels.regression.rolling import RollingOLS
import pandas_datareader.data as web
import statsmodels.api as sm
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import numpy as np
import pandas_ta as pta
import os
from io import StringIO

def get_spy():
    url = 'https://www.slickcharts.com/sp500'
    request = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = bs(request.text, "lxml")
    
    stats = soup.find('table', class_='table table-hover table-borderless table-sm')
    df = pd.read_html(StringIO(str(stats)))[0]

    
    symbols_list = df['Symbol'].tolist()
    
    symbols_list_with_hyphens = [symbol.replace('.', '-') for symbol in symbols_list]
    symbols_list_with_hyphens = [symbol for symbol in symbols_list_with_hyphens if symbol != 'VLTO']

    return symbols_list_with_hyphens

def gkv(df):
    return ((np.log(df['high'])-np.log(df['low']))**2)/2 - (2*np.log(2)-1)*(np.log(df['adj close'])-np.log(df['open']))**2

def rsi(df):
    return df.groupby(level=1)['adj close'].transform(lambda ajc: pta.rsi(close=ajc, length=20))

def bbl(df):
    return df.groupby(level=1)['adj close'].transform(lambda ajc: pta.bbands(close=ajc, length=20).iloc[:,0])

def bbm(df):
    return df.groupby(level=1)['adj close'].transform(lambda ajc: pta.bbands(close=ajc, length=20).iloc[:,1])

def bbh(df):
    return df.groupby(level=1)['adj close'].transform(lambda ajc: pta.bbands(close=ajc, length=20).iloc[:,2])

def atr(df):
    atr = pta.atr(high=df['high'],low=df['low'],close=df['close'],length=14)
    return atr.sub(atr.mean()).div(atr.std())

def macd(close):
    macd = pta.macd(close=close, length=20).iloc[:,0]
    return macd.sub(macd.mean()).div(macd.std())

def dv(df):
    return (df['adj close']*df['volume'])/1000000

def getdata():
    if os.path.exists('data' + str(dt.date.today())+'.pickle'):
        print('dataframe already exists loading')
        return pd.read_pickle(f"data{dt.date.today()}.pickle")
    print('downloading...')
    end_date = dt.date.today()

    start_date = pd.to_datetime(end_date)-pd.DateOffset(365*5)

    df = yf.download(tickers=get_spy(),start=start_date,end=end_date).stack()
    
    df.index.names = ['date', 'ticker']
    df.columns = df.columns.str.lower()
    df.loc[:,'gkv'] = gkv(df)
    df.loc[:,'rsi'] = rsi(df)
    df.loc[:,'bbl'] = bbl(df)
    df.loc[:,'bbm'] = bbm(df)
    df.loc[:,'bbh'] = bbh(df)
    df.loc[:,'atr'] = df.groupby(level=1, group_keys=False).apply(atr)
    df.loc[:,'macd'] = df.groupby(level=1, group_keys=False)['adj close'].apply(macd)
    df.loc[:,'dv'] = dv(df)

    lcols = [c for c in df.columns.unique(0) if c not in ['dv', 'volume', 'open', 'high', 'low', 'close']]

    data = (pd.concat([df.unstack('ticker')['dv'].resample('D').mean().stack('ticker').to_frame('dv'), #can change resample to D
            df.unstack()[lcols].resample('D').last().stack('ticker')],axis=1)).dropna()

    data.sort_index(inplace=True)

    # data['dv'] = (data.loc[:, 'dv'].unstack('ticker').rolling(5 * 12, min_periods=12).mean().stack())
    # data['dv_rank'] = (data.groupby('date')['dv'].rank(ascending=False))
    # data = data[data['dv_rank']<150].drop(['dv','dv_rank'], axis=1) #take top
    # def returns(df):
    #     oc = 0.005
    #     months = [1, 2, 3, 6, 9, 12]

    #     for month in months:
    #         df[f'return_{month}m'] = (df['adj close']
    #                                 .pct_change(month)
    #                                 .pipe(lambda x: x.clip(lower=x.quantile(oc),
    #                                                     upper=x.quantile(1-oc)))
    #                                 .add(1)
    #                                 .pow(1/month)
    #                                 .sub(1))
    #     return df
    # data = data.groupby(level=1, group_keys=False).apply(returns).dropna()
    # famaFrench = web.DataReader('F-F_Research_Data_5_Factors_2x3','famafrench',start='2010-01-01')[0].drop('RF', axis=1)
    # famaFrench.index = famaFrench.index.to_timestamp()
    # famaFrench = famaFrench.resample('D').last().div(100)
    # famaFrench.index.name = 'date'
    # famaFrench = famaFrench.join(data['return_1m']).sort_index()
    # obs = famaFrench.groupby(level=1).size()
    # validStocks = obs[obs >= 10]
    # famaFrench = famaFrench[famaFrench.index.get_level_values('ticker').isin(validStocks.index)]

    # #54:50 check 
    # betas = (famaFrench.groupby(level=1,
    #                             group_keys=False)
    #         .apply(lambda x: RollingOLS(endog=x['return_1m'],
    #                                     exog=sm.add_constant(x.drop('return_1m', axis=1)),
    #                                     window=min(24, x.shape[0]),
    #                                     min_nobs=len(x.columns)+1)
    #         .fit(params_only=True)
    #         .params
    #         .drop('const', axis=1)
    #                                     ))
    # factors = ['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']
    # data = data.join(betas.groupby('ticker').shift())
    # data.loc[:,factors] = data.groupby('ticker', group_keys=False)[factors].apply(lambda x: x.fillna(x.mean()))
    data = data.dropna()
    data.to_pickle('data' + str(dt.date.today())+'.pickle')
    return data

if __name__ == "__main__":

    print((getdata()))
    