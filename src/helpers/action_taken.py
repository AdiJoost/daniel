from src.enums.actions import Actions


class ActionTaken():
    """
    Represents an action taken during a trading day.

    Args:
        action (str): The type of action taken (e.g., "buy", "sell" or "end_day").
        amount (float): The amount of the asset involved in the action.
        money_transfered (float): The amount of money transferred during the action.
        ticker (str): The ticker symbol of the asset involved in the action.
        fee_paid (float): The fee paid for executing the action.
    """

    def __init__(self, action: Actions, amount: float, money_transfered: float, ticker: str, fee_paid: float) -> None:
        self.action = action
        self.amount = amount
        self.money_transfered = money_transfered
        self.ticker = ticker
        self.fee_paid = fee_paid

    def to_json(self) -> dict:
        return {
            "action": str(self.action),
            "amount": self.amount,
            "money_transfered": self.money_transfered,
            "ticker": self.ticker,
            "fee_paid": self.fee_paid
        }

    def __repr__(self) -> str:
        return f"<action={self.action}, ticker={self.ticker}, amount={self.amount}, money_transfered={self.money_transfered}, fee_paid={self.fee_paid}>\n"