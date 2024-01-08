import numpy as np
import pandas_ta as pta

def gkv(df):
    return ((np.log(df['high'])-np.log(df['low']))**2)/2 - (2*np.log(2)-1)*(np.log(df['adj close'])-np.log(df['open']))**2
def rsi(df):
    return df.groupby(level=1)['adj close'].transform(lambda ajc: pta.rsi(close=ajc, length=20))
def bbl(df):
    return df.groupby(level=1)['adj close'].transform(lambda ajc: pta.bbands(close=np.log1p(ajc), length=20).iloc[:,0])
def bbm(df):
    return df.groupby(level=1)['adj close'].transform(lambda ajc: pta.bbands(close=np.log1p(ajc), length=20).iloc[:,1])
def bbh(df):
    return df.groupby(level=1)['adj close'].transform(lambda ajc: pta.bbands(close=np.log1p(ajc), length=20).iloc[:,2])
def atr(df):
    atr = pta.atr(high=df['high'],low=df['low'],close=df['close'],length=14)
    return atr.sub(atr.mean()).div(atr.std())
def macd(close):
    macd = pta.macd(close=close, length=20).iloc[:,0]
    return macd.sub(macd.mean()).div(macd.std())
def dv(df):
    return (df['adj close']*df['volume'])/1000000