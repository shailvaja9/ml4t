
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import datetime as dt
from util import get_data


def author():
    return "svaja6"


def bb(data, window = 20, std = 2):

    mid_band = data.rolling(window = window).mean()
    standard_deviation  = data.rolling(window = window).std()

    upper_band = mid_band + (standard_deviation * std)
    lower_band = mid_band - (standard_deviation * std)

    mid_band.index = data.index
    upper_band.index = data.index
    lower_band.index = data.index

    #bb = pd.DataFrame(data.index.copy())#, columns = ["mid_band", "upper_band", "lower_band"])

    #bb["mid_band"] = mid_band
    #bb["upper_band"] = upper_band
    #bb["lower_band"] = lower_band
    bb = pd.concat([mid_band, upper_band, lower_band], axis = 1)
    bb.columns = ["mid_band", "upper_band", "lower_band"]
    return bb

def rsi(data, window = 14):

    delta = data.diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window = window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window = window).mean()

    rs = gain/loss
    rs = 100 - (100/(1+rs))
    rs.index = data.index
    #rsi_df = pd.DataFrame(data.index.copy())
    #rsi_df["rsi"] = rs
    rs.columns = ["rsi"]
    return rs


def stochastic(data, high_data, low_data,  window = 14, d_n = 3):
    data_s = data['JPM']
    high_s = high_data['JPM']
    low_s = low_data['JPM']

    low_min = low_s.rolling(window=window).min()
    high_max = high_s.rolling(window=window).max()
    #low_min.index = data.index
    #high_max.index = data.index
    epsilon = 1e-10

    #stochastic_df = pd.DataFrame(data.index.copy())
    k = (((data_s - low_min) / (high_max - low_min+ epsilon))) * 100
    k.index = data.index
    # Calculate %D
    d = k.rolling(window=d_n).mean()
    d.index = data.index
    stochastic_df = pd.concat([k,d], axis=1)
    stochastic_df.columns = ["%K", "%D"]
    return stochastic_df


def momentum_indicator(data, window = 14):
    momentum = data["JPM"].diff(window)
    momentum.index = data.index
    momentum.columns = ["momentum"]
    return momentum


def macd(data, slow = 26, fast = 12, signal = 9):
    ema_fast = data.ewm(span = fast, adjust=True).mean()
    ema_slow = data.ewm(span = slow, adjust=True).mean()
    macd = ema_fast - ema_slow

    signal_line = macd.ewm(span = signal, adjust=True).mean()
    macd.index = data.index
    signal_line.index = data.index
    #macd_df = pd.DataFrame(data.index.copy())
    macd_df = pd.concat([macd, signal_line], axis=1)
    macd_df.columns = ["macd", "signal"]
    return macd_df

def plotter(indicator, indicator_data, data):
    plt.figure(figsize=(10, 6))
    if indicator == "BollingerBands" or indicator == "BollingerBandsZoom":
        middle_band = indicator_data["mid_band"]
        upper_band = indicator_data["upper_band"]
        lower_band = indicator_data["lower_band"]
        plt.plot(data, label = "Price", color = 'blue')
        plt.plot(middle_band, label = "Middle Band", color = 'black', linestyle = 'dashed')
        plt.fill_between(indicator_data.index, lower_band, upper_band, color = 'grey', alpha = 0.3, label = "Bollinger Bands")
        plt.title("Bollinger Bands and Price")
    if indicator == "RSI" or indicator == "RSIZoom":
        plt.plot(data, label = "Price", color = 'blue')
        plt.plot(indicator_data.index, indicator_data['rsi'], label="RSI", color='purple')
        plt.axhline(70, color='red', linestyle='--', label='Overbought (70)')
        plt.axhline(30, color='green', linestyle='--', label='Oversold (30)')
        plt.title('Relative Strength Index (RSI)')
        plt.ylim(0, 100)
    if indicator == "macd" or indicator == "macd":
        indicator_data['Histogram'] = indicator_data['macd'] - indicator_data['signal']

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 7), sharex=True)

        ax1.plot(data.index, data['JPM'], label='Close Price')
        ax1.set_title('Stock Price and MACD Indicator')
        ax1.set_ylabel('Price')
        ax1.legend()

        ax2.plot(indicator_data.index, indicator_data['macd'], label='MACD Line', color='blue')
        ax2.plot(indicator_data.index, indicator_data['signal'], label='Signal Line', color='red')
        ax2.bar(indicator_data.index, indicator_data['Histogram'], label='Histogram', color='grey', alpha=0.5)
        ax2.set_ylabel('MACD')
        ax2.legend()

        plt.xticks(rotation=45)
        plt.xlabel('Date')
        plt.tight_layout()
        plt.savefig('./images/Fig_' + indicator + '.png')

    if indicator == "stochastic" or indicator == "stochasticZoom":
        plt.plot(data, label="Price", color='blue')
        plt.plot(indicator_data.index, indicator_data['%K'], label = "%K", color = 'purple')
        plt.plot(indicator_data.index, indicator_data['%D'], label = "%D", color = 'red')
        plt.axhline(80, color='grey', linestyle='--', alpha = 0.5)
        plt.axhline(20, color='grey', linestyle='--', alpha = 0.5)
        plt.title("Stochastic Oscillator")
    if indicator == "momentum":
        fig, ax1 = plt.subplots(figsize=(10, 6))

        color = 'tab:blue'
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Price', color=color)
        ax1.plot(data.index, data, label='Price', color=color)
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel('Momentum', color=color)
        ax2.plot(data.index, indicator_data, label='Momentum', color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        fig.tight_layout()
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        plt.title('Closing Price and Momentum Indicator')
        plt.savefig('./images/Fig_'+ indicator+'.png')



    if indicator != "momentum" and indicator != "macd" and "Zoom" not in indicator:
        plt.xlim(indicator_data.index.min(), indicator_data.index.max())
        plt.legend()
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.savefig('./images/Fig_'+ indicator+'.png')

    if "Zoom" in indicator:
        start_date = dt.datetime(2009, 3, 1)
        end_date = dt.datetime(2009, 7, 1)
        plt.xlim(start_date, end_date)
        plt.legend()
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.savefig('./images/Fig_Zoomed_' + indicator + '.png')


def run():
    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2009, 12, 31)
    symbol = "JPM"
    data = get_data([symbol], pd.date_range(start_date, end_date))
    data.drop("SPY", inplace = True, axis=1)
    data = data.bfill().ffill()
    high_data = get_data([symbol], pd.date_range(start_date, end_date),  colname='High')
    high_data.drop("SPY", inplace=True, axis=1)
    high_data = high_data.bfill().ffill()
    low_data = get_data([symbol], pd.date_range(start_date, end_date), colname='Low')
    low_data.drop("SPY", inplace=True, axis=1)
    low_data = low_data.bfill().ffill()
    close_data = get_data([symbol], pd.date_range(start_date, end_date), colname='Close')
    close_data.drop("SPY", inplace=True, axis=1)
    close_data = low_data.bfill().ffill()
    #data = pd.concat([data, high_data, low_data], axis=1)

    bollinger_bands = bb(data)
    plotter("BollingerBands", bollinger_bands, data )
    plotter("BollingerBandsZoom", bollinger_bands, data )

    rsi_bands = rsi(data)
    plotter("RSI", rsi_bands, data)
    plotter("RSIZoom", rsi_bands, data)
    stochastic_bands = stochastic(close_data, high_data, low_data)
    plotter("stochastic", stochastic_bands, data)
    plotter("stochasticZoom", stochastic_bands, data)
    macd_data = macd(data)
    plotter("macd", macd_data, data)
    momentum_data  = momentum_indicator(data)
    plotter("momentum", momentum_data, data)






if __name__ == '__main__':
    run()