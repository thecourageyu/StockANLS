import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROUTINE = "ROUTINE"
inpath = "C:/Users/YuZhe/AppData/Local/lxss"
inpath = "E:\LinuxHub\data"


class StockData():
    def __init__(self, symbol):
        self.symbol = symbol

    def cksymbol(self):
        print(self.symbol)

    def readdata(self):
        filename = inpath + "/" + str(self.symbol) + ".csv"
        pd.read_table(filename)

symbol = "2317"
filename = inpath + "/" + str(symbol) + ".csv"
c = pd.read_table(filename, sep=",", header=None)
colname = ["date", "shares", "price", "open", "high", "low", "close", "diff", "num"]
c.columns = colname
c.date[1]

a = StockData("2317")
b = a.readdata()