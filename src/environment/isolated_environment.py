from datetime import date
from src.enums.price_points import PricePoints
from src.environment.base_environment import BaseEnvironment
import pandas as pd

class IsolatedEnvironment(BaseEnvironment):
    """
    Represents a trading environment using historical stock data from a CSV file.

    Args:
        datastring (str): Path to the CSV file containing historical stock data.
        performance_ticker (str): Ticker symbol used for performance comparison (e.g., S&P 500).
    """
    
    def __init__(self, datastring, performance_ticker, payout_fee: float= 0.0) -> None:
        super().__init__()
        self.datastring = datastring
        self.load_data(datastring)
        self.performance_ticker = performance_ticker
        self.PAYOUT_FEE = payout_fee

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
    
    def get_tickers_change(self) -> dict:
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
        performance = 0.0
        for ticker in self.get_tickers():
            if ticker == self.performance_ticker:
                continue
            try:
                open_price = float(self.df_i.at[(date, ticker), 'open'])
                close_price = float(self.df_i.at[(date, ticker), 'close'])
                performance += (close_price - open_price) / open_price
            except KeyError:
                raise KeyError(f"Performance ticker '{ticker}' data not found for date '{date}'.")
        return performance / (len(self.get_tickers()) - 1)
    
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
        self.current_date = pd.to_datetime(self.df['date'].min())

    def to_json(self):
        return {
            "datastring": self.datastring,
            "performance_ticker": self.performance_ticker,
            "PAYOUT_FEE": self.PAYOUT_FEE,
            "class_name": "IsolatedEnvironment"
        }