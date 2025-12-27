from datetime import date
from src.enums.price_points import PricePoints
from src.environment.base_environment import BaseEnvironment
import pandas as pd

class Environment(BaseEnvironment):
    """
    Represents a trading environment using historical stock data from a CSV file.

    Args:
        datastring (str): Path to the CSV file containing historical stock data.
        performance_ticker (str): Ticker symbol used for performance comparison (e.g., S&P 500).
    """

    PAYOUT_FEE = 0.001
    
    def __init__(self, datastring, performance_ticker) -> None:
        super().__init__()
        self.load_data(datastring)
        self.performance_ticker = performance_ticker

    def load_data(self, datastring) -> None:
        self.df = pd.read_csv(datastring)
        if 'date' not in self.df.columns:
            raise ValueError('Input CSV must contain a "date" column')

        self.df['date'] = pd.to_datetime(self.df['date'])
        if 'ticker' in self.df.columns:
            self.df_i = self.df.set_index(['date', 'ticker']).sort_index()
        else:
            raise ValueError('Input CSV must contain a "ticker" column')

        self.current_date = pd.to_datetime(self.df['date'].min())

        self.current_dates = sorted(pd.DatetimeIndex(self.df['date'].unique()))
    
    def set_current_date(self, to_date) -> None:
        self.current_date = pd.to_datetime(to_date)

    def set_next_date(self) -> None:
        try:
            current_index = self.current_dates.index(pd.to_datetime(self.current_date))
        except ValueError:
            raise ValueError(f'Current date {self.current_date} not present in dataset')

        if current_index + 1 < len(self.current_dates):
            self.current_date = self.current_dates[current_index + 1]
        else:
            raise IndexError(f"No next date available in the dataset. Current date: {self.current_date}")

    def buy(self, amount: float, ticker: str, price_point: PricePoints=PricePoints.OPEN) -> tuple[float, float]:
        """Returns the total cost including payout fee and the fee paid."""
        price = self.get_current_price(ticker, price_point)
        fee = amount * price * self.PAYOUT_FEE
        return (amount * price * (1 + self.PAYOUT_FEE), fee)

    def sell(self, amount: float, ticker: str, price_point: PricePoints=PricePoints.OPEN) -> tuple[float, float]:
        """Returns the total revenue after deducting payout fee and the fee paid."""
        price = self.get_current_price(ticker, price_point)
        fee = amount * price * self.PAYOUT_FEE
        return (amount * price * (1 - self.PAYOUT_FEE), fee)

    def get_current_price(self, ticker: str, price_point: PricePoints=PricePoints.OPEN) -> float:
        date = pd.to_datetime(self.current_date)

        try:
            if price_point.value in self.df_i.columns:
                return float(self.df_i.at[(date, ticker), price_point.value])
        except KeyError:
            raise KeyError(f"Price for ticker '{ticker}' on date '{date}' not found.")

        raise KeyError(f"Ticker column not found for {ticker}")
    
    def get_tickers(self) -> list:
        tickers = sorted(self.df['ticker'].unique().tolist())
        try:
            tickers.remove(self.performance_ticker)
        except:
            pass
        return tickers

    def get_start_date(self) -> date:
        return pd.to_datetime(self.df['date'].min())

    def get_end_date(self) -> date:
        return pd.to_datetime(self.df['date'].max())
    
    def get_performance_of_today(self) -> float:
        date = pd.to_datetime(self.current_date)
        try:
            open_price = float(self.df_i.at[(date, self.performance_ticker), 'open'])
            close_price = float(self.df_i.at[(date, self.performance_ticker), 'close'])
            performance = (close_price - open_price) / open_price
            return performance
        except KeyError:
            raise KeyError(f"Performance ticker '{self.performance_ticker}' data not found for date '{date}'.")
    
    def get_current_date(self) -> date:
        """
        Returns the current date of the environment

        :return: Current date of the environment
        """
        return self.current_date
    
    def get_number_of_days(self) -> int:
        """
        Returns the total number of days in the dataset

        :return: Total number of days in the dataset
        """
        return len(self.current_dates)