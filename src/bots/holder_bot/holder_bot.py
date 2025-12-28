

from datetime import date
import itertools
import json
import math
import os
import random
from rpds import List
import pandas as pd
from config.rootPath import getRootPath
from src.bots.base_bot import BaseBot
from src.enums.actions import Actions
from src.enums.price_points import PricePoints
from src.environment.base_environment import BaseEnvironment
from src.environment.environment import Environment
from src.helpers.action_taken import ActionTaken
from src.helpers.history_entry import HistoryEntry


class HolderBot(BaseBot):

    def __init__(self, name: str, saving_path: str, environment: BaseEnvironment = None, updateQValues: bool = True, qStratRandom: bool = False, cash: float = 100000) -> None:
        self.environment = environment
        self._initValueActionAndStateTables()
        self.name = name
        self.history: List[HistoryEntry] = []
        self.cash = cash
        self.initial_cash = cash
        self.portfolio = {ticker: 0 for ticker in self.tickers}
        self.updateQValues = updateQValues
        self.qStratRandom = qStratRandom
        self.environment.set_next_date()
        self.setTodaysHistoryEntry()
        self.buy_initial_holdings()
        

    def _initValueActionAndStateTables(self) -> None:
        self.tickers = self.environment.get_tickers()

    def buy_initial_holdings(self) -> None:
        for ticker in self.tickers:
            max_price = self.cash / (len(self.tickers))
            current_price = self.environment.get_current_price(ticker, PricePoints.OPEN)
            amount = math.floor(max_price / current_price) if current_price > 0 else 0
            self.buy(ticker, int(amount))

    def take_action(self) -> bool:
        action_taken = ActionTaken(
            action=Actions.END_DAY,
            amount=0.0,
            money_transfered=0.0,
            ticker="-",
            fee_paid=0.0)
        self.todaysHistory.add_action_taken(action_taken)
        self.end_day()
        return True
    
    def _get_state_string(self, states: list[int]) -> str:
        return ''.join([str(state) for state in states.values()])

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
        """Holder Bot never sells"""
        pass

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

    def learn(self) -> None:
        """Holder Bot does not learn"""
        pass

    def test(self) -> None:
        pass

    def save(self) -> None:
        path = getRootPath().joinpath(f"data/holder_bot/{self.name}/environment.json")
        environment_json = self.environment.to_json()
        with open(path, "w") as f:
            json.dump(environment_json, f, indent=4)

    def save_history(self, saving_path) -> None:
        value =  [entry.to_json() for entry in self.history]
        path = getRootPath().joinpath(f"data/holder_bot/{self.name}/{saving_path}")
        os.makedirs(path.parent, exist_ok=True)
        with open(path, "w") as f:
            json.dump(value, f, indent=4)

    def load(self, saving_path: str) -> None:
        """Holder Bot does not load state action tables"""
        pass

    def get_portfolio_value(self, price_point: PricePoints=PricePoints.OPEN) -> float:
        total_value = 0.0
        for ticker, amount in self.portfolio.items():
            if amount > 0:
                price = self.environment.get_current_price(ticker, price_point=price_point)
                total_value += price * amount
        return total_value
    
    def setTodaysHistoryEntry(self) -> None:
        today: date= self.environment.get_current_date()
        cash_at_start = self.cash
        portfolio_value_at_start = self.get_portfolio_value(price_point=PricePoints.OPEN)
        sAndPPerformance = self.environment.get_performance_of_today()
        self.todaysHistory = HistoryEntry(today, portfolio_value_at_start, cash_at_start, sAndPPerformance, actions_taken=[])

    def get_history_as_string(self) -> str:
        history_strings = []
        for entry in self.history:
            history_strings.append(str(entry))
        return "\n".join(history_strings)
    
    def reset(self) -> None:
        self.cash = self.initial_cash
        self.portfolio = {ticker: 0 for ticker in self.tickers}
        self.environment.reset_environment()
        self.history = []
        self.environment.set_next_date()
        self.setTodaysHistoryEntry()