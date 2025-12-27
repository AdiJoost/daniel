from abc import ABC, abstractmethod
from datetime import date

from src.enums.price_points import PricePoints

class BaseEnvironment(ABC):

    @abstractmethod
    def load_data(self, datastring) -> None:
        """
        Load the data from the data folder
        :param datastring: Path to the data file
        :type datastring: str
        """
    
    @abstractmethod
    def set_current_date(self, to_date: date) -> None:
        """
        Sets the current date of the environment. to_date must be in range of the dataset date span

        :param to_date: The date to set the current date to
        :type to_date: date
        """

    @abstractmethod
    def set_next_date(self) -> None:
        """
        Sets the current date to the next date in the dataset
        """

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
    def get_current_price(self, ticker: str, price_point: PricePoints=PricePoints.OPEN) -> float:
        """
        Returns the current price of a ticker
        
        :param ticker: The ticker symbol to get the price for
        :type ticker: str
        :param price_point: The price point to retrieve (default is OPEN)
        :type price_point: PricePoints            
        """

    @abstractmethod
    def get_tickers(self) -> list:
        """
        Returns a list of all tickers in the dataset
        
        :return: List of ticker symbols
        """

    @abstractmethod
    def get_start_date(self) -> date:
        """
        Returns the start date of the dataset
        
        :return: Start date of the dataset
        """

    @abstractmethod
    def get_end_date(self) -> date:
        """
        Returns the end date of the dataset
        
        :return: End date of the dataset
        """

    @abstractmethod
    def get_current_date(self) -> date:
        """
        Returns the current date of the environment
        
        :return: Current date of the environment
        """

    @abstractmethod
    def get_performance_of_today(self) -> float:
        """
        Returns the performance of the performance ticker for the current date
        
        :return: Performance of the performance ticker for the current date
        """

    @abstractmethod
    def get_number_of_days(self) -> int:
        """
        Returns the total number of days in the dataset
        
        :return: Total number of days in the dataset
        """