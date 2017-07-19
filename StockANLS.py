#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime as dt




if "-s" in sys.argv:
    symbol = str(sys.argv[sys.argv.index("-s") + 1])

ROUTINE = "ROUTINE"
#inpath = "C:/Users/YuZhe/AppData/Local/lxss"
inpath = "E:\LinuxHub\data"
optpath = "OUTPUT"
#symbol = "3231"

with open(ROUTINE + "/option.txt", "r") as opfile:
    print(opfile.readlines())
    for tmp in opfile.readlines():
        #print(tmp.split("="))
        if str(tmp).split("=")[0].strip() == "INPUT":
            inpath = str(tmp).split("=")[1].strip("\n")
            print(inpath)
        if str(tmp).split("=")[0].strip() == "OUTPUT":
            optpath = str(tmp).split("=")[1].strip("\n")
            print(optpath)

#inpath = "E:\LinuxHub\data"
#optpath = "OUTPUT"


class StockData():
    def __init__(self, symbol):
        self.symbol = symbol


    def cksymbol(self):
        print(self.symbol)

    def read_data(self):
        filename = inpath + "/" + str(self.symbol) + ".csv"
        rawdata = pd.read_table(filename, sep=",", header=None)
        # 每列包含：交易日期、成交股數、成交金額、開盤價、最高價、最低價、收盤價、漲跌價差、成交筆數
        colname = ["date", "shares", "price", "open", "high", "low", "close", "diff", "num"]
        rawdata.columns = colname
        #AD = [[idx, str(int(str(tmp).split("/")[0]) + 1911) + "/" + tmp.split("/")[1] + "/" + tmp.split("/")[2]] for idx, tmp in enumerate(rawdata.date) if int(str(tmp).split("/")[0]) < 1911]
        datelist = []
        for tmp in rawdata.icol(0):
            tmp = str(tmp).split("/")
            if int(tmp[0]) < 1911:
                datelist.append(str(int(tmp[0]) + 1911) + tmp[1] + tmp[2])
            else:
                datelist.append(tmp[0] + tmp[1] + tmp[2])
        datelist = pd.DataFrame({"date": datelist})
        rawdata = pd.concat([datelist, rawdata[colname[1:]]], axis=1)

        #elf.rawdata = rawdata
        return(rawdata)


#symbol = "2317"
#filename = inpath + "/" + str(symbol) + ".csv"
#rawdata = pd.read_table(filename, sep=",", header=None)
#colname = ["date", "shares", "price", "open", "high", "low", "close", "diff", "num"]
#rawdata.columns = colname
#rawdata.date.apply(str)
#datelist = []
#for tmp in rawdata.icol(0):
#    tmp = str(tmp).split("/")
#    if int(tmp[0]) < 1911:
#        datelist.append(str(int(tmp[0]) + 1911) + tmp[1] + tmp[2])
#    else:
#        datelist.append(tmp[0] + tmp[1] + tmp[2])
#datelist = pd.DataFrame({"date": datelist})
#datelist

#pd.concat([datelist, rawdata[colname[1:]]], axis=1)


#symbol = "2317"
#filename = inpath + "/" + str(symbol) + ".csv"
#c = pd.read_csv(filename, sep=",", header=None)
#c
#colname = ["date", "shares", "price", "open", "high", "low", "close", "diff", "num"]
#c.columns = colname
#c.date.apply(str)




#obj = StockData("3231")
obj = StockData(symbol)
stock = obj.read_data()

InvestInfo = []
ckInOut = []
initial = 10**5
threshold = 0.05
idxIn = 0
opt = open(optpath + "/Return_"+ symbol + "_M1.txt", "w")
counts = 0
for idx, tmp in enumerate(stock.date):
    wday = dt.strptime(str(tmp), "%Y%m%d").timetuple().tm_wday
    if idxIn == 0:
        if wday + 1 == 1:
            ckInOut = []
            try:
                ckInOut.append({"date": tmp, "price": float(stock.close[idx]), "idx": idx, "money": initial})
            except:
                continue
            print(ckInOut)
        if wday + 1 == 3 and len(ckInOut) != 0:
            if idx - ckInOut[0]["idx"] == 2:
                try:
                    ckInOut.append({"date": tmp, "price": float(stock.close[idx]), "idx": idx, "money": initial})
                except:
                    continue
                ratio = (ckInOut[1]["price"] - ckInOut[0]["price"]) / ckInOut[0]["price"]
                if ratio >= threshold:
                    idxIn = 1
                    initial = initial - ckInOut[1]["price"] * 1000
                    ckInOut[1]["money"] = initial
                    continue
                elif ratio <= ((-1) * threshold):
                    idxIn = 1
                    ckInOut[1]["money"] = initial
                    continue
            print(ckInOut)
    elif idxIn == 1: # it should add a condition that in Out at the same day.
        #if idx - ckInOut[1]["idx"] == 1:
        try:
            ckInOut.append({"date": tmp, "price": float(stock.close[idx]), "idx": idx, "money": initial})
        except:
            continue
        ratio = (ckInOut[1]["price"] - ckInOut[0]["price"]) / ckInOut[0]["price"]
        if ratio >= threshold:
            idxIn = 0
            initial = initial + ckInOut[2]["price"] * 1000
            ckInOut[2]["money"] = initial
        elif ratio <= ((-1) * threshold):
            idxIn = 0
            initial = initial + (ckInOut[1]["price"] * 1000 - ckInOut[2]["price"] * 1000)
            ckInOut[2]["money"] = initial
        if idxIn == 0:
            counts = counts + 1

            opt.write("*** the {0:>4d}-th buy and sell\n".format(counts))
            opt.write("{0:<9s} {1:<8.2f} {2:<8.2f}\n".format(ckInOut[0]["date"], ckInOut[0]["price"], ckInOut[0]["money"]))
            opt.write("{0:<9s} {1:<8.2f} {2:<8.2f} {3:<8.2f}\n".format(ckInOut[1]["date"], ckInOut[1]["price"], ckInOut[1]["money"], ratio))
            opt.write("{0:<9s} {1:<8.2f} {2:<8.2f}\n".format(ckInOut[2]["date"], ckInOut[2]["price"], ckInOut[2]["money"]))

    #print(a, idx)


opt.close()



dt.strptime("20170109", "%Y%m%d").timetuple()
dt.strptime("20170110", "%Y%m%d").timetuple()

dt.strptime("1060109", "%Y%m%d").timetuple()

# 导入需要的库
import tushare as ts
import matplotlib.pyplot as plt
import matplotlib.finance as mpf

%matplotlib inline

# 设置历史数据区间
date1 = (2014, 12, 1)  # 起始日期，格式：(年，月，日)元组
date2 = (2016, 12, 1)  # 结束日期，格式：(年，月，日)元组
# 从雅虎财经中获取股票代码601558的历史行情
quotes = mpf.quotes_historical_yahoo_ohlc('601558.ss', date1, date2)

# 创建一个子图
fig, ax = plt.subplots(facecolor=(0.5, 0.5, 0.5))
fig.subplots_adjust(bottom=0.2)
# 设置X轴刻度为日期时间
ax.xaxis_date()
# X轴刻度文字倾斜45度
plt.xticks(rotation=45)
plt.title("股票代码：601558两年K线图")
plt.xlabel("时间")
plt.ylabel("股价（元）")
mpf.candlestick_ohlc(ax, quotes, width=1.2, colorup='r', colordown='green')
plt.grid(True)


#import clr

#clr.CompileModules("C:\pyrad\pyrad.dll", "C:\pyrad\setup.py")

#使用ironpython的clr命令即可

< span
style = "font-size:14px;" >  # -- coding: utf-8 --
import requests
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

fig = plt.figure(figsize=(8, 6), dpi=72, facecolor="white")
axes = plt.subplot(111)
axes.set_title('Shangzheng')
axes.set_xlabel('time')
line, = axes.plot([], [], linewidth=1.5, linestyle='-')
alldata = []


def dapan(code):
    url = 'http://hq.sinajs.cn/?list=' + code
    r = requests.get(url)
    data = r.content[21:-3].decode('gbk').encode('utf8').split(',')
    alldata.append(data[3])
    axes.set_ylim(float(data[5]), float(data[4]))
    return alldata


def init():
    line.set_data([], [])
    return line


def animate(i):
    axes.set_xlim(0, i + 10)
    x = range(i + 1)
    y = dapan('sh000001')
    line.set_data(x, y)
    return line


anim = animation.FuncAnimation(fig, animate, init_func=init, frames=10000, interval=5000)

plt.show() < / span >