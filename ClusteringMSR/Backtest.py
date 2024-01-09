import matplotlib.pyplot as plt
import numpy as np
from dataframe import getdata  # Assuming this is a custom module you have for fetching data
from msrweights import getportfolio  # Assuming this is a custom module for portfolio allocation
import datetime as dt
import yfinance as yf

# Get portfolio returns
portfolio_df = getportfolio(getdata())

# Define start and end dates for the 5-year period
end_date = dt.date.today()
start_date = '2019-01-08'  # 5 years ago

# Download S&P 500 data for the 5-year period
spy = yf.download(tickers='SPY', start=start_date, end=end_date)

# Calculate daily percent returns for the S&P 500
spy['S&P 500 Daily Returns'] = spy['Adj Close'].pct_change().dropna()

# Compute cumulative returns for the S&P 500 over the 5-year period
cumulative_return_spy = (1 + spy['S&P 500 Daily Returns']).prod() - 1

total_return_percent = cumulative_return_spy * 100

print(f"S&P 500 total returns: {cumulative_return_spy * 100:.2f}%")

# Merge the S&P 500 returns with portfolio returns
portfolio_df = portfolio_df.merge(spy[['S&P 500 Daily Returns']], left_index=True, right_index=True)

# Calculate cumulative returns for portfolio and S&P 500
portfolio_df['Portfolio Cumulative Returns '] = (1 + portfolio_df['PovertySimulator Algorithm TM pending']).cumprod() - 1
portfolio_df['S&P 500 Cumulative Returns '] = (1 + portfolio_df['S&P 500 Daily Returns']).cumprod() - 1

# Calculate the difference in cumulative returns between portfolio and S&P 500
portfolio_df['Difference '] = portfolio_df['Portfolio Cumulative Returns '] - portfolio_df['S&P 500 Cumulative Returns ']

# Print the DataFrame for inspection
print(portfolio_df)

# Plotting
plt.style.use('ggplot')
portfolio_df[['Portfolio Cumulative Returns ', 'S&P 500 Cumulative Returns ', 'Difference ']].plot(figsize=(16, 6))

plt.title('Cumulative Percent Returns Comparison')
plt.xlabel('Date')
plt.ylabel('Cumulative Percent Returns ')

plt.legend(loc='upper left')
plt.show()
