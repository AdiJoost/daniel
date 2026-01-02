import itertools
import json
import os
import pandas as pd
from config.rootPath import getRootPath
from src.bots.base_bot import BaseBot
from src.enums.actions import Actions
from src.environment.base_environment import BaseEnvironment
from src.environment.environment import Environment
from src.environment.isolated_environment import IsolatedEnvironment
from src.helpers.action_taken import ActionTaken


class TemporalDifferenceBot(BaseBot):

    def __init__(self, name: str, saving_path: str, environment: BaseEnvironment = None, updateQValues: bool = True, qStratRandom: bool = False, cash: float = 100000, bulkBuy: int = 100, loadFromSave: bool = False) -> None:
        if loadFromSave == False:
            self.environment = environment
        else:
            self.load(saving_path= saving_path)
        
        super().__init__(name, saving_path, self.environment, updateQValues, cash)
        self.qStratRandom = qStratRandom
        self.bulkBuy = bulkBuy
        self.environment.set_next_date()
        
        if loadFromSave == False:
            # We can only init the tables if we are not loading from a save, but we can only init it after calling super().__init__
            self._initValueActionAndStateTables()
        
    def _initValueActionAndStateTables(self) -> None:
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
            self.buy(ticker, self.bulkBuy)
        elif action == Actions.SELL.value:
            self.sell(ticker, self.bulkBuy)
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
        path = getRootPath().joinpath(f"data/temporal_difference_bot/{self.saving_path}/state_action_table.csv")
        os.makedirs(path.parent, exist_ok=True)
        self.value_table.to_csv(path, index=False)

        path = getRootPath().joinpath(f"data/temporal_difference_bot/{self.saving_path}/environment.json")
        environment_json = self.environment.to_json()
        with open(path, "w") as f:
            json.dump(environment_json, f, indent=4)

    def save_history(self, filename: str) -> None:
        value =  [entry.to_json() for entry in self.history]
        path = getRootPath().joinpath(f"data/temporal_difference_bot/{self.saving_path}/histories/{filename}")
        os.makedirs(path.parent, exist_ok=True)
        with open(path, "w") as f:
            json.dump(value, f, indent=4)

    def load(self, saving_path: str) -> None:
        path = getRootPath().joinpath(f"data/temporal_difference_bot/{saving_path}/state_action_table.csv")
        self.value_table = pd.read_csv(path)
        path = getRootPath().joinpath(f"data/temporal_difference_bot/{saving_path}/environment.json")
        with open(path, "r") as f:
            environment_json = json.load(f)
        environmentClassName = environment_json.pop("class_name")
        if environmentClassName == "Environment":
            self.environment = Environment(**environment_json)
        elif environmentClassName == "IsolatedEnvironment":
            self.environment = IsolatedEnvironment(**environment_json)
        else:
            raise ValueError(f"Unknown environment class name: {environmentClassName}")
        