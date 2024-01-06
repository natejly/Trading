from pypfopt.efficient_frontier import EfficientFrontier 
from pypfopt import risk_models 
from pypfopt import expected_returns
import pandas as pd
import yfinance as yf
import numpy as np
from KmeanCluster import dofilter
from KmeanCluster import getdates
from dataframe import getdata
def optimize_weights (prices, lower_bound=0):
    returns = expected_returns.mean_historical_return(prices=prices,frequency=252)
    cov = risk_models.sample_cov (prices=prices, frequency=252)
    ef = EfficientFrontier(expected_returns=returns,cov_matrix=cov, weight_bounds=(lower_bound, .1), solver='SCS')
    weights = ef.max_sharpe()
    return ef. clean_weights()

data = getdata()
stocks = data.index.get_level_values('ticker').unique().tolist()
new_df = yf.download(tickers=stocks, start=data.index.get_level_values('date').unique()[0]-pd.DateOffset(months=12), 
                     end=data.index.get_level_values('date').unique()[-1])

fixed_dates = getdates(dofilter(data))

returns_dataframe = np.log(new_df['Adj Close']).diff()
portfolio_df = pd.DataFrame()
for start_date in fixed_dates.keys():
    end_date = (pd.to_datetime(start_date)+pd.offsets.MonthEnd(0)).strftime('%Y-%m-%d')
    cols = fixed_dates [start_date]
    optimization_start_date = (pd.to_datetime(start_date)-pd.DateOffset(months=12)).strftime('%Y-%m-%d')
    optimization_end_date = (pd.to_datetime(start_date)-pd.DateOffset(days=1)).strftime('%Y-%m-%d')

#weights = optimize_weights(prices, lower_bound=0 )
optimization_df = new_df[optimization_start_date:optimization_end_date]['Adj Close'][cols]
print(optimization_df)