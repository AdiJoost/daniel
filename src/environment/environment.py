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
        payout_fee (float): Transaction fee percentage applied to buy/sell actions.
    """
    
    def __init__(self, datastring, performance_ticker, payout_fee: float= 0.0) -> None:
        super().__init__(datastring, performance_ticker, payout_fee)

    def get_performance_of_today(self) -> float:
        date = pd.to_datetime(self.current_date)
        try:
            open_price = float(self.df_i.at[(date, self.performance_ticker), 'open'])
            close_price = float(self.df_i.at[(date, self.performance_ticker), 'close'])
            performance = (close_price - open_price) / open_price
            return performance
        except KeyError:
            raise KeyError(f"Performance ticker '{self.performance_ticker}' data not found for date '{date}'.")
    
    