from iqoptionapi.stable_api import IQ_Option
import time
import numpy as np
import os
from multiprocessing import Process
import pandas as pd
from stockstats import StockDataFrame


class dankiq:
    def __init__(self):
        pass

    def buy_function(self):
        iq = IQ_Option("test@gmail.com", "test")
        iq.connect()
        print("Buy Process Connected")
        goal = "EURUSD-OTC"
        size = 120
        maxdict = 30
        money = 5
        expirations_mode = 2
        ACTION = ""  # "call" or "put"
        iq.start_candles_stream(goal, size, maxdict)

        buy_macd_first_trigger = False
        buy_macd_second_trigger = False
        buy_macd_third_trigger = False
        buy_sma_trigger = False

        def get_stockstats_df():
            # get real time candles from iqoptions
            candles = iq.get_realtime_candles(goal, size)
            data = []

            # convert the dictionary of dictionaries from the candles into a list
            for i, k in candles.items():
                data.append(k)

            # convert the list into a padas Dataframe
            df = pd.DataFrame(data=data)
            df.drop(labels=["id", "from", "at"], axis=1)
            # convert the pandas dataframe into a stockstats dataframe (still works with pandas)
            stock = StockDataFrame.retype(df)

            return stock

        while True:
            stock = get_stockstats_df()
            # enable macd, macds and macdh in the stockstats dataframe
            stock["macd"]

            # select the last row of the dataframe
            buy_macd_last_row = stock.tail(1)

            # get macd value from the stockstats dataframe
            macd = buy_macd_last_row.get("macd")
            macd = float(macd)
            macd = np.around(macd, decimals=5)

            # get macds value from the stockstats dataframe
            macds = buy_macd_last_row.get("macds")
            macds = float(macds)
            macds = np.around(macds, decimals=5)

            # check for macd first trigger
            if not buy_macd_first_trigger:
                if (macd < macds) and (abs(macd - macds) >= 0.00001):
                    buy_macd_first_trigger = True
                    print("buy macd first trigger activated")

            # check for macd second trigger
            if not buy_macd_second_trigger:
                if buy_macd_first_trigger and (macd == macds):
                    buy_macd_second_trigger = True
                    print("buy macd second trigger activated")

            # check for third trigger
            if not buy_macd_third_trigger:
                if buy_macd_second_trigger:
                    duration = 180
                    end = time.time() + duration
                    while time.time() < end:
                        stock = get_stockstats_df()
                        stock["macd"]
                        # select the last row of the dataframe
                        buy_macd_last_row = stock.tail(1)

                        # get macd value from the stockstats dataframe
                        macd = buy_macd_last_row.get("macd")
                        macd = float(macd)
                        macd = np.around(macd, decimals=5)

                        # get macds value from the stockstats dataframe
                        macds = buy_macd_last_row.get("macds")
                        macds = float(macds)
                        macds = np.around(macds, decimals=5)

                        if (macd > macds) and (abs(macd - macds) >= 0.00001):
                            buy_macd_third_trigger = True
                            print("Buy macd third trigger activated")
                            break

                    if not buy_macd_third_trigger:
                        buy_macd_first_trigger = False
                        buy_macd_second_trigger = False
                        print("Buy macd triggers reset")

            # check for sma trigger
            if not buy_sma_trigger:
                if buy_macd_third_trigger:
                    print("Buy check sma")
                    # check for sma triggers for 8 minutes
                    duration = 480
                    end = time.time() + duration
                    while time.time() < end:
                        stock = get_stockstats_df()
                        stock["open_6_sma"]
                        stock["open_14_sma"]

                        sma_last_row = stock.tail(1)

                        sma_6 = sma_last_row.get("open_6_sma")
                        sma_6 = float(sma_6)
                        sma_6 = np.around(sma_6, decimals=5)

                        sma_14 = sma_last_row.get("open_14_sma")
                        sma_14 = float(sma_14)
                        sma_14 = np.around(sma_14, decimals=5)

                        if not buy_sma_trigger:
                            if sma_6 == sma_14:
                                buy_sma_trigger = True
                                print("buy sma trigger activated")
                                break

                    if not buy_sma_trigger:
                        buy_macd_first_trigger = False
                        buy_macd_second_trigger = False
                        buy_macd_third_trigger = False
                        print("Buy Macd triggers have been reseted")

            # check for buy
            if buy_sma_trigger:
                print("Checking if to buy")
                while True:
                    stock = get_stockstats_df()
                    stock["open_6_sma"]
                    stock["open_14_sma"]

                    sma_last_row = stock.tail(1)

                    sma_6 = sma_last_row.get("open_6_sma")
                    sma_6 = float(sma_6)
                    sma_6 = np.around(sma_6, decimals=5)

                    sma_14 = sma_last_row.get("open_14_sma")
                    sma_14 = float(sma_14)
                    sma_14 = np.around(sma_14, decimals=5)

                    if (sma_6 > sma_14) and (abs(sma_6 - sma_14) >= 0.00001):
                        ACTION = "call"
                        iq.buy(money, goal, ACTION, expirations_mode)
                        print("Buy bid placed\n")
                        buy_macd_first_trigger = False
                        buy_macd_second_trigger = False
                        buy_macd_third_trigger = False
                        buy_sma_trigger = False
                        break

    def sell_function(self):
        iq = IQ_Option("autisticmaster69@gmail.com", "FAKErayan106")
        iq.connect()
        print("Sell Process Connected")
        goal = "EURUSD-OTC"
        size = 120
        maxdict = 30
        money = 5
        expirations_mode = 2
        ACTION = ""  # "call" or "put"
        iq.start_candles_stream(goal, size, maxdict)

        sell_macd_first_trigger = False
        sell_macd_second_trigger = False
        sell_macd_third_trigger = False
        sell_sma_trigger = False

        def get_stockstats_df():
            # get real time candles from iqoptions
            candles = iq.get_realtime_candles(goal, size)
            data = []

            # convert the dictionary of dictionaries from the candles into a list
            for i, k in candles.items():
                data.append(k)

            # convert the list into a padas Dataframe
            df = pd.DataFrame(data=data)
            df.drop(labels=["id", "from", "at"], axis=1)
            # convert the pandas dataframe into a stockstats dataframe (still works with pandas)
            stock = StockDataFrame.retype(df)

            return stock

        while True:
            stock = get_stockstats_df()
            # enable macd, macds and macdh in the stockstats dataframe
            stock["macd"]

            # select the last row of the dataframe
            sell_macd_last_row = stock.tail(1)

            # get macd value from the stockstats dataframe
            macd = sell_macd_last_row.get("macd")
            macd = float(macd)
            macd = np.around(macd, decimals=5)

            # get macds value from the stockstats dataframe
            macds = sell_macd_last_row.get("macds")
            macds = float(macds)
            macds = np.around(macds, decimals=5)

            # check for macd first trigger
            if not sell_macd_first_trigger:
                if (macd > macds) and (abs(macd - macds) >= 0.00001):
                    sell_macd_first_trigger = True
                    print("sell macd first trigger activated")

            # check for macd second trigger
            if not sell_macd_second_trigger:
                if sell_macd_first_trigger and (macd == macds):
                    sell_macd_second_trigger = True
                    print("sell macd second trigger activated")

            # check for third trigger
            if not sell_macd_third_trigger:
                if sell_macd_second_trigger:
                    duration = 180
                    end = time.time() + duration
                    while time.time() < end:
                        stock = get_stockstats_df()
                        stock["macd"]
                        # select the last row of the dataframe
                        sell_macd_last_row = stock.tail(1)

                        # get macd value from the stockstats dataframe
                        macd = sell_macd_last_row.get("macd")
                        macd = float(macd)
                        macd = np.around(macd, decimals=5)

                        # get macds value from the stockstats dataframe
                        macds = sell_macd_last_row.get("macds")
                        macds = float(macds)
                        macds = np.around(macds, decimals=5)

                        if (macd > macds) and (abs(macd - macds) >= 0.00001):
                            sell_macd_third_trigger = True
                            print("Sell macd third trigger activated")
                            break

                    if not sell_macd_third_trigger:
                        sell_macd_first_trigger = False
                        sell_macd_second_trigger = False
                        print("Sell macd triggers reset")
            # check for sma trigger
            if not sell_sma_trigger:
                if sell_macd_third_trigger:
                    print("sell check sma")
                    # check for sma triggers for 8 minutes
                    duration = 480
                    end = time.time() + duration
                    while time.time() < end:
                        stock = get_stockstats_df()
                        stock["open_6_sma"]
                        stock["open_14_sma"]

                        sma_last_row = stock.tail(1)

                        sma_6 = sma_last_row.get("open_6_sma")
                        sma_6 = float(sma_6)
                        sma_6 = np.around(sma_6, decimals=5)

                        sma_14 = sma_last_row.get("open_14_sma")
                        sma_14 = float(sma_14)
                        sma_14 = np.around(sma_14, decimals=5)

                        if not sell_sma_trigger:
                            if sma_6 == sma_14:
                                sell_sma_trigger = True
                                print("sell sma trigger activated")
                                break

                    if not sell_sma_trigger:
                        sell_macd_first_trigger = False
                        sell_macd_second_trigger = False
                        sell_macd_third_trigger = False
                        print("Sell Macd triggers have been reseted")

            # check for buy or sell
            if sell_sma_trigger:
                print("checking if to sell")
                while True:
                    stock = get_stockstats_df()
                    stock["open_6_sma"]
                    stock["open_14_sma"]

                    sma_last_row = stock.tail(1)

                    sma_6 = sma_last_row.get("open_6_sma")
                    sma_6 = float(sma_6)
                    sma_6 = np.around(sma_6, decimals=5)

                    sma_14 = sma_last_row.get("open_14_sma")
                    sma_14 = float(sma_14)
                    sma_14 = np.around(sma_14, decimals=5)

                    if (sma_6 < sma_14) and (abs(sma_6 - sma_14) >= 0.00001):
                        ACTION = "put"
                        iq.buy(money, goal, ACTION, expirations_mode)
                        print("sell bid placed\n")
                        sell_macd_first_trigger = False
                        sell_macd_second_trigger = False
                        sell_macd_third_trigger = False
                        sell_sma_trigger = False
                        break

    def get_buy_process(self):
        buy_process = Process(target=self.buy_function)
        return buy_process

    def get_sell_process(self):
        sell_process = Process(target=self.sell_function)
        return sell_process


bot = dankiq()
buy_process = bot.get_buy_process()
sell_process = bot.get_sell_process()
buy_process.start()
sell_process.start()
