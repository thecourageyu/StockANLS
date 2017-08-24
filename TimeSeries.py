

# -*- coding: utf-8 -*-

import codecs
import math
import matplotlib
matplotlib.use("AGG")
import matplotlib.pyplot as plt
plt.style.use("ggplot")
import numpy as np
import os
import pandas as pd
import re
from datetime import datetime as dt
from datetime import timedelta as td

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

#=======================
# get Pres time series
#=======================
InputPath = "REF/Pres20170819/ForEachID"
fnames = os.listdir(InputPath)

PresMM = ["00", "10", "20", "30", "40", "50", "[0-9]{2}"]
PresMM = ["00", "10", "20", "30", "40", "50"]
for MM in PresMM:

    print(MM)
    OutputPath = "TSplot_" + MM
    if not os.path.exists(OutputPath):
        os.makedirs(OutputPath)

    for ID in StaInfo["StaID"]:
        reform = "PPQC_" + str(ID) + "_(" + MM + ").txt"
        reobj = re.compile(pattern=reform)
        files = []
        for tmp in fnames:
            m = reobj.match(tmp)
            if m is not None:
                files.append(m.group(0))

        if len(files) == 1:
            myfile = InputPath + "/" + files[0]
            fname = codecs.open(myfile, encoding='utf-8')
            #PresInfo = pd.DataFrame(np.loadtxt(fname, dtype={"names":("yyyymmddhh", "Pres", "Est", "ErrCode"), "formats":("i8", "f8", "f8", "i4")}, skiprows=1, usecols=[1, 2, -2, -1]))
            PresInfo = np.loadtxt(fname, dtype={"names": ("yyyymmddhh", "Pres", "Est", "ErrCode"), "formats": ("i8", "f8", "f8", "i4")}, skiprows=1, usecols=[1, 2, -2, -1])
            #PresInfo = pd.DataFrame(np.loadtxt(fname, dtype=np.float64, skiprows=1, usecols=[1, 2, -2, -1]))
            #PresInfo.columns = ["yyyymmddhh", "Pres", "Est", "ErrCode"]
            x = PresInfo["Pres"]
            y = PresInfo["Est"]
            err = PresInfo["ErrCode"]
            xtick = PresInfo["yyyymmddhh"]
            #xtick = np.array(PresInfo["yyyymmddhh"].apply(lambda x: str(int(x))))

            #xtick[np.where(x < 0)] = np.nan
            #err[np.where(x < 0)] = np.nan

            x[np.where(x < 0)] = np.nan
            y[np.where(y < 0)] = np.nan
            errposi = [idx for idx, tmp in enumerate(err) if tmp == 1]
            errpts = np.ones(len(err)) * np.nan
            errpts[errposi] = x[errposi]

            optname = OutputPath + "/Pres_QC_" + ID + ".png"
            #TSplot(x[np.where(y > 0)], s1=y[np.where(y > 0)], pts1=errpts[np.where(y > 0)], xlab="date", ylab="Pres(hPa)", title=ID, xtick=xtick[np.where(y > 0)], file=optname)
            TSplot(x, s1=y, pts1=errpts, xlab="date", ylab="Pres(hPa)", title=ID, xtick=xtick, file=optname)
        #elif len(files) > 1:
        else:
            print(str(ID) + " files doesn't exist!")

#=======================
# get Tx time series
#=======================
InputPath = "REF/TOMP20170808"
fnames = os.listdir(InputPath)

TxMM = ["00", "10", "20", "30", "40", "50"]
sdate = "201704130250" # yyyymmddHHMMSS
if str(int(sdate) - math.floor(int(sdate) / 10**2) * 10**2).zfill(2) not in TxMM:
    print("reset MM of yyyymmddHHMMSS")
edate = "201704301250"
sdt = dt.strptime(sdate, "%Y%m%d%H%M")
edt = dt.strptime(edate, "%Y%m%d%H%M")
dtobj = sdt
ndate = 0
while dtobj <= edt:
    ndate = ndate + 1
    dtobj = dtobj + td(minutes=10)

Tx = np.ndarray(shape=(ndate, 6, nSta)) # dim2: obs, est, est_c, sd, errcode, est_1
Tx.fill(-999.0)
dtobj = sdt
dates = []
dateidx = 0
while dtobj <= edt:

    fname = InputPath + "/bias_" + dt.strftime(dtobj, "%Y%m%d%H%M") + ".txt"
    dates.append(dt.strftime(dtobj, "%Y%m%d%H%M"))
    print(dates[-1])
    dtobj = dtobj + td(minutes=10)
    dateidx = dateidx + 1
    try:
        TxInfo = np.loadtxt(fname, dtype={"names": ("StaID", "obs", "est", "est_c", "sd", "errcode", "est_1"), "formats": ("a6", "f8", "f8", "f8", "f8", "i4", "f8")}, skiprows=1)
    except:
        continue

    for idx3, tmpID1 in enumerate(TxInfo["StaID"]):
        for idx2, tmpID2 in enumerate(StaInfo["StaID"]):
            if tmpID2 == tmpID1.decode():
                for idx1 in range(6):
                    Tx[dateidx, idx1, idx2] = TxInfo[idx3][idx1 + 1]



OutputPath = "TxTSplot"
if not os.path.exists(OutputPath):
    os.makedirs(OutputPath)

for idx, ID in enumerate(StaInfo["StaID"]):

    obs = Tx[:, 0, idx]
    est = Tx[:, 1, idx]
    est_c = Tx[:, 2, idx]
    sd = Tx[:, 3, idx]
    err = Tx[:, 4, idx]
    est_1 = Tx[:, 5, idx]
    xtick = np.array(dates)
    # xtick = np.array(PresInfo["yyyymmddhh"].apply(lambda x: str(int(x))))

    # xtick[np.where(x < 0)] = np.nan
    # err[np.where(x < 0)] = np.nan
    obs[np.where(obs < -90.0)] = np.nan
    est_c[np.where(est_c < -90.0)] = np.nan
    errposi = [idx for idx, tmp in enumerate(err) if tmp == 1]
    errpts = np.ones(len(err)) * np.nan
    errpts[errposi] = obs[errposi]

    optname = OutputPath + "/Tx_QC_" + ID + ".png"
    # TSplot(x[np.where(y > 0)], s1=y[np.where(y > 0)], pts1=errpts[np.where(y > 0)], xlab="date", ylab="Pres(hPa)", title=ID, xtick=xtick[np.where(y > 0)], file=optname)
    TSplot(obs, s1=est_c, s2=est_c-3*sd, s3=est_c+3*sd, pts1=errpts, pts2=obs, pts3=est_c, xlab="date", ylab="Temp(C)", xtick=xtick, title=ID, file=optname)
    #TSplot(obs, s1=est, pts1=errpts, xlab="date", ylab="Temp(C)", title=ID, xtick=xtick, file=optname)
# elif len(files) > 1:

#=======================================
# a time series plot function
#=======================================
def TSplot(*positional, **keywords):
    # *positional is a tuple. **keywords is a dict.
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
    if nobs<=5:
        print("nobs = ", nobs)
        return
    plt.ioff()
    plt.figure(figsize = (12,10))
    #plt.subplots()
    #plt.subplots_adjust(bottom=0.2)
    p, = plt.plot(x, y, zorder=10, alpha=0.5)
    axes = plt.gca()
    #axes.set_xlim([min(x) - 1, max(x) + 1])
    plt.xlim([min(x) - 10, max(x) + 10])
    handles = [p]
    labels = ["obs"]
    if "s1" in keywords.keys():
        p1, = plt.plot(x, keywords["s1"], zorder=3)
        handles.append(p1)
        labels.append("est")
    if "s2" in keywords.keys():
        p2, = plt.plot(x, keywords["s2"], zorder=2)
        handles.append(p2)
        labels.append("line2")
    if "s3" in keywords.keys():
        p3, = plt.plot(x, keywords["s3"], zorder=1)
        handles.append(p3)
        labels.append("line3")
    if "pts1" in keywords.keys():
        pts1 = plt.scatter(x, keywords["pts1"], color="#000000", zorder=11, alpha=0.5, marker="o")
        handles.append(pts1)
        labels.append("err")
    if "pts2" in keywords.keys():
        pts2 = plt.scatter(x, keywords["pts2"], alpha=0.5, marker="o")
        #handles.append(pts2)
        #labels.append("pt2")
    if "pts3" in keywords.keys():
        pts3 = plt.scatter(x, keywords["pts3"], alpha=0.5, marker="o")
        # handles.append(pts3)
        # labels.append("pt3")
    if "xtick" in keywords.keys():

        posi = [tmp for tmp in range(0, nobs, int(nobs / 5.0))]
        print(posi)
        print(x[posi])
        print(keywords["xtick"][posi])
        #if (nobs - 1) not in posi: posi.append(nobs - 1)
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

    plt.xticks(rotation=45)
    plt.legend(handles=handles, labels=labels, loc="best")
    #plt.legend(handles=handles, labels=labels, loc="lower left")

    if "file" in keywords.keys():
        plt.savefig(keywords["file"])
    else:
        plt.savefig("TSplot.png")
    plt.close()

x = np.linspace(-5, 5, 100)
y = np.random.normal(0, 1, 100)
z = np.random.exponential(3,100)

TSplot(y, s1=z, pts1=x, xlab=r"date", ylab=r"Pres(hPa)", title=r"Pres", file="test4.png")
TSplot(y)
