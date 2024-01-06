from pypfopt.efficient_frontier import EfficientFrontier 
from pypfopt import risk_models 
from pypfopt import expected_returns
import pandas as pd
import yfinance as yf
import numpy as np
from KmeanCluster import dofilter
from KmeanCluster import getdates
from dataframe import getdata
import matplotlib.pyplot as plt
def optimize_weights (prices, lower_bound=0):
    returns = expected_returns.mean_historical_return(prices=prices,frequency=252)
    cov = risk_models.sample_cov (prices=prices, frequency=252)
    ef = EfficientFrontier(expected_returns=returns,cov_matrix=cov, weight_bounds=(lower_bound, .1), solver='ECOS')
    weights = ef.max_sharpe()
    return ef.clean_weights()

def getportfolio(data):
    stocks = data.index.get_level_values('ticker').unique().tolist()
    new_df = yf.download(tickers=stocks, start=data.index.get_level_values('date').unique()[0]-pd.DateOffset(months=12), 
                        end=data.index.get_level_values('date').unique()[-1])


    returns_dataframe = np.log(new_df['Adj Close']).diff()
    portfolio_df = pd.DataFrame()
    fixed_dates = getdates(dofilter(data))
    for start_date in fixed_dates.keys():
        try: 
            end_date = (pd.to_datetime(start_date)+pd.offsets.MonthEnd(0)).strftime('%Y-%m-%d')
            cols = fixed_dates[start_date]
            optimization_start_date = (pd.to_datetime(start_date)-pd.DateOffset(months=12)).strftime('%Y-%m-%d')
            optimization_end_date = (pd.to_datetime(start_date)-pd.DateOffset(days=1)).strftime('%Y-%m-%d')
            optimization_df = new_df[optimization_start_date:optimization_end_date]['Adj Close'][cols] #?????
            success = False
            try:
                weights = optimize_weights(optimization_df, lower_bound=round(1/(len(optimization_df.columns)*2),3))
                weights = pd.DataFrame(weights, index=pd.Series(0))
                success = True
            except:
                print(f'Max Sharpe Optimization failed for {start_date}, using equal weights')
            if not success:
                weights = pd.DataFrame([1/len(optimization_df.columns) for x in range(len(optimization_df.columns))],
                                    index=optimization_df.columns.tolist(),
                                    columns=pd.Series(0)).T
            temp_df = returns_dataframe[start_date:end_date]
            temp_df = temp_df.stack().to_frame('return').reset_index(level=0).merge(weights.stack().to_frame('weight').reset_index(level=0,drop=True), 
                                                                                    left_index=True,
                                                                                    right_index=True)\
                                                        .reset_index().set_index(['Date', 'index']).unstack().stack()
            temp_df.index.names = ['date', 'ticker']
            temp_df['weighted_return'] = temp_df['return']*temp_df['weight']
            temp_df = temp_df.groupby(level=0)['weighted_return'].sum().to_frame('Strategy Return')
            portfolio_df = pd.concat([portfolio_df, temp_df], axis=0)
        except Exception as e:
            print(e)


    portfolio_df = portfolio_df.drop_duplicates()
    return portfolio_df
