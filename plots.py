import pandas as pd
import pandas_datareader as pdr
from datetime import datetime
from datetime import date
import matplotlib.pyplot as plt
from matplotlib import dates as md

class plot_ti:

    '''
    a function used to plot
    closing prices of a stock
    '''
    def plot_stock(stock):
        start = plot_ti.start()
        end = plot_ti.end()
        df = pdr.get_data_yahoo(stock, start, end)
        plt.plot(df.index, df['Close'], label = stock, color = 'black')
        plt.title(stock + " closings")
        plt.legend(loc = 'upper left')
        plt.xlabel('Dates')

    '''
    a function used to plot
    the 20 day SMA and the 50 day SMA
    '''
    def plot_ma(stock, sma20, sma50, cross_day, cross_price):
        start = plot_ti.start()
        end = plot_ti.end()
        df = pdr.get_data_yahoo(stock, start, end)
        plt.figure(1)
        plt.plot(df.index[0:sma20.size], sma20, label = 'SMA 20')
        plt.plot(df.index[0:sma50.size], sma50, label = 'SMA 50')
        year = cross_day[0:4]
        month_num = cross_day[5:7]
        day = cross_day[8:10]
        cross_day = datetime(int(year), int(month_num), int(day))
        x_cross = md.datestr2num(cross_day.strftime("%m-%d-%Y"))
        y_cross = cross_price
        plt.scatter(x_cross, y_cross, marker='o', s=400, facecolors = 'none', edgecolors='y')
        plt.title("Moving averages for " + stock)
        plt.legend(loc = 'upper left')
        plt.xlabel('Dates')
        plt.xticks(rotation = 50)

    '''
    a function used to plot
    the MACD and signal line
    '''
    def plot_macd(stock, macd, signal, diff, cross_day, cross_price):
        start = plot_ti.start()
        end = plot_ti.end()
        df = pdr.get_data_yahoo(stock, start, end)
        plt.figure(2)
        plt.plot(df.index[0:macd.size], macd, label='MACD', color = 'green')
        plt.plot(df.index[0:signal.size], signal, label='Signal', color = 'purple')
        plt.bar(df.index[0: diff.size],diff , label = 'MACD Histogram', color = 'red')
        year = cross_day[0:4]
        month_num = cross_day[5:7]
        day = cross_day[8:10]
        cross_day = datetime(int(year), int(month_num), int(day))
        x_cross = md.datestr2num(cross_day.strftime("%m-%d-%Y"))
        y_cross = cross_price
        plt.scatter(x_cross, y_cross, marker='o', s= 300, facecolors='none', edgecolors='y')
        plt.title("MACD for " + stock)
        plt.legend(loc='upper left')
        plt.xlabel('Dates')
        plt.xticks(rotation=50)

    '''
    a function used to plot
    the stock's closing prices and bollinger bands
    '''
    def plot_bb(stock, lower, upper, cross_day, cross_price):
        start = plot_ti.start()
        end = plot_ti.end()
        df = pdr.get_data_yahoo(stock, start, end)
        plt.figure(3)
        plt.plot(df.index[0:lower.size], upper, label='+2SD Bollinger Band', color='pink')
        plt.plot(df.index[0:upper.size], lower, label='-2SD Bollinger Band', color='cyan')
        plot_ti.plot_stock(stock)
        year = cross_day[0:4]
        month_num = cross_day[5:7]
        day = cross_day[8:10]
        cross_day = datetime(int(year), int(month_num), int(day))
        x_cross = md.datestr2num(cross_day.strftime("%m-%d-%Y"))
        y_cross = cross_price
        plt.scatter(x_cross, y_cross, marker='o', s=300, facecolors='none', edgecolors='y')
        plt.title("Bollinger Bands For " + stock)
        plt.legend(loc='upper left')
        plt.xlabel('Dates')
        plt.xticks(rotation=50)

    @staticmethod
    def start():
        year = date.today().year
        month = date.today().month
        day = date.today().day
        return datetime(year - 1, month, day)

    @staticmethod
    def end():
        year = date.today().year
        month = date.today().month
        day = date.today().day
        return datetime(year, month, day)
