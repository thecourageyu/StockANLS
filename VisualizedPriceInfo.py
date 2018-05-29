
import argparse
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime as dt


import matplotlib.pyplot as plt

import mpl_finance as mpf
from matplotlib.pylab import date2num

from matplotlib import dates as mdates
from matplotlib import ticker as mticker

#from matplotlib.finance import candlestick_ohlc
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY
from matplotlib.dates import MonthLocator,MONTHLY
import pylab




if "-s" in sys.argv:
    Symbol = str(sys.argv[sys.argv.index("-s") + 1])

ROUTINE = "ROUTINE"
#inpath = "C:/Users/YuZhe/AppData/Local/lxss"
inpath = "E:/LinuxHub/data"
optpath = "OUTPUT"
Symbol = "3231"


#with open(ROUTINE + "/option.txt", "r") as opfile:
#    print(opfile.readlines())
#    for tmp in opfile.readlines():
#        #print(tmp.split("="))
#        if str(tmp).split("=")[0].strip() == "INPUT":
#            inpath = str(tmp).split("=")[1].strip("\n")
#            print(inpath)
#        if str(tmp).split("=")[0].strip() == "OUTPUT":
#            optpath = str(tmp).split("=")[1].strip("\n")
#            print(optpath)

#inpath = "E:\LinuxHub\data
#optpath = "OUTPUT"


class StockData():
    def __init__(self, symbol, tscale="day"):
        self.symbol = symbol
        self.filename = inpath + "/" + str(self.symbol) + ".csv"
        if not os.path.exists(self.filename):
            print("IOError: " + self.filename + " doesn't exist!")
            return(-1)
        else:
            print("CheckSRC-StockDataClass-45: " + self.filename)

    def PrintSymbol(self):
        print(self.symbol)

    def _read_data(self):
        rawdata = pd.read_table(self.filename, sep=",", header=None)
        # 每列包含：交易日期、成交股數、成交金額、開盤價、最高價、最低價、收盤價、漲跌價差、成交筆數
        colname = ["date", "volume", "amount", "open", "high", "low", "close", "diff", "num"]
        rawdata.columns = colname
        # AD = [[idx, str(int(str(tmp).split("/")[0]) + 1911) + "/" + tmp.split("/")[1] + "/" + tmp.split("/")[2]] for idx, tmp in enumerate(rawdata.date) if int(str(tmp).split("/")[0]) < 1911]

        datelist = []   # a string list
        for tmp in rawdata.iloc[:, 0]:
            tmp = str(tmp).split("/")
            if int(tmp[0]) < 1911:
                datelist.append(str(int(tmp[0]) + 1911) + tmp[1] + tmp[2])
            else:
                datelist.append(tmp[0] + tmp[1] + tmp[2])
        datelist = pd.DataFrame({"date": datelist})
        rawdata = pd.concat([datelist, rawdata[colname[1:]]], axis=1)
        self.rawdata = rawdata

    def _SMA(self, N):
        CloseSeries = np.array(self.rawdata["close"])
        SMA = np.zeros(shape=(CloseSeries.size))
        SMA[0] = CloseSeries[0]
        for idx in range(1, CloseSeries.size, 1):
            K = 1.0 / N
            sidx = idx - N + 1
            if sidx < 0:
                sidx = 0
            try:
                MA[idx] = float(CloseSeries[idx]) * K + EMA[idx - 1] * (1 - K)
            except:
                print("Warning-EMA: {0} shows up!".format(CloseSeries[idx]))
                EMA[idx] = EMA[idx - 1]
            #print(EMA[idx])
        return(EMA)

    def _EMA(self, N):
        CloseSeries = np.array(self.rawdata["close"])
        EMA = np.zeros(shape=(CloseSeries.size))
        EMA[0] = CloseSeries[0]
        for idx in range(1, CloseSeries.size, 1):
            K = 2 / (N + 1)
            try:
                EMA[idx] = float(CloseSeries[idx]) * K + EMA[idx - 1] * (1 - K)
            except:
                print("Warning-EMA: {0} shows up!".format(CloseSeries[idx]))
                EMA[idx] = EMA[idx - 1]
            #print(EMA[idx])
        return(EMA)

    def _EMAStratege(self, N1, N2):
        if N1 < N2:
            NShort = N1
            NLong = N2
        else:
            NShort = N2
            NLong = N1

        EMAShort = self._EMA(NShort)
        print(EMAShort)
        EMALong = self._EMA(NLong)

        #EMAReturn = np.zeros(len(EMALong)) * np.nan
        EMAReturn = np.zeros(len(EMALong))
        PriceList = []
        Holded = 0
        Idx = 0

        for emaquick, emaslow in zip(EMAShort, EMALong):

            if Holded == 0:
                if emaquick > emaslow:
                    print("In: ", emaquick, emaslow)
                    try:
                        PriceList.append(float(self.rawdata['close'][Idx]))

                        EMAReturn[Idx] = 0
                        Holded = 1
                    except:
                        pass
                else:
                    PriceList.append(np.nan)
            elif Holded == 1:
                if emaquick < emaslow:
                    print("exit: ", emaquick, emaslow)
                    try:
                        print("why: ", self.rawdata['close'][Idx], PriceList[-1])
                        EMAReturn[Idx] = (float(self.rawdata['close'][Idx]) - PriceList[-1]) / PriceList[-1]

                        PriceList.append(np.nan)
                        Holded = 0
                    except:
                        PriceList.append(PriceList[-1])
                        pass
                else:
                    PriceList.append(PriceList[-1])

            Idx = Idx + 1
        return(EMAReturn)

    def GetTA(self, NShort, NLong):
        self._read_data()
        self.EMAQuick = pd.DataFrame({"EMAQuick": self._EMA(NShort)})
        self.EMASlow = pd.DataFrame({"EMASlow": self._EMA(NLong)})
        print(type(self.rawdata))
        print(type(self.EMASlow))

        self.EMAReturn = pd.DataFrame({"EMAReturn": self._EMAStratege(NShort, NLong)})
        self.TA = pd.concat([self.rawdata, self.EMAQuick, self.EMASlow, self.EMAReturn], axis=1)
        return (self.TA)

Symbol = '2317'
obj = StockData(Symbol)
obj.symbol
stock = obj.GetTA(10, 20)
#print(stock)
stock.columns
sum(stock['EMAReturn'])
type(stock)
stock['close'][2]
a = obj._EMA(10)
b = obj._EMA(20)
for tmp1, tmp2 in zip(a, b):
    print(tmp1, tmp2)

sum(stock['EMAReturn'])

DataList = []
x_posi = []

for SN, EachRow in stock.iterrows():
    dtObj = dt.strptime(EachRow["date"], "%Y%m%d")
    date_time = date2num(dtObj)
    x_posi.append(date_time)
    open, high, low, close = EachRow[['open', 'high', 'low', 'close']]
    try:
        DataTuple = (date_time, float(open), float(high), float(low), float(close))
    except:
        DataTuple = (date_time, np.nan, np.nan, np.nan, np.nan)
    DataList.append(DataTuple)

# 创建子图
#fig, ax = plt.subplots()
#fig.subplots_adjust(bottom=0.2)

LEMA = obj._EMA(5)
EMA = stock['EMA']
Volume = stock["volume"]
fig = plt.figure(figsize=(24, 8))
ax = plt.subplot2grid((4, 4), (0, 0), rowspan=2, colspan=4)
#ax = plt.gca()
# 设置X轴刻度为日期时间
ax.xaxis_date()
plt.xticks(rotation=45)
plt.yticks()
plt.title(Symbol)
plt.xlabel("Date")
plt.ylabel("Price")
plt.xlim(x_posi[-1]-500, x_posi[-1])
plt.ylim(70, 125)
mpf.candlestick_ohlc(ax, DataList, width=1.5, colorup='r', colordown='green')
plt.grid()
plt.plot(x_posi, LEMA)
plt.plot(x_posi, EMA)
plt.subplot2grid((4, 4), (2, 0), rowspan=1, colspan=4)
plt.bar(x_posi, Volume)

CloseSeries = np.array(stock['close'])
EMA = np.zeros(shape=(CloseSeries.size))
EMA[0] = CloseSeries[0]
N = 10

for idx in range(1, CloseSeries.size, 1):

    K = 2 / (N + 1)

    try:
        EMA[idx] = float(CloseSeries[idx]) * K + EMA[idx - 1] * (1 - K)
    except:
        print("Warning-EMA: {0} shows up!".format(CloseSeries[idx]))
        EMA[idx] = EMA[idx - 1]

#movi

#fig = plt.

# https://zhuanlan.zhihu.com/p/29519040

import tensorflow as tf

# Creates a graph.
a = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2, 3], name='a')
b = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3, 2], name='b')
c = tf.matmul(a, b)
# Creates a session with log_device_placement set to True.
sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
# Runs the op.
print(sess.run(c))
tf.Session(config=tf.ConfigProto(log_device_placement=True))