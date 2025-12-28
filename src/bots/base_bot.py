from abc import ABC, abstractmethod

class BaseBot(ABC):

    @abstractmethod
    def take_action(self) -> bool:
        """
        Decide on an action based on the current state of the environment. Then take that action.

        return True if the action was to end the day, otherwise False.
        """

    @abstractmethod
    def buy(self, ticker: str, amount: int) -> None:
        """
        Buys a specified amount of the given ticker.
        
        :param ticker: The ticker symbol to buy.
        :type ticker: str
        :param amount: The amount of the ticker to buy.
        :type amount: int
        """

    @abstractmethod
    def sell(self, ticker: str, amount: int) -> None:
        """
        Sells a specified amount of the given ticker.

        :param ticker: The ticker symbol to sell.
        :type ticker: str
        :param amount: The amount of the ticker to sell.
        :type amount: int
        """

    @abstractmethod
    def end_day(self) -> None:
        """
        Ends the current trading day, performing any necessary wrap-up actions.
        """

    @abstractmethod
    def learn(self, itterations: int= 1) -> None:
        """
        Learns from past actions to improve future decisions.

        :param itterations: The number of iterations to learn from.
        :type itterations: int
        """

    @abstractmethod
    def test(self) -> None:
        """
        Tests the bot's performance on the last days of the environment.
        """

    @abstractmethod
    def save(self) -> None:
        """
        Saves the bot's state to the specified path.
        """

    @abstractmethod
    def save_history(self, saving_path: str) -> None:
        """
        Saves the bot's history to the specified path.

        :param saving_path: The path to save the bot's history.
        :type saving_path: str
        """

    @abstractmethod
    def load(self, saving_path: str) -> None:
        """
        Loads the bot's state from the specified path.

        :param saving_path: The path to load the bot's state.
        :type saving_path: str
        """

    @abstractmethod
    def reset(self) -> None:
        """
        Resets the bot to its initial state.
        """