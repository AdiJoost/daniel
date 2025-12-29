

from datetime import date
import json
import os
import random
from rpds import List
from config.rootPath import getRootPath
from src.bots.base_bot import BaseBot
from src.enums.actions import Actions
from src.enums.price_points import PricePoints
from src.environment.base_environment import BaseEnvironment
from src.helpers.action_taken import ActionTaken
from src.helpers.history_entry import HistoryEntry


class RandomBot(BaseBot):

    def __init__(self, environment: BaseEnvironment, name="Random Bot", saving_path="random_bot", cash: float = 100000.0) -> None:
        self.environment = environment
        super().__init__(name=name, saving_path=saving_path, environment=environment, cash=cash)

    def take_action(self) -> bool:
        action = random.choice([Actions.BUY, Actions.SELL, Actions.END_DAY])
        if action == Actions.BUY:
            ticker = random.choice(self.tickers)
            amount = random.randint(100, 1000)
            self.buy(ticker, amount)
            return False
        elif action == Actions.SELL:
            ticker = random.choice(self.tickers)
            if self.portfolio[ticker] == 0:
                return False

            amount = 1 if self.portfolio[ticker] == 1 else random.randint(1, self.portfolio[ticker])
            self.sell(ticker, amount)
            return False
        else:
            self.end_day()
            return True

    def learn(self, itterations: int= 1) -> None:
        pass

    def test(self) -> None:
        pass

    def save(self, saving_path: str) -> None:
        pass

    def save_history(self, filename: str) -> None:
        value =  [entry.to_json() for entry in self.history]
        path = getRootPath().joinpath(f"data/random_bot/{self.saving_path}/histories/{filename}")
        os.makedirs(path.parent, exist_ok=True)
        with open(path, "w") as f:
            json.dump(value, f, indent=4)

    def load(self, saving_path: str) -> None:
        pass

    
    
    

    