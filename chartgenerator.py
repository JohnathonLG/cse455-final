# Jess Olmstead and Johnathon Guerrero

import numpy as np
import matplotlib.pyplot as plt
import mplfinance
import csv
import pandas as pd
import pandas_datareader as pdr
import datetime as dt
from random import randint

SECONDS_IN_DAY = 60 * 60 * 24
CHART_PERIOD = SECONDS_IN_DAY * 3


def import_data():
    today = dt.datetime(2021, 5, 29)

    # start = dt.datetime(2015, 7, 13)
    # start = dt.datetime(2014, 1, 1)
    start = dt.datetime(2021, 5, 12)
    old_start = dt.datetime(2017, 1, 29)
    chart_end = start + dt.timedelta(days=14)
    end = chart_end + dt.timedelta(days=1)
    # older_assets = {"DOGE-USD", "XMR-USD", "XLM-USD", "LTC-USD", "XEM-USD", "DASH-USD", "ETH-USD"}
    assets = {"ADA-USD", "BNB-USD", "XRP-USD", "DOT1-USD", "UNI3-USD", "BCH-USD", "ETC-USD", "MATIC-USD", "LINK-USD",
              "ALGO-USD", "TRX-USD", "BTT1-USD", "AMP1-USD", "ETH-USD", "MIOTA-USD", "HEX-USD", "SOL1-USD", "VET-USD",
              "THETA-USD", "EOS-USD", "FIL-USD", "XMR-USD", "AAVE-USD", "NEO-USD", "MKR-USD", "BSV-USD", "XTZ-USD",
              "CRO-USD", "ATOM1-USD", "LUNA1-USD", "KSM-USD", "AVAX-USD", "COMP-USD", "ZEC-USD", "HNT1-USD", "CTC1-USD",
              "DCR-USD", "HBAR-USD", "CCXX-USD", "CHZ-USD", "EGLD-USD", "TFUEL-USD", "CEL-USD", "SUSHI-USD",
              "DOGE-USD", "XMR-USD", "XLM-USD", "LTC-USD", "XEM-USD", "DASH-USD"}
    # while end < today:
    while start > old_start:
        for asset in assets:
            print(f"Checking {asset} on {start}")
            try:
                df = pdr.DataReader(asset, 'yahoo', start, end)
                close = df.at[chart_end, 'Close']
                nextclose = df.at[end, 'Close']
                df.drop(df.tail(1).index, inplace=True)
                print(df)
                print(close)
                print(nextclose)
                chart_from_df(df, start, close, nextclose, asset)
            except KeyError:
                continue
            except:  # Need this to prevent be robust against any unexpected errors when running overnight for days
                continue
        # start += dt.timedelta(days=1)
        # chart_end += dt.timedelta(days=1)
        # end += dt.timedelta(days=1)
        start -= dt.timedelta(days=1)
        chart_end -= dt.timedelta(days=1)
        end -= dt.timedelta(days=1)


def chart_from_df(df, date, close, nextclose, asset):
    change = (nextclose - close) / close
    if not isinstance(change, float):
        return

    if -0.01 < change < 0.01:
        dir = "flat"
    elif 0.01 < change < 0.05:
        dir = "+1%"
    elif 0.05 < change < 0.10:
        dir = "+5%"
    elif change > 0.10:
        dir = "+10%"
    elif -0.01 > change > -0.05:
        dir = "d1%"
    elif -0.05 > change > -0.10:
        dir = "d5%"
    elif change < -0.10:
        dir = "d10%"
    else:
        dir = ""
    num = randint(0, 100)
    if num > 97:
        dataset = "val"
    elif num > 85:
        dataset = "test"
    else:
        dataset = "train"
    filename = f"data/{dataset}/{dir}/{asset}_{date.strftime('%Y-%m-%d')}.jpg"
    print(filename)

    # Make the figure and save it
    save = {"fname": filename, "dpi": 60, "bbox_inches": "tight"}
    mplfinance.plot(df, type="candle", style="charles", volume=True, mav=3, axisoff=True, figscale=1, savefig=save)


class ChartGenerator:
    def __init__(self, path):
        self.path = path

    def gen_data(self):
        with open(self.path, 'r') as file:
            datareader = csv.reader(file)
            data = []
            for lnum, line in enumerate(datareader):
                time = int(line[0])
                if lnum == 0:
                    start_time = time
                if time - start_time >= CHART_PERIOD:
                    self.make_chart(data)
                    start_time += SECONDS_IN_DAY
                    i = 0
                    while i < len(data) and data[i][0] <= start_time:
                        i += 1
                    data = data[i:]
                data.append((int(line[0]), float(line[1]), float(line[2])))

    def make_chart(self, data):
        print(f"Creating chart from t={data[0][0]} to t={data[-1][0]}, with {len(data)} datapoints")

        # Get the data in the format we need
        # opens, closes, highs, lows

        figure = plt.figure(num=1, figsize=(3, 3), dpi=50, facecolor='w', edgecolor='k')


if __name__ == '__main__':
    # gen = ChartGenerator("coinbaseUSD.csv")
    # gen.gen_data()
    import_data()
