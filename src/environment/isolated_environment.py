from datetime import date
from src.enums.price_points import PricePoints
from src.environment.base_environment import BaseEnvironment
import pandas as pd

class IsolatedEnvironment(BaseEnvironment):
    """
    Represents a trading environment using historical stock data from a CSV file.

    Args:
        datastring (str): Path to the CSV file containing historical stock data.
        performance_ticker (str): Ticker symbol that would be used as performance check, but here is only give, so the environment does not allow trading with it. The performance is calculated as the average performance of all other tickers.
        payout_fee (float): Transaction fee percentage applied to buy/sell actions.
    """
    
    def __init__(self, datastring, performance_ticker, payout_fee: float= 0.0) -> None:
        super().__init__(datastring, performance_ticker, payout_fee)

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
