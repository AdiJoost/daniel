

from src.bots.holder_bot.holder_bot import HolderBot
from src.bots.random_bot.random_bot import RandomBot
from src.bots.temporal_difference_bot.temporal_difference_bot import TemporalDifferenceBot
from src.environment.environment import Environment
from tqdm import tqdm

from src.environment.isolated_environment import IsolatedEnvironment


def main_random_bot():
    for i in range(5):
        environment = Environment(datastring='data/yfinance/metals_tickers_2015-01-01_to_2019-12-31_tidy.csv', performance_ticker='^GSPC')
        bot = RandomBot(environment=environment)
        for _ in range(environment.get_number_of_days() - 1):
            while not bot.take_action():
                pass

        bot.save_history(f"metal_random_bot_history_{i}.json")
        print(f"Final cash: {bot.cash + bot.get_portfolio_value()}")

def main_td_bot():
    learning_itterations = 1000
    environment = Environment(datastring='data/yfinance/tickers_2015-01-01_to_2019-12-31_tidy.csv', performance_ticker='^GSPC')
    bot = TemporalDifferenceBot(name="TD Bot", saving_path="", environment=environment, qStratRandom=True)
    for itteration in tqdm(range(learning_itterations), desc="Learning Iterations"):
        for _ in range(environment.get_number_of_days() - 2):
            while not bot.take_action():
                pass
        bot.save_history(f"td_bot_history_{itteration}.json")
        print(f"Iteration {itteration + 1}/{learning_itterations} complete. Final cash: {bot.cash + bot.get_portfolio_value()}")
        bot.reset()
    bot.save()

def main_td_bot_isolated_environment():
    learning_itterations = 1000
    environment = IsolatedEnvironment(datastring='data/yfinance/tickers_2015-01-01_to_2019-12-31_tidy.csv', performance_ticker='^GSPC')
    bot = TemporalDifferenceBot(name="Isolated TD Bot", saving_path="", environment=environment, qStratRandom=True)
    for itteration in tqdm(range(learning_itterations), desc="Learning Iterations"):
        for _ in range(environment.get_number_of_days() - 2):
            while not bot.take_action():
                pass
        bot.save_history(f"isolated_td_bot_history_{itteration}.json")
        print(f"Iteration {itteration + 1}/{learning_itterations} complete. Final cash: {bot.cash + bot.get_portfolio_value()}")
        bot.reset()
    bot.save()

def test_td_bot():
    learning_itterations = 10
    environment = Environment(datastring='data/yfinance/tickers_2015-01-01_to_2019-12-31_tidy.csv', performance_ticker='^GSPC')
    bot = TemporalDifferenceBot(name="TD Bot", saving_path="", environment=environment, qStratRandom=False, updateQValues=False)
    for itteration in tqdm(range(learning_itterations), desc="Learning Iterations"):
        for _ in range(environment.get_number_of_days() - 2):
            while not bot.take_action():
                pass
        bot.save_history(f"td_bot_history_{itteration}.json")
        print(f"Iteration {itteration + 1}/{learning_itterations} complete. Final cash: {bot.cash + bot.get_portfolio_value()}")
        bot.reset()
    bot.save()

def test_holder_bot():
    environment = Environment(datastring='data/yfinance/tickers_2015-01-01_to_2019-12-31_tidy.csv', performance_ticker='^GSPC')
    bot = HolderBot(name="Holder Bot", saving_path="", environment=environment, qStratRandom=False, updateQValues=False)
    for _ in range(environment.get_number_of_days() - 2):
        while not bot.take_action():
            pass
    bot.save_history(f"holder_bot_history.json")
    print(f"Final cash: {bot.cash + bot.get_portfolio_value()}")
    bot.save()

if __name__ == "__main__":
    main_td_bot_isolated_environment()