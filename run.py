

from src.bots.random_bot.random_bot import RandomBot
from src.environment.environment import Environment


def main():
    for i in range(5):
        environment = Environment(datastring='data/yfinance/metals_tickers_2015-01-01_to_2019-12-31_tidy.csv', performance_ticker='^GSPC')
        bot = RandomBot(environment=environment)
        for _ in range(environment.get_number_of_days() - 1):
            while not bot.take_action():
                pass

        bot.save_history(f"metal_random_bot_history_{i}.json")
        print(f"Final cash: {bot.cash + bot.get_portfolio_value()}")

if __name__ == "__main__":
    main()