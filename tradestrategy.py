import robin_stocks as r #using the robinhood api
import ta #used for finding technical indicators for securities
import pandas as pd #used for data storage and usage
import datetime
from plots import plot_ti
import matplotlib.pyplot as plt

'''
This class is designed to make decisions about a particular
security using moving averages, the MACD, and RSI
'''
class TradingStrategy:

    def __init__(self, stock):
        self.stock = stock

    '''
    returns a dictionary that contains one key value pair
    with a boolean as the key that indicates whether to buy
    based of the crossing of moving averages
    and a string value that represents the approximate date
    that the moving averages crossed
    '''

    def moving_average_decision(self) -> dict:
        closings = self.get_closings()
        closing_dates = self.get_closing_dates()
        sma20 = ta.volatility.bollinger_mavg(closings, 20, fillna=False)
        sma50 = ta.volatility.bollinger_mavg(closings, 50, fillna=False)
        crossover = self.moving_average_cross(sma20, sma50)
        raw_date = None

        num_date = list(crossover.values())[0]
        if (num_date is not None):
            raw_date = closing_dates.iloc[num_date]['begins_at']
            crossover_price = sma20[num_date]
            date = self.get_date(raw_date)
        else:
            date = None

        if (raw_date is not None):
            plot_ti.plot_ma(self.stock, sma20, sma50, raw_date[0:10], crossover_price)

        buy = list(crossover.keys())[0]
        return dict({buy: date})

    '''
    a helper function that determines the most recent cross of 
    2 data sets that represent simple moving averages
    it takes a 2 moving averages as parameters
    this function returns a dictionary with
    one key value pair where the key is a boolean
    indicating whether to buy a stock based on the MACD
    crossing and the value is an index in the dataframe
    of where the moving averages crossed
    '''
    def moving_average_cross(self, shorterma, longerma) -> dict:
        # remove NaN at first
        short = shorterma.dropna(axis='index')
        long = longerma.dropna(axis='index')

        short_Nan = shorterma.size - short.size
        offset = short_Nan

        amount = long.size
        start = longerma.size - amount - offset
        end = longerma.size - 1
        short = short[start:end]

        index = end
        if short[index] > long[index]:
            while (short[index] > long[index]) and index != start - 1:
                index -= 1
            if (short[index] < long[index]):
                cross_day = index
            if index == start - 1:
                cross_day = None
            buy = True
        else:
            while (short[index] < long[index]) and index != start - 1:
                index -= 1
            if (short[index] > long[index]):
                cross_day = index
            if index == start - 1:
                cross_day = None
            buy = False
        return dict({buy: cross_day})

    '''
    returns a dictionary that contains one key value pair
    with a boolean as the key that indicates whether to buy
    based of the MACD and a string value that represents the
    approximate date the MACD line crossed the signal line
    '''
    def macd_decision(self) -> dict:
        closings = self.get_closings()
        closing_dates = self.get_closing_dates()
        macd_diff = ta.trend.macd_diff(closings, window_slow = 26, window_fast = 12, window_sign = 9 , fillna =False)
        macd = ta.trend.macd(closings, window_slow = 26, window_fast = 12, fillna = False)
        signal = ta.trend.macd_signal(closings, window_slow = 26, window_fast = 12, window_sign = 9 , fillna =False)

        crossover = self.macd_cross(macd_diff)

        num_date = list(crossover.values())[0]
        if (num_date is not None):
            raw_date = closing_dates.iloc[num_date]['begins_at']
            crossover_price = macd[num_date]
            date = self.get_date(raw_date)
        else:
            date = None

        if (raw_date is not None):
            plot_ti.plot_macd(self.stock, macd, signal, macd_diff, raw_date[0:10], crossover_price)

        buy = list(crossover.keys())[0]
        return dict({buy: date})

    '''
    a helper function that takes the macd difference
    as a parameter and returns a dictionary with
    one key value pair where the key is a boolean
    indicating whether to buy a stock based on the MACD
    crossing and the value is an index in the dataframe
    of where the MACD crossed the signal line
    '''
    def macd_cross(self, macd_diff) -> dict:
        macd_cleaned = macd_diff.dropna(axis='index')

        end = macd_diff.size - 1
        start = macd_diff.size - macd_cleaned.size
        index = end

        if macd_cleaned[index] > 0:
            while macd_cleaned[index] > 0 and index != start - 1:
                index -= 1
            if macd_cleaned[index] < 0:
                cross_day = index
            if index == start - 1:
                cross_day = None
            buy = True
        else:
            while macd_cleaned[index] < 0 and index != start - 1:
                index -= 1
            if macd_cleaned[index] > 0:
                cross_day = index
            if index == start - 1:
                cross_day = None
            buy = False

        return dict({buy: cross_day})

    '''
    returns a dictionary that contains one key value pair
    with a string as the key that indicates how the stock is 
    valued and a date as the value that gives the approximate 
    day when a crossover occurred
    '''
    def bb_decision(self) -> dict:
        closing_dates = self.get_closing_dates()
        closings = self.get_closings()
        lower = ta.volatility.bollinger_lband(closings, window=20, window_dev=2, fillna=False)
        upper = ta.volatility.bollinger_hband(closings, window=20, window_dev=2, fillna=False)

        crossover = self.bb_crossover(closings,lower, upper)

        num_date = list(crossover.values())[0]
        if (num_date is not None):
            raw_date = closing_dates.iloc[num_date]['begins_at']
            if list(crossover.keys())[0] == 'oversold':
                crossover_price = lower[num_date]
            else:
                crossover_price = upper[num_date]
            date = self.get_date(raw_date)
        else:
            date = None

        if (raw_date is not None):
            plot_ti.plot_bb(self.stock, lower, upper, raw_date[0:10], crossover_price)

        buy = list(crossover.keys())[0]
        return dict({buy: date})

    '''
    a helper function that returns a dictionary with
    a string as the key to indicate how the stock is valued
    and a number corresponding to a date to indicate when the
    crossover occurred
    '''
    def bb_crossover(self, closings, lower_band, upper_band) -> dict:
        lower = lower_band.dropna(axis='index')
        upper = upper_band.dropna(axis='index')

        end = closings.size
        start = lower_band.size - lower.size
        closings = closings[start:end]
        index = end - 1
        closings = closings.astype('float64')

        while closings[index] > lower[index] and closings[index] < upper[index] and index != start -1:
            index -= 1
        if closings[index] < lower[index]:
            evaluation = "oversold"
        if closings[index] > upper[index]:
            evaluation = "overbought"
        if (index == start - 1):
            evaluation = "neutral"
            cross_day = None
        else:
            cross_day = index
        return dict({evaluation: cross_day})

    '''
    returns a str that represents a date
    '''
    def get_date(self , date) -> str:
        year = date[0:4]
        month_num = date[5:7]
        day = date[8:10]
        month = datetime.datetime(day = int(day), month = int(month_num), year = int(year))
        month_name = month.strftime("%B")
        date = month_name + " " + day + ", " + year
        return date

    '''
    a function that returns a pandas
    DataFrame for the closing prices of 
    a stock
    '''
    def get_closings(self):
        stock_history = r.stocks.get_stock_historicals(self.stock, interval='day', span='year', bounds='regular')
        stock_history_df = pd.DataFrame(stock_history)
        closings = stock_history_df['close_price']
        return closings

    '''
    a function that returns a pandas
    DataFrame with the dates corresponding to
    closing prices
    '''
    def get_closing_dates(self):
        stock_history = r.stocks.get_stock_historicals(self.stock, interval='day', span='year', bounds='regular')
        stock_history_df = pd.DataFrame(stock_history)
        closing_dates = stock_history_df[['begins_at', 'close_price']]
        return closing_dates

    '''
    a function that makes a final decision based off of the technical indicators 
    implemented on the stock
    '''
    def final_decision(self):
        score = 0
        ma_dict = self.moving_average_decision()
        if (list(ma_dict.keys())[0] == True):
            score += 1.5
            ma_conclusion = "The 20 day SMA crossed over the 50 day SMA around " + list(ma_dict.values())[0]
        else:
            score -= 1.5
            ma_conclusion = "The 20 day SMA crossed underneath the 50 day SMA around " + list(ma_dict.values())[0]

        macd_dict = self.macd_decision()
        if (list(macd_dict.keys())[0] == True):
            score += 1
            macd_conclusion = "The MACD crossed over the signal line around " + list(macd_dict.values())[0]
        else:
            score -= 1
            macd_conclusion = "The MACD crossed under the signal line around " + list(macd_dict.values())[0]

        bb_dict = self.bb_decision()
        if (list(bb_dict.keys())[0] == 'oversold'):
            score += .5
            bb_conclusion = self.stock + " closings crossed under the lower band around " + list(bb_dict.values())[0]
        elif(list(bb_dict.keys())[0] == 'overbought'):
            score -= .5
            bb_conclusion = self.stock + " closings crossed over the upper band around " + list(bb_dict.values())[0]
        else:
            bb_conclusion = self.stock + " closings never crossed over any band"

        if score == 3:
            decision = "strong buy"
        elif score >= 1.5:
            decision = "potential buy"
        elif score >= -1.5:
            decision = "potential sell"
        else:
            decision = "sell"

        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.options.display.max_colwidth = 100


        data = {'Conclusion' : [ma_conclusion, macd_conclusion, bb_conclusion, decision]}
        indices = ['Moving averages analysis: ', 'MACD Analysis: ', 'Bollinger Bands Analysis: ', 'Overall Decision: ']
        print(pd.DataFrame(data = data,index = indices))

