'''
This python script is indented to be used as a hypothetical trading bot
through the Robinhood Trading Platform
Noah Safeer
#1-15-21
'''

import robin_stocks as r #using the robinhood api
import getpass #used for the password
from tradestrategy import TradingStrategy
import matplotlib.pyplot as plt #used for plotting the data frames


'''
function designed to login to robinhood
'''
def login():
    input_user = input("What is your username? ")
    input_password = getpass.getpass("What is your password? ")

    login = r.login(input_user, input_password)

'''
function that sets up the trading bot and returns the stock the user is interested in
'''
def setup() -> str:

    stock = input("What stock are you interested in? (Only type the ticker) ")
    return stock.upper()

def run():
    login()
    ticker = setup()
    while ticker != "DONE":
        try:
            indicator = TradingStrategy(ticker)
            print("Displaying Graphs and Information...")
            indicator.final_decision()
        except:
            print("That ticker isn't available to trade on Robinhood. \n")
        plt.show(block = False)
        ticker = input("\nType in \"Done\" when you are finished or enter a new ticker for another stock: ")
        ticker = ticker.upper()
    #r.logout()

run()
