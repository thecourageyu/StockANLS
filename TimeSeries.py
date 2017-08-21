
# -*- coding: utf-8 -*-
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re

wkdir = "F:\MITDATA"
os.chdir(wkdir)
fnames = os.listdir("Pres")
stalist = "stalist.txt"
with open(stalist, "r") as fid:
    for tmp in fid.readlines():
        print(tmp)

x, _ = np.loadtxt(stalist, dtype=np.str_, unpack=True)
pd.read_table(stalist, encoding="utf-8", sep=r"\s+" )

MM = "10"
reform = "Pres_QC_([0-9]{10})(" + MM + ").txt"
reobj = re.compile(pattern=reform)
for idx, tmpfile in enumerate(fnames):
    m = reobj.match(tmpfile)
    if m is not None:
        print(tmpfile)


sdate = "201704100000"
sdt = dtdate
np.loadtxt()


