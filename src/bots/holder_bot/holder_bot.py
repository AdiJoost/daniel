

from datetime import date
import itertools
import json
import math
import os
import random
from typing import override
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

    def __init__(self, name: str, saving_path: str, environment: BaseEnvironment = None, cash: float = 100000) -> None:
        super().__init__(name, saving_path, environment, cash=cash)
        self.buy_initial_holdings()

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

    override
    def sell(self, ticker, amount) -> None:
        """Holder Bot never sells"""
        pass

    def learn(self) -> None:
        """Holder Bot does not learn"""
        pass

    def test(self) -> None:
        pass

    def save(self) -> None:
        """Holder Bot does not save state action tables"""
        pass

    def save_history(self, filename: str) -> None:
        value =  [entry.to_json() for entry in self.history]
        path = getRootPath().joinpath(f"data/holder_bot/{self.name}/histories/{filename}")
        os.makedirs(path.parent, exist_ok=True)
        with open(path, "w") as f:
            json.dump(value, f, indent=4)

    def load(self, saving_path: str) -> None:
        """Holder Bot does not load state action tables"""
        pass