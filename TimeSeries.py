
# -*- coding: utf-8 -*-
import datetime as dt
import matplotlib
matplotlib.use("AGG")
import matplotlib.pyplot as plt
plt.style.use("ggplot")
import numpy as np
import os
import pandas as pd
import re

wkdir = "F:/MITDATA"
wkdir = "C:/Users/YJL/Desktop/realtimeQC"
os.chdir(wkdir)

# get StaInfo
stalist = "REF/stalist.txt"
fid = open(stalist, "r")
readobj = fid.readlines()
StaInfo = pd.DataFrame([tmp.split()[0:4] for tmp in readobj])
StaInfo.columns = ["StaID", "lon", "lat", "h"]
nSta = len(StaInfo["StaID"])
fid.close()

# get time series
InputPath = "REF/Pres20170819/ForEachID"
fnames = os.listdir(InputPath)

MM = "10"
MM = "[0-9]{2}"
#reform = "Pres_QC_([0-9]{10})(" + MM + ").txt"
reform = "PPQC_(.{6})_(" + MM + ").txt"
reobj = re.compile(pattern=reform)

MM = "[0-9]{2}"
MM = "20"
for ID in StaInfo["StaID"]:
    reform = "PPQC_" + str(ID) + "_(" + MM + ").txt"
    reobj = re.compile(pattern=reform)
    files = []
    for tmp in fnames:
        m = reobj.match(tmp)
        if m is not None:
            files.append(m.group(0))


    if len(files) == 1:
        PresInfo = pd.DataFrame(np.loadtxt(InputPath + "/" + files[0], dtype=np.str_, usecols=[1, 2, -2, -1]))
        PresInfo.columns = ["yyyymmddhh", "Pres", "Est", "ErrCode"]
        print(PresInfo["Pres"])
        TSplot(x)
    #elif len(files) > 1:
    else:
        print(str(ID) + " files doesn't exist!")




for idx, tmpfile in enumerate(fnames):
    m = reobj.match(tmpfile)
    if m is not None:

        print(tmpfile)

for idx, tmpfile in enumerate(fnames):
    m = reobj.match(tmpfile)
    if m is not None:
        fid = np.loadtxt(InputPath + "/" + tmpfile, dtype=np.str_, skiprows=1, usecols=[0, 1, 2, -2, -1])
        print(fid)


def TSplot(*positional, **keywords):
    if len(positional) == 1:
        nobs = len(positional[0])
        x = np.linspace(1, nobs, nobs)
        y = positional[0]
    elif len(positional) == 2:
        x = positional[0]
        y = positional[1]
        if len(x) == len(y):
            nobs = len(x)
        else:
            print("Warnnig: length of time series is different!")
    plt.ioff()
    plt.subplots()
    plt.plot(x, y)
    if "s1" in keywords.keys():
        plt.plot(keywords["s1"])
    if "s2" in keywords.keys():
        plt.plot(keywords["s2"])
    if "s3" in keywords.keys():
        plt.plot(keywords["s3"])
    if "xtick" in keywords.keys():
        posi = [tmp for tmp in range(0, nobs, int(nobs / 5.0))]
        if nobs not in posi: posi.append(nobs)
        plt.xticks(x[posi], keywords["xtick"][posi])
    if "xlab" in keywords.keys():
        plt.xlabel(keywords["xlab"])
    else:
        plt.xlabel(r"x")
    if "ylab" in keywords.keys():
        plt.ylabel(keywords["ylab"])
    else:
        plt.ylabel(r"y")
    if "title" in keywords.keys():
        plt.title(keywords["title"])
    if "file" in keywords.keys():
        plt.savefig(keywords["file"])
    else:
        plt.savefig("TSplot.png")
    plt.close()



x = np.linspace(-5, 5, 100)
y = np.random.normal(0, 1, 100)
z = np.random.exponential(3,100)

TSplot(y, s1=z, xlab=r"date", ylab=r"Pres(hPa)", title=r"Pres", file="test1.png")
TSplot(y)

def foo(*positional, **keywords):
    #print("Positional:", positional)
    print(type(positional))
    print(len(positional))
    if positional is not ():
        print(positional[0])
    print(type(keywords))
    print("Keywords:", keywords)

x=np.random.rand(10)
y=np.random.normal(10,1,10)

foo(x,y,c='three',d='four')
foo(a='one', b='two', c='three')
