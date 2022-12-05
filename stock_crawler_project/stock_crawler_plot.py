#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 00:25:58 2022

@author: jus
"""
import crawler_module as m
from time import sleep
import pandas as pd
import matplotlib.pyplot as plt
import mpl_finance as mpf
import talib

all_list = []
stock_symbol, dates = m.get_data()
for date in dates:
    sleep(5)
    try:
        crawler_data = m.crawl_data(date, stock_symbol)
        all_list.append(crawler_data[0])
        df_columns = crawler_data[1]
        print("OK! date = " + date + ",stock_symbol = " + stock_symbol)
    except:
        print("error! date = " + date + ",stock_symbol = " + stock_symbol)

all_df = pd.DataFrame(all_list, columns=df_columns)

# step1 準備data
day = all_df["日期"]
openprice = all_df["開盤價"].astype(float)
closeprice = all_df["收盤價"].astype(float)
high = all_df["最高價"].astype(float)
low = all_df["最低價"].astype(float)
volume = all_df["成交股數"].str.replace(',','').astype(float)

#step 2 製作圖表（主圖）
fig,(ax,ax2) = plt.subplots(2,1,sharex=True,figsize=(24,15),dpi=100)
plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']
ax.set_title(stock_symbol+"K線圖（" + dates[0] + " ～ " + dates[-1] +"）")

#step 3 plot子圖（ax）
mpf.candlestick2_ochl(ax,openprice,closeprice,high,low,width = 0.5,\
                      colorup='r',colordown='g',alpha=0.6)
ax.plot(talib.SMA(closeprice,10),label='10日均線')
ax.plot(talib.SMA(closeprice,30),label='30日均線')
ax.legend(loc="best",fontsize=20)
ax.grid(True)

#step 4 plot子圖（ax2）
mpf.volume_overlay(ax2,openprice,closeprice,volume,\
                      colorup='r',colordown='g',width=0.5,alpha=0.8)
ax2.set_xticks(range(0,len(day),5))
ax2.set_xticklabels(day[::5])
ax2.grid(True)

#step 5 秀圖表
plt.show()