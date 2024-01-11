import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from meanreversion import generate_signals, getdata  # Assuming you have a function to fetch data
from dataframe import get_spy  # Function to get S&P 500 stocks

def backtest_strategy(data, signals):
    data = data.copy()
    
    # Calculate daily returns
    data['daily_returns'] = data['adj close'].pct_change()
    
    data['position'] = np.nan
    data.loc[signals['Buy'], 'position'] = 1
    data.loc[signals['Sell'], 'position'] = 0
    data['position'] = data['position'].fillna(method='ffill')
    
    data['strategy_returns'] = data['position'].shift() * data['daily_returns']
    data['cumulative_strategy_returns'] = (1 + data['strategy_returns']).cumprod()
    data['cumulative_buy_hold_returns'] = (1 + data['daily_returns']).cumprod()
    
    return data[['daily_returns', 'strategy_returns', 'cumulative_strategy_returns', 'cumulative_buy_hold_returns']]

if __name__ == "__main__":
    sp500_symbols = get_spy()
    backtest_results_dict = {}
    data = getdata()  # Fetch your data; adjust accordingly

    cumulative_returns_dict = {}
    cumulative_returns_list = []

    for symbol in sp500_symbols:
        try:
            stock_data = data.loc[data.index.get_level_values('ticker') == symbol]
            
            if stock_data.empty:
                continue
            
            signals = generate_signals(stock_data)
            
            backtest_results = backtest_strategy(stock_data, signals)
            
            backtest_results_dict[symbol] = backtest_results
            cumulative_returns_list.append(backtest_results['cumulative_strategy_returns'].iloc[-1])
            
            cumulative_returns_dict[symbol] = backtest_results['cumulative_strategy_returns'].iloc[-1]
            
            print(f"Backtested strategy for {symbol}", end='\r')
        except Exception as e:
            print(f"Error processing {symbol}: {e}")

    sorted_stocks = sorted(cumulative_returns_dict.items(), key=lambda x: x[1], reverse=True)
    
    if cumulative_returns_list:
        average_cumulative_returns = sum(cumulative_returns_list) / len(cumulative_returns_list)
        print(f"\nAverage Cumulative Returns for All Stocks Combined: {average_cumulative_returns:.2f}")
    else:
        print("\nNo valid cumulative returns data available for calculation.")
    
    print("\nTop 10 Performing Stocks Trading Mean Reversion:")
    for rank, (symbol, cumulative_return) in enumerate(sorted_stocks[:10], 1):
        print(f"{rank}. {symbol}: {cumulative_return:.2f}")

    # Fetch S&P 500 data for comparison
    sp500_data = getdata()  # Fetch the S&P 500 data; adjust accordingly
    sp500_data['daily_returns'] = sp500_data['adj close'].pct_change()

    # Assuming an initial investment of $1 for both strategies
    initial_investment = 1

    # Calculate the cumulative dollar returns
    sample_symbol = next(iter(backtest_results_dict))  # Take the first symbol as a sample
    backtest_results_dict[sample_symbol].reset_index(drop=True, inplace=True)
    sp500_data.reset_index(drop=True, inplace=True)

    backtest_results_dict[sample_symbol]['cumulative_strategy_dollars'] = initial_investment * (1 + backtest_results_dict[sample_symbol]['strategy_returns']).cumprod()
    sp500_data['cumulative_sp500_dollars'] = initial_investment * (1 + sp500_data['daily_returns']).cumprod()

    # Plotting in dollar units
    # Plotting in dollar units using a line graph
plt.figure(figsize=(14, 7))

# Plotting the cumulative dollar returns for the strategy as a line
plt.plot(backtest_results_dict[sample_symbol]['cumulative_strategy_dollars'], label='Strategy Cumulative Dollar Returns', color='blue', linewidth=2)

# Plotting the cumulative dollar returns for the S&P 500 as a line
plt.plot(sp500_data['cumulative_sp500_dollars'], label='S&P 500 Cumulative Dollar Returns', color='green', linewidth=2)

# Adding title and labels
plt.title('Cumulative Dollar Returns: Strategy vs. S&P 500')
plt.xlabel('Date Index')
plt.ylabel('Cumulative Dollar Returns')

# Adding legend to distinguish the lines
plt.legend()

# Display grid for better readability
plt.grid(True)

# Adjust layout for better visualization
plt.tight_layout()

# Show the plot
plt.show()
