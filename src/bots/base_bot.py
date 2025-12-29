from abc import ABC, abstractmethod
from ast import List
from datetime import date

from src.enums.actions import Actions
from src.enums.price_points import PricePoints
from src.environment.base_environment import BaseEnvironment
from src.helpers.action_taken import ActionTaken
from src.helpers.history_entry import HistoryEntry

class BaseBot(ABC):

    def __init__(self, name: str, saving_path: str, environment: BaseEnvironment, updateQValues: bool = True, cash: float = 100000) -> None:
        self.name = name
        self.saving_path = saving_path
        self.environment = environment
        self.updateQValues = updateQValues
        self.cash = cash
        self.initial_cash = cash
        self.history: List[HistoryEntry] = []
        self.tickers = self.environment.get_tickers()
        self.portfolio = {ticker: 0 for ticker in self.tickers}
        self.setTodaysHistoryEntry()

    @abstractmethod
    def take_action(self) -> bool:
        """
        Decide on an action based on the current state of the environment. Then take that action.

        return True if the action was to end the day, otherwise False.
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
    def save_history(self, filename: str) -> None:
        """
        Saves the bot's history to the specified path.
        """

    @abstractmethod
    def load(self) -> None:
        """
        Loads the bot's state from the specified path.
        """

    def buy(self, ticker: str, amount: int) -> None:
        price, fee_paid = self.environment.buy(amount, ticker)
        if self.cash >= price:
            self.cash -= price
            self.portfolio[ticker] += amount
            action_taken = ActionTaken(
                action=Actions.BUY,
                amount=amount,
                money_transfered=price,
                ticker=ticker,
                fee_paid=fee_paid)
            self.todaysHistory.add_action_taken(action_taken)

    def sell(self, ticker, amount) -> None:
        price, fee_paid = self.environment.sell(amount, ticker)
        if self.portfolio[ticker] >= amount:
            self.cash += price
            self.portfolio[ticker] -= amount
            action_taken = ActionTaken(
                action=Actions.SELL,
                amount=amount,
                money_transfered=price,
                ticker=ticker,
                fee_paid=fee_paid
            )
            self.todaysHistory.add_action_taken(action_taken)

    def _get_state_string(self, states: list[int]) -> str:
        return ''.join([str(state) for state in states.values()])
    
    def end_day(self) -> None:
        action_taken = ActionTaken(
            action=Actions.END_DAY, 
            amount=0.0,
            money_transfered=0.0,
            ticker="-",
            fee_paid=0.0)
        self.todaysHistory.add_action_taken(action_taken)

        self.todaysHistory.set_cash_at_end(self.cash)
        portfolio_value = self.get_portfolio_value(price_point=PricePoints.CLOSE)
        self.todaysHistory.set_portfolio_value_at_end(portfolio_value)
        self.todaysHistory.calculate_alpha()
        self.todaysHistory.caluclate_total_gain()
        if self.updateQValues:
            self.learn()
        self.history.append(self.todaysHistory)
        self.environment.set_next_date()
        self.setTodaysHistoryEntry()

    def reset(self) -> None:
        self.cash = self.initial_cash
        self.portfolio = {ticker: 0 for ticker in self.tickers}
        self.environment.reset_environment()
        self.history = []
        self.environment.set_next_date()
        self.setTodaysHistoryEntry()

    def get_history_as_string(self) -> str:
        history_strings = []
        for entry in self.history:
            history_strings.append(str(entry))
        return "\n".join(history_strings)
    
    def setTodaysHistoryEntry(self) -> None:
        today: date= self.environment.get_current_date()
        cash_at_start = self.cash
        portfolio_value_at_start = self.get_portfolio_value(price_point=PricePoints.OPEN)
        sAndPPerformance = self.environment.get_performance_of_today()
        self.todaysHistory = HistoryEntry(today, portfolio_value_at_start, cash_at_start, sAndPPerformance, actions_taken=[])
    
    def get_portfolio_value(self, price_point: PricePoints=PricePoints.OPEN) -> float:
        total_value = 0.0
        for ticker, amount in self.portfolio.items():
            if amount > 0:
                price = self.environment.get_current_price(ticker, price_point=price_point)
                total_value += price * amount
        return total_value