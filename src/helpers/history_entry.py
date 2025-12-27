"""
% better than smp500
action taken
"""

from datetime import date
from rpds import List
from src.helpers.action_taken import ActionTaken


class HistoryEntry():
    """
    Represents a history entry for a trading day.

    Args:
        day (str): The day of the trading entry.
        actions_taken (List[ActionTaken]): List of actions taken on that day.
        portfolio_value (float): The value of the portfolio at the end of the day.
        cash (float): The amount of cash available at the end of the day.
        sAndPPerformance (float): The performance of the S&P 500 on that day.
        alpha (float): The alpha value representing performance relative to the S&P 500.
    """

    def __init__(self, day: date,  portfolio_value_at_start: float, cash_at_start: float, sAndPPerformance: float, portfolio_value_at_end: float = 0.0, cash_at_end: float = 0.0, actions_taken: "List[ActionTaken]"= []) -> None:
        self.day = day
        self.actions_taken: "List[ActionTaken]" = actions_taken
        self.portfolio_value_at_start = portfolio_value_at_start
        self.cash_at_start = cash_at_start
        self.portfolio_value_at_end = portfolio_value_at_end
        self.cash_at_end = cash_at_end
        self.sAndPPerformance = sAndPPerformance
        self.alpha = None
        self.total_gain = None

    def add_action_taken(self, action_taken: ActionTaken) -> None:
        self.actions_taken.append(action_taken)

    def set_cash_at_end(self, cash_at_end: float) -> None:
        self.cash_at_end = cash_at_end

    def set_portfolio_value_at_end(self, portfolio_value_at_end: float) -> None:
        self.portfolio_value_at_end = portfolio_value_at_end

    def calculate_alpha(self) -> float:
        """
        Calculate the alpha value representing performance relative to the S&P 500.

        :param cash_at_start: Cash at the start of the day.
        :type cash_at_start: float
        :param portfolio_value_at_start: Portfolio value at the start of the day.
        :type portfolio_value_at_start: float
        :param cash_at_end: Cash at the end of the day.
        :type cash_at_end: float
        :param portfolio_value_at_end: Portfolio value at the end of the day.
        :type portfolio_value_at_end: float
        :param sAndPPerformance: Performance of the S&P 500 on that day.
        :type sAndPPerformance: float
        :return: Calculated alpha value.
        :rtype: float
        """
        starting_total = self.cash_at_start + self.portfolio_value_at_start
        ending_total = self.cash_at_end + self.portfolio_value_at_end

        if starting_total == 0:
            self.alpha = 0.0
            return 0.0

        bot_performance = (ending_total - starting_total) / starting_total
        alpha = bot_performance - self.sAndPPerformance
        self.alpha = alpha
        return alpha
    
    def caluclate_total_gain(self) -> float:
        start_value = self.portfolio_value_at_start + self.cash_at_start
        end_value = self.portfolio_value_at_end + self.cash_at_end
        
        if start_value == 0:
            self.total_gain = 0.0
            return 0.0
        self.total_gain = (end_value - start_value) / start_value
        return self.total_gain

    def to_json(self) -> dict:
        return {
            "day": str(self.day),
            "portfolio_value_at_start": self.portfolio_value_at_start,
            "cash_at_start": self.cash_at_start,
            "portfolio_value_at_end": self.portfolio_value_at_end,
            "cash_at_end": self.cash_at_end,
            "sAndPPerformance": self.sAndPPerformance,
            "total_gain": self.total_gain,
            "alpha": self.alpha,
            "actions_taken": [action.to_json() for action in self.actions_taken]
        }
    
    def __repr__(self) -> str:
        actions = '\n'.join([repr(action) for action in self.actions_taken])
        return f"---HistoryEntry {self.day}---\n\nportfolio_value_at_start={self.portfolio_value_at_start}\ncash_at_start={self.cash_at_start}\nportfolio_value_at_end={self.portfolio_value_at_end}\ncash_at_end={self.cash_at_end}\nperformance={self.caluclate_total_gain()}\nsAndPPerformance={self.sAndPPerformance}\nalpha={self.alpha}\n\n-Actions-\n\n{actions}\n\n"