
import argparse
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime as dt


import matplotlib.pyplot as plt
plt.style.use("ggplot")
import mpl_finance as mpf
from matplotlib.pylab import date2num

from matplotlib import dates as mdates
from matplotlib import ticker as mticker


from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY
from matplotlib.dates import MonthLocator,MONTHLY
import pylab




if "-s" in sys.argv:
    Symbol = str(sys.argv[sys.argv.index("-s") + 1])

ROUTINE = "ROUTINE"
#inpath = "C:/Users/YuZhe/AppData/Local/lxss"
inpath = "E:/LinuxHub/data"
outpath = "OUTPUT"
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
    def __init__(self, symbol, inpath, outpath, tscale="day"):
        self.symbol = symbol
        self.inpath = inpath
        self.outpath = outpath
        self.filename = self.inpath + "/" + str(self.symbol) + ".csv"
        if not os.path.exists(self.filename):
            print("IOError: " + self.filename + " doesn't exist!")
            return(-1)
        else:
            print("CheckSRC-StockDataClass-45: " + self.filename)

        if not os.path.exists(self.outpath):
            os.makedirs(self.outpath)

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
                #print("Warning-EMA: {0} shows up!".format(CloseSeries[idx]))
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
                #print("Warning-EMA: {0} shows up!".format(CloseSeries[idx]))
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
        EMALong = self._EMA(NLong)

        #EMAReturn = np.zeros(len(EMALong)) * np.nan
        EMAReturn = np.zeros(len(EMALong))
        PriceList = []
        InOut = []
        Holded = 0
        Idx = 0

        for emaquick, emaslow in zip(EMAShort, EMALong):

            if Holded == 0:
                if emaquick > emaslow:

                    try:
                        PriceList.append(float(self.rawdata['close'][Idx]))
                        InOut.append(1)
                        EMAReturn[Idx] = 0
                        Holded = 1
                    except:
                        PriceList.append(np.nan)
                        InOut.append(0)
                        pass
                else:
                    PriceList.append(np.nan)
                    InOut.append(0)
            elif Holded == 1:
                if emaquick < emaslow:

                    try:

                        EMAReturn[Idx] = (float(self.rawdata['close'][Idx]) - PriceList[-1]) / PriceList[-1]

                        PriceList.append(np.nan)
                        InOut.append(0)
                        Holded = 0
                    except:
                        PriceList.append(PriceList[-1])
                        InOut.append(1)
                        pass
                else:
                    PriceList.append(PriceList[-1])
                    InOut.append(1)

            Idx = Idx + 1
        return(EMAReturn, InOut)

    def GetTA(self, NShort=10, NLong=20):
        self._read_data()
        self.EMAQuick = pd.DataFrame({"EMAQuick": self._EMA(NShort)})
        self.EMASlow = pd.DataFrame({"EMASlow": self._EMA(NLong)})

        EMAReturn, HoldStat = self._EMAStratege(NShort, NLong)
        self.EMAReturn = pd.DataFrame({"EMAReturn": EMAReturn})
        self.HoldStat = pd.DataFrame({"HoldStat": HoldStat})
        self.TA = pd.concat([self.rawdata, self.EMAQuick, self.EMASlow, self.EMAReturn, self.HoldStat], axis=1)

        fname = self.outpath + "/TA_" + self.symbol + ".csv"
        self.TA.to_csv(fname, sep=",")

        DataList = []
        x_posi = []
        x_ticks = []
        for SN, EachRow in self.TA.iterrows():
            dtObj = dt.strptime(EachRow["date"], "%Y%m%d")
            date_time = date2num(dtObj)
            x_posi.append(date_time)
            x_ticks.append(EachRow["date"])

            open, high, low, close = EachRow[['open', 'high', 'low', 'close']]

            try:
                DataTuple = (date_time, float(open), float(high), float(low), float(close))
            except:
                DataTuple = (date_time, np.nan, np.nan, np.nan, np.nan)
            DataList.append(DataTuple)

        # 创建子图
        # fig, ax = plt.subplots()
        # fig.subplots_adjust(bottom=0.2)


        Volume = self.TA["volume"]
        qema = self.TA["EMAQuick"]
        sema = self.TA["EMASlow"]
        fig = plt.figure(figsize=(16, 10))
        ax = plt.subplot2grid((4, 4), (0, 0), rowspan=4, colspan=4)
        #ax.xaxis.set_ticks([], [])


        # 设置X轴刻度为日期时间
        ax.xaxis_date()
        plt.yticks()
        plt.title(Symbol)
        plt.ylabel("Price")
        #plt.xlim(x_posi[-1], x_posi[-1])
        #plt.ylim(70, 125)
        mpf.candlestick_ohlc(ax, DataList, width=1.5, colorup='r', colordown='green')

        #plt.plot(x_posi, qema)
        #plt.plot(x_posi, sema)
        plt.grid()
        #ax = plt.subplot2grid((4, 4), (3, 0), rowspan=1, colspan=4)
        #plt.bar(x_posi, Volume)
        #ax.xaxis.set_ticks(x_posi, x_ticks)
        #plt.ylabel("Amount")
        plt.xlabel("Date")

        #plt.xticks(x_posi, x_ticks, rotation=45)
        fname = self.outpath + "/TA_" + self.symbol + ".png"
        plt.savefig(fname)
        return(self.TA)

Symbol = '2317'
obj = StockData(Symbol, inpath, outpath)

stock = obj.GetTA()
fname = outpath + "/TA_" + Symbol + ".csv"


#print(stock)
stock.columns
sum(stock['EMAReturn'])
stock['HoldStat']

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
sys.exit()

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

