
style = "font-size:14px;"
# -- coding: utf-8 --
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
anim
plt.show()


#================================================================
# 导入需要的库
import tushare as ts
import matplotlib.pyplot as plt
import matplotlib.finance as mpf

#% matplotlib
#inline



# 设置历史数据区间
date1 = (2014, 12, 1)  # 起始日期，格式：(年，月，日)元组
date2 = (2016, 12, 1)  # 结束日期，格式：(年，月，日)元组
# 从雅虎财经中获取股票代码601558的历史行情
quotes = mpf.quotes_historical_yahoo_ohlc('^GSPC', date1, date2)

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

#===========##fdassgfdgfdsgfdsgfgfsdadasfsdffdsaf






#dsaf


from matplotlib.pylab import date2num
import datetime

obj = StockData("3231")
stock = obj.read_data()
stock.iterrows()
# 对tushare获取到的数据转换成candlestick_ohlc()方法可读取的格式
data_list = []
for sn, row in stock.iterrows():
    date = row[0]
    # 将时间转换为数字
    date_time = datetime.datetime.strptime(str(date), '%Y%m%d')
    t = date2num(date_time)
    open, high, low, close = [float(tmp) for tmp in row[3:7]]
    datas = (t, open, high, low, close)
    data_list.append(datas)

# 创建子图
fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2)
# 设置X轴刻度为日期时间
ax.xaxis_date()
plt.xticks(rotation=45)
plt.yticks()
plt.title("股票代码：601558两年K线图")
plt.xlabel("时间")
plt.ylabel("股价（元）")
mpf.candlestick_ohlc(ax, data_list, width=1.5, colorup='r', colordown='green')
plt.grid()