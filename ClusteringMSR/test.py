import yfinance as yf
import matplotlib.pyplot as plt

def calculate_cumulative_percent_change():
    # Fetch historical data for SPY (S&P 500 ETF)
    ticker_symbol = 'SPY'
    start_date = '2019-01-08'  # 5 years from the current date
    end_date = '2024-01-08'
    
    spy_data = yf.download(tickers=ticker_symbol, start=start_date, end=end_date)
    
    # Calculate the daily percentage change
    spy_data['Daily_Percent_Change'] = spy_data['Adj Close'].pct_change() * 100
    
    # Calculate the cumulative percentage change
    spy_data['Cumulative_Percent_Change'] = (1 + spy_data['Daily_Percent_Change'] / 100).cumprod() - 1
    
    return spy_data['Cumulative_Percent_Change']

def plot_cumulative_percent_change(cumulative_percent_change):
    plt.figure(figsize=(14, 7))
    cumulative_percent_change.plot(color='b', alpha=0.7)
    
    plt.title('Cumulative Percentage Change of SPY Over the Past 5 Years')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Percentage Change (%)')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    cumulative_percent_change = calculate_cumulative_percent_change()
    
    # Plot the cumulative percentage change
    plot_cumulative_percent_change(cumulative_percent_change)
