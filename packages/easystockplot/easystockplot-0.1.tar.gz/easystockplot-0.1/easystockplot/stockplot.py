import datetime
import matplotlib.pyplot as plt
import seaborn as sns 
import yfinance as yf

# Define class of stock ploting
class StockPlot:
    def __init__(self, ticker, end_date=datetime.datetime.today().date(), days=365):
        '''
        ticker: str
            Ticker of the stock
        end_date: datetime.date
            End date of the stock data
        days: int
            Number of days of the stock data
        '''
        assert isinstance(ticker, str), 'ticker must be a string'
        assert isinstance(end_date, datetime.date), 'end_date must be a datetime.date object'
        assert isinstance(days, int), 'days must be an integer'
        
        self.ticker = ticker
        self.end_date = end_date
        self.start_date = end_date - datetime.timedelta(days=days)
    
    def get_stock_data(self):
        stock_data = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        return stock_data
    
    def plot_stock(self):
        stock_data = self.get_stock_data()
        # Plot the adjusted close price
        sns.lineplot(data=stock_data, x=stock_data.index, y=stock_data['Adj Close'], label = 'daily price', color = 'royalblue')
        # Plot the 30-day rolling average
        sns.lineplot(data=stock_data, x=stock_data.index, y=stock_data['Adj Close'].rolling(30).mean(), label = '30-day moving average', color = 'orangered')
        sns.despine()
        plt.ylabel(f'Adj Close Price (USD)')
        plt.xlabel(None)
        plt.title(f'{self.ticker} Stock Price ({self.start_date} - {self.end_date})')
        plt.legend()
        plt.show()

    def plot_stock_return(self):
        # Plot daily return for the stock
        stock_data = self.get_stock_data()
        sns.barplot(data=stock_data, x=stock_data.index, y=stock_data['Adj Close'].pct_change(), color = 'royalblue')
        plt.xticks(range(0, len(stock_data.index), 30), stock_data.index.date[::30], rotation=45)
        sns.despine()
        plt.ylabel(f'Daily Return')
        plt.xlabel(None)
        plt.title(f'{self.ticker} Stock Return ({self.start_date} - {self.end_date})')
        plt.show()


# Define class of stock statistics
# class StockStats:
#     # define constructor
#     def __init__(self, ticker, end_date=datetime.datetime.today().date(), days=365):
#         '''
#         ticker: str
#             Ticker of the stock
#         end_date: datetime.date
#             End date of the stock data
#         days: int
#             Number of days of the stock data
#         '''
#         assert isinstance(ticker, str), 'ticker must be a string'
#         assert isinstance(end_date, datetime.date), 'end_date must be a datetime.date object'
#         assert isinstance(days, int), 'days must be an integer'
#         self.ticker = ticker
#         self.end_date = end_date
#         self.start_date = end_date - datetime.timedelta(days=days)
    
#     # define function to get stock data
#     def get_stock_data(self):
#         stock_data = yf.download(self.ticker, start=self.start_date, end=self.end_date)
#         return stock_data
    
#     # define function to get stock statistics
#     def get_stock_stats(self):
#         # get stock data
#         stock_data = self.get_stock_data()
#         # get stock statistics
#         stock_stats = stock_data.describe()
#         return stock_stats
