import pandas as pd
import numpy as np
from meanreversion import generate_signals, getdata  # Assuming you have a function to fetch data
from dataframe import get_spy  # Function to get S&P 500 stocks

def backtest_strategy(data, signals):
    """
    Backtest the trading strategy based on the generated signals.
    """
    # Create a copy of the data to avoid modifying the original dataframe
    data = data.copy()
    
    # Calculate daily returns
    data['daily_returns'] = data['adj close'].pct_change()
    
    # Initialize a column to store the strategy's position (1 for long, -1 for short, 0 for neutral)
    data['position'] = np.nan
    
    # Apply the buy and sell signals to set the positions
    data.loc[signals['Buy'], 'position'] = 1
    data.loc[signals['Sell'], 'position'] = 0
    
    # Forward fill the positions to represent holding the position until a new signal is generated
    data['position'] = data['position'].fillna(method='ffill')
    
    # Calculate strategy's daily returns based on the positions
    data['strategy_returns'] = data['position'].shift() * data['daily_returns']
    
    # Calculate cumulative returns
    data['cumulative_strategy_returns'] = (1 + data['strategy_returns']).cumprod()
    
    # Calculate benchmark (buy and hold strategy) cumulative returns
    data['cumulative_buy_hold_returns'] = (1 + data['daily_returns']).cumprod()
    
    return data[['strategy_returns', 'cumulative_strategy_returns', 'cumulative_buy_hold_returns']]

if __name__ == "__main__":
    # Get S&P 500 stocks
    sp500_symbols = get_spy()
    
    backtest_results_dict = {}
    
    data = getdata()
    
    cumulative_returns_dict = {}  # Dictionary to store cumulative returns for each stock
    cumulative_returns_list = []  # List to store cumulative returns for each stock

    # Loop through each stock symbol in S&P 500
    for symbol in sp500_symbols:
        try:
            stock_data = data.loc[data.index.get_level_values('ticker') == symbol]
            
            # Skip if data is insufficient or other errors occur
            if stock_data.empty:
                continue
            
            # Generate signals for the stock
            signals = generate_signals(stock_data)
            
            # Backtest the strategy for the stock
            backtest_results = backtest_strategy(stock_data, signals)
            
            # Store backtest results in dictionary
            backtest_results_dict[symbol] = backtest_results
            cumulative_returns_list.append(backtest_results['cumulative_strategy_returns'].iloc[-1])

            # Store the last cumulative return of the stock in the dictionary
            cumulative_returns_dict[symbol] = backtest_results['cumulative_strategy_returns'].iloc[-1]
            
            # Print progress
            print(f"Backtested strategy for {symbol}")
            
        except Exception as e:
            print(f"Error processing {symbol}: {e}")
    
    # Sort stocks based on cumulative returns in descending order
    sorted_stocks = sorted(cumulative_returns_dict.items(), key=lambda x: x[1], reverse=True)
    if cumulative_returns_list:
        average_cumulative_returns = sum(cumulative_returns_list) / len(cumulative_returns_list)
        print(f"\nAverage Cumulative Returns for All Stocks Combined: {average_cumulative_returns:.2f}")
    else:
        print("\nNo valid cumulative returns data available for calculation.")
    # Display top 10 performing stocks
    print("\nTop 10 Performing Stocks Trading Mean Reversion:")
    for rank, (symbol, cumulative_return) in enumerate(sorted_stocks[:10], 1):
        print(f"{rank}. {symbol}: {cumulative_return:.2f}")