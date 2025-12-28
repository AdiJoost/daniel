

from datetime import date
import itertools
import json
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


class TemporalDifferenceBot(BaseBot):

    def __init__(self, name: str, saving_path: str, environment: BaseEnvironment = None, updateQValues: bool = True, qStratRandom: bool = False) -> None:
        if saving_path is None or saving_path == "":
            self.environment = environment
            self._initValueActionAndStateTables()
        else:
            self.load(name)
        self.name = name
        self.history: List[HistoryEntry] = []
        self.cash = 100000.0
        self.portfolio = {ticker: 0 for ticker in self.tickers}
        self.updateQValues = updateQValues
        self.qStratRandom = qStratRandom
        self.environment.set_next_date()
        self.setTodaysHistoryEntry()

    def _initValueActionAndStateTables(self) -> None:
        self.tickers = self.environment.get_tickers()
        combos = list(itertools.product([0,1], repeat=len(self.tickers)))
        combo_df = pd.DataFrame(combos, columns=self.tickers)
        df = pd.concat(
            [
                combo_df.assign(ticker=t, value=1, action=action)
                for t in self.tickers
                for action in [Actions.BUY.value, Actions.SELL.value, Actions.HOLD.value]
            ],
            ignore_index=True
        )
        self.value_table = df[["ticker", "value", "action"] + self.tickers]

    def take_action(self) -> bool:
        self.todays_state = self.environment.get_tickers_change()
        self.todaysHistory.set_state(self._get_state_string(self.todays_state))
        maskActions = (self.value_table[self.tickers] == pd.Series(self.todays_state)).all(axis=1)
        possibleActions = self.value_table[maskActions]
        if self.qStratRandom == False:
            top_actions = possibleActions.nlargest(3, "value")
            chosenActionRow = top_actions.sample(n=1).iloc[0]
        else:
            chosenActionRow = possibleActions.sample(n=1).iloc[0]
        action = chosenActionRow["action"]
        ticker = chosenActionRow["ticker"]
        if action == Actions.BUY.value:
            self.buy(ticker, 10)
        elif action == Actions.SELL.value:
            self.sell(ticker, 10)
        elif action == Actions.HOLD.value:
            action_taken = ActionTaken(
                action=Actions.HOLD,
                amount=0.0,
                money_transfered=0.0,
                ticker=ticker,
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
        if self.updateQValues:
            self.learn()
        self.history.append(self.todaysHistory)
        self.environment.set_next_date()
        self.setTodaysHistoryEntry()

    def learn(self) -> None:
        for actionTaken in self.todaysHistory.actions_taken:
            if (actionTaken.action == Actions.END_DAY):
                continue
            mask = ((self.value_table["ticker"] == actionTaken.ticker) &
                    (self.value_table["action"] == actionTaken.action.value))
            for col, val in self.todays_state.items():
                mask &= self.value_table[col] == val
            
            delta = -actionTaken.fee_paid + (
            self.todaysHistory.alpha - self.value_table.loc[mask, "value"])       

            self.value_table.loc[mask, "value"] += delta

    def test(self) -> None:
        pass

    def save(self) -> None:
        path = getRootPath().joinpath(f"data/temporal_difference_bot/{self.name}/state_action_table.csv")
        os.makedirs(path.parent, exist_ok=True)
        self.value_table.to_csv(path, index=False)

        path = getRootPath().joinpath(f"data/temporal_difference_bot/{self.name}/environment.json")
        environment_json = self.environment.to_json()
        with open(path, "w") as f:
            json.dump(environment_json, f, indent=4)

    def save_history(self, saving_path) -> None:
        value =  [entry.to_json() for entry in self.history]
        path = getRootPath().joinpath(f"data/temporal_difference_bot/{self.name}/{saving_path}")
        os.makedirs(path.parent, exist_ok=True)
        with open(path, "w") as f:
            json.dump(value, f, indent=4)

    def load(self, saving_path: str) -> None:
        path = getRootPath().joinpath(f"data/temporal_difference_bot/{self.saving_path}/state_action_table.csv")
        self.value_table = pd.read_csv(path)
        path = getRootPath().joinpath(f"data/temporal_difference_bot/{self.saving_path}/environment.json")
        with open(path, "r") as f:
            environment_json = json.load(f)
        self.environment = Environment(**environment_json)

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
        self.cash = 100000.0
        self.portfolio = {ticker: 0 for ticker in self.tickers}
        self.environment.reset_environment()
        self.history = []
        self.environment.set_next_date()
        self.setTodaysHistoryEntry()