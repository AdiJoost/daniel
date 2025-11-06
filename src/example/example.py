from config.configManager import loadConfig
import os

from src.bots.bot import hello

def main():
    print("Hello "+ loadConfig())
    print(os.environ.get("APP_ENV"))
    hello()


    

