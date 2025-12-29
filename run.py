

from src.bots.holder_bot.holder_bot import HolderBot
from src.bots.random_bot.random_bot import RandomBot
from src.bots.temporal_difference_bot.temporal_difference_bot import TemporalDifferenceBot
from src.environment.environment import Environment
from tqdm import tqdm

from src.environment.isolated_environment import IsolatedEnvironment


def run_random_bot():
    
    #Init the environment and bot
    environment = Environment(datastring='data/yfinance/metals_tickers_2015-01-01_to_2019-12-31_tidy.csv', performance_ticker='^GSPC')
    bot = RandomBot(environment=environment)

    #We run the bot 5 times to get different histories
    for i in range(5):

        #We run the bot the number of days -2, because the first day is used to set the initial state
        for _ in range(environment.get_number_of_days() - 2):

            #When bot.take_action() returns True, the day has ended, if it returns False, the bot is taking an action still
            while not bot.take_action():
                pass

        #We save the history of the bot in the file annotated with the iteration number, then we reset the bot for the next iteration
        bot.save_history(f"metal_random_bot_history_{i}.json")
        print(f"Final cash: {bot.cash + bot.get_portfolio_value()}")
        bot.reset()

def run_holder_bot():
    # The holder bot buys initial holdings and holds them throughout the simulation, acts as a benchmark for other bots
    environment = Environment(datastring='data/yfinance/tickers_2015-01-01_to_2019-12-31_tidy.csv', performance_ticker='^GSPC')
    bot = HolderBot(name="Holder Bot", saving_path="", environment=environment, cash=100000)
    
    for _ in range(environment.get_number_of_days() - 2):
        while not bot.take_action():
            pass
    bot.save_history(f"holder_bot_history.json")
    print(f"Final cash: {bot.cash + bot.get_portfolio_value()}")
    bot.save()

def run_td_bot():
    learning_itterations = 1
    
    environment = Environment(datastring='data/yfinance/tickers_2015-01-01_to_2019-12-31_tidy.csv', performance_ticker='^GSPC')
    bot = TemporalDifferenceBot(name="TD Bot", saving_path="", environment=environment, qStratRandom=True)
    
    for itteration in tqdm(range(learning_itterations), desc="Learning Iterations"):
        for _ in range(environment.get_number_of_days() - 2):
            while not bot.take_action():
                pass
        bot.save_history(f"td_bot_history_{itteration}.json")
        print(f"Iteration {itteration + 1}/{learning_itterations} complete. Final cash: {bot.cash + bot.get_portfolio_value()}")
        bot.reset()
    
    #Bot.save will save the state action table and the environment used in the specified saving path, we only do this once. But if you want to be save, you can save after a set intervall of itterations, effectively checkpointing the learning.
    bot.save()

def run_td_bot_isolated_environment():
    learning_itterations = 500
    
    # Isolated environment will test the performance not against the performance ticker, but against the average performance of all tickers the bot could buy or sell
    environment = IsolatedEnvironment(datastring='data/yfinance/tickers_2015-01-01_to_2019-12-31_tidy.csv', performance_ticker='^GSPC')
    bot = TemporalDifferenceBot(name="Isolated TD Bot", saving_path="Long_training", environment=environment, qStratRandom=True)
    
    for itteration in tqdm(range(learning_itterations), desc="Learning Iterations"):
        for _ in range(environment.get_number_of_days() - 2):
            while not bot.take_action():
                pass
        bot.save_history(f"isolated_td_bot_history_{itteration}.json")
        print(f"Iteration {itteration + 1}/{learning_itterations} complete. Final cash: {bot.cash + bot.get_portfolio_value()}")
        bot.reset()
    
    bot.save()

def test_td_bot():
    #Load a previously trained TD bot and test it without learning, we test it 10 times, as it is a stochastic bot
    learning_itterations = 10
    bot = TemporalDifferenceBot(name="Isolated TD Bot", saving_path="Long_training", qStratRandom=False, updateQValues=False, loadFromSave=True)
    
    for itteration in tqdm(range(learning_itterations), desc="Learning Iterations"):
        for _ in range(bot.environment.get_number_of_days() - 2):
            while not bot.take_action():
                pass
        bot.save_history(f"td_bot_history_{itteration}.json")
        print(f"Iteration {itteration + 1}/{learning_itterations} complete. Final cash: {bot.cash + bot.get_portfolio_value()}")
        bot.reset()
    bot.save()



if __name__ == "__main__":
    run_td_bot_isolated_environment()