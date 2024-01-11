import yfinance as yf
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from dataframe import getdata

# Fetch data using your getdata function
data = getdata()

# Filter data for Apple (AAPL)
aapl_data = data[data.index.get_level_values('ticker') == 'AAPL'].copy()  # Make sure to use .copy() to avoid the SettingWithCopyWarning

# Calculate Bollinger Bands for AAPL
aapl_data.loc[:, 'BBM'] = aapl_data['bbm'] 
aapl_data.loc[:, 'BBH'] = aapl_data['bbh'] 
aapl_data.loc[:, 'BBL'] = aapl_data['bbl'] 

# Plotting Bollinger Bands
plt.figure(figsize=(14, 7))
plt.title('Bollinger Bands for Apple (AAPL)')
plt.plot(aapl_data.index.get_level_values('date'), aapl_data['adj close'], label='Adj Close', color='blue')
plt.plot(aapl_data.index.get_level_values('date'), aapl_data['BBM'], label='Middle Band', color='black')
plt.plot(aapl_data.index.get_level_values('date'), aapl_data['BBH'], label='Upper Band', color='green')
plt.plot(aapl_data.index.get_level_values('date'), aapl_data['BBL'], label='Lower Band', color='red')
plt.legend(loc='best')
plt.xlabel('Date')
plt.ylabel('Price')
plt.grid(True)
plt.tight_layout()
plt.show()
