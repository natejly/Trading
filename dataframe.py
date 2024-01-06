import yfinance as yf
import datetime
import pandas as pd
import indicators
from statsmodels.regression.rolling import RollingOLS
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import statsmodels.api as sm
from spy import get_spy
def getdata():
    end_date = '2023-09-27' #date used in yt video
    start_date = pd.to_datetime(end_date)-pd.DateOffset(365*8)

    df = yf.download(tickers=get_spy(),start=start_date,end=end_date).stack()
    df.index.names = ['date', 'ticker']
    df.columns = df.columns.str.lower()
    df['gkv'] = indicators.gkv(df)
    df['rsi'] = indicators.rsi(df)
    df['bbl'] = indicators.bbl(df)
    df['bbm'] = indicators.bbm(df)
    df['bbh'] = indicators.bbh(df)
    df['atr'] = df.groupby(level=1, group_keys=False).apply(indicators.atr)
    df['macd'] = df.groupby(level=1, group_keys=False)['adj close'].apply(indicators.macd)
    df['dv'] = indicators.dv(df)

    lcols = [c for c in df.columns.unique(0) if c not in ['dv', 'volume', 'open', 'high', 'low', 'close']]

    data = (pd.concat([df.unstack('ticker')['dv'].resample('M').mean().stack('ticker').to_frame('dv'), #can change resample to D
            df.unstack()[lcols].resample('M').last().stack('ticker')],axis=1)).dropna()

    data.sort_index(inplace=True)

    data['dv'] = (data.loc[:, 'dv'].unstack('ticker').rolling(5 * 12, min_periods=12).mean().stack())
    data['dv_rank'] = (data.groupby('date')['dv'].rank(ascending=False))
    data = data[data['dv_rank']<150].drop(['dv','dv_rank'], axis=1) #take top
    def returns(df):
        oc = 0.005
        months = [1, 2, 3, 6, 9, 12]

        for month in months:
            df[f'return_{month}m'] = (df['adj close']
                                    .pct_change(month)
                                    .pipe(lambda x: x.clip(lower=x.quantile(oc),
                                                        upper=x.quantile(1-oc)))
                                    .add(1)
                                    .pow(1/month)
                                    .sub(1))
        return df
    data = data.groupby(level=1, group_keys=False).apply(returns).dropna()
    famaFrench = web.DataReader('F-F_Research_Data_5_Factors_2x3','famafrench',start='2010-01-01')[0].drop('RF', axis=1)
    famaFrench.index = famaFrench.index.to_timestamp()
    famaFrench = famaFrench.resample('M').last().div(100)
    famaFrench.index.name = 'date'
    famaFrench = famaFrench.join(data['return_1m']).sort_index()
    obs = famaFrench.groupby(level=1).size()
    validStocks = obs[obs >= 10]
    famaFrench = famaFrench[famaFrench.index.get_level_values('ticker').isin(validStocks.index)]

    #54:50 check 
    betas = (famaFrench.groupby(level=1,
                                group_keys=False)
            .apply(lambda x: RollingOLS(endog=x['return_1m'],
                                        exog=sm.add_constant(x.drop('return_1m', axis=1)),
                                        window=min(24, x.shape[0]),
                                        min_nobs=len(x.columns)+1)
            .fit(params_only=True)
            .params
            .drop('const', axis=1)
                                        ))
    factors = ['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']
    data = data.join(betas.groupby('ticker').shift())
    data.loc[:,factors] = data.groupby('ticker', group_keys=False)[factors].apply(lambda x: x.fillna(x.mean()))
    data = data.dropna()
    data = data.drop('adj close',axis=1)
    return data

