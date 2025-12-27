

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

    def __init__(self, environment: BaseEnvironment) -> None:
        self.environment = environment
        self.tickers = self.environment.get_tickers()
        self.history: List[HistoryEntry] = []
        self.cash = 100000.0
        self.portfolio = {ticker: 0 for ticker in self.tickers}
        self.setTodaysHistoryEntry()

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
        self.history.append(self.todaysHistory)
        self.environment.set_next_date()
        self.setTodaysHistoryEntry()

    def learn(self, itterations: int= 1) -> None:
        pass

    def test(self) -> None:
        pass

    def save(self, saving_path: str) -> None:
        pass

    def save_history(self, saving_path) -> None:
        value =  [entry.to_json() for entry in self.history]
        path = getRootPath().joinpath(f"data/random_bot_histories/{saving_path}")
        os.makedirs(path.parent, exist_ok=True)
        with open(path, "w") as f:
            json.dump(value, f, indent=4)

    def load(self, saving_path: str) -> None:
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