import matplotlib.pyplot as plt
import numpy as np
from dataframe import getdata
from weightedreturns import getportfolio
import datetime as dt
import yfinance as yf
import numpy as np
portfolio_df = getportfolio(getdata())
spy = yf.download(tickers='SPY',
                  start='2015-01-01',
                  end=dt.date.today()
                  )
spy_ret = np.log(spy[['Adj Close']]).diff().dropna().rename({'Adj Close':'S&P 500'}, axis=1)

portfolio_df = portfolio_df.merge(spy_ret, left_index=True, right_index=True)
plt.style.use('ggplot')

portfolio_cum = np.exp(np.log1p(portfolio_df).cumsum())

portfolio_cum.plot(figsize=(16,6))
plt.show()