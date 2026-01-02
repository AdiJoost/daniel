from abc import ABC, abstractmethod
from datetime import date

import pandas as pd

from src.enums.price_points import PricePoints

class BaseEnvironment(ABC):
    

    def __init__(self, datastring, performance_ticker, payout_fee: float= 0.0) -> None:
        self.datastring = datastring
        self.performance_ticker = performance_ticker
        self.PAYOUT_FEE = payout_fee
        self.load_data(datastring)

    @abstractmethod
    def get_performance_of_today(self) -> float:
        """
        Returns the performance of the performance ticker for the current date
        
        :return: Performance of the performance ticker for the current date
        """

    def load_data(self, datastring) -> None:
        """
        Load the data from the data folder
        :param datastring: Path to the data file
        :type datastring: str
        """
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
    
    def set_current_date(self, to_date: date) -> None:
        """
        Sets the current date of the environment. to_date must be in range of the dataset date span

        :param to_date: The date to set the current date to
        :type to_date: date
        """
        self.current_date = pd.to_datetime(to_date)

    def set_next_date(self) -> None:
        """
        Sets the current date to the next date in the dataset
        """
        try:
            current_index = self.current_dates.index(pd.to_datetime(self.current_date))
        except ValueError:
            raise ValueError(f'Current date {self.current_date} not present in dataset')

        if current_index + 1 < len(self.current_dates):
            self.current_date = self.current_dates[current_index + 1]
        else:
            raise IndexError(f"No next date available in the dataset. Current date: {self.current_date}")

    def buy(self, amount: float, ticker: str, price_point: PricePoints=PricePoints.OPEN) -> tuple[float, float]:
        """
        Buy amount of a ticker. Returns costs of buying including fees and the fee paid

        :param amount: The amount of the ticker to buy
        :type amount: float
        :param ticker: The ticker symbol to buy
        :type ticker: str
        :param price_point: The price point to use for buying (default is OPEN)
        :type price_point: PricePoints
        """
        price = self.get_current_price(ticker, price_point)
        fee = amount * price * self.PAYOUT_FEE
        return (amount * price * (1 + self.PAYOUT_FEE), fee)

    def sell(self, amount: float, ticker: str, price_point: PricePoints=PricePoints.OPEN) -> tuple[float, float]:
        """
        Sell amount of a ticker. Returns revenue of selling after fees and the fee paid

        :param amount: The amount of the ticker to sell
        :type amount: float
        :param ticker: The ticker symbol to sell
        :type ticker: str
        :param price_point: The price point to use for selling (default is OPEN)
        :type price_point: PricePoints
        """
        price = self.get_current_price(ticker, price_point)
        fee = amount * price * self.PAYOUT_FEE
        return (amount * price * (1 - self.PAYOUT_FEE), fee)

    def get_current_price(self, ticker: str, price_point: PricePoints=PricePoints.OPEN) -> float:
        """
        Returns the current price of a ticker
        
        :param ticker: The ticker symbol to get the price for
        :type ticker: str
        :param price_point: The price point to retrieve (default is OPEN)
        :type price_point: PricePoints            
        """
        date = pd.to_datetime(self.current_date)

        try:
            if price_point.value in self.df_i.columns:
                return float(self.df_i.at[(date, ticker), price_point.value])
        except KeyError:
            raise KeyError(f"Price for ticker '{ticker}' on date '{date}' not found.")

        raise KeyError(f"Ticker column not found for {ticker}")

    def get_tickers_change(self) -> dict:
        """
        Returns a dictionary with the change in price for each ticker from the previous day to the current day
        
        :return: Dictionary with ticker symbols as keys and their price change as values
        """
        date = pd.to_datetime(self.current_date)
        previous_date_index = self.current_dates.index(date) - 1
        if previous_date_index < 0:
            raise IndexError(f"No previous date available in the dataset for date '{date}'.")

        previous_date = self.current_dates[previous_date_index]
        tickers = self.get_tickers()
        changes = {}

        for ticker in tickers:
            try:
                current_close = float(self.df_i.at[(date, ticker), 'open'])
                previous_close = float(self.df_i.at[(previous_date, ticker), 'open'])
                changes[ticker] = 1 if current_close - previous_close > 0 else 0
            except KeyError:
                changes[ticker] = 0

        return changes

    def get_tickers(self) -> list:
        """
        Returns a list of all tickers in the dataset
        
        :return: List of ticker symbols
        """
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

    def reset_environment(self) -> None:
        """
        Resets the environment to the initial state
        """
        self.current_date = pd.to_datetime(self.df['date'].min())

    def to_json(self) -> dict:
        """
        Returns a JSON representation of the environment
        
        :return: JSON representation of the environment
        """
        return {
            "datastring": self.datastring,
            "performance_ticker": self.performance_ticker,
            "payout_fee": self.PAYOUT_FEE,
            "class_name": self.__class__.__name__
        }