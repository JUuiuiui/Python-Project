#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 19:38:16 2022

@author: jus
"""
import requests
from io import StringIO
import pandas as pd
import datetime

#讀取設定檔
#在日後變更參數時可不用變更主程式
def get_setting():
    res = []
    try:
        with open('stock.txt') as f:
            slist = f.readlines()
            #使用readlines()的原因是為了要存入list
            print('讀入：',slist)
            a, b, c = slist[0].split(',')
            res = [a, b, c]
    except:
        print('stock.txt讀取錯誤')
    return res

def get_data():
    data = get_setting()
    dates = []
    start_date = datetime.datetime.strptime(data[1],'%Y%m%d')
    end_date = datetime.datetime.strptime(data[2],'%Y%m%d')
    for daynumber in range((end_date-start_date).days+1):
        date = (start_date + datetime.timedelta(days = daynumber))
        if date.weekday()<6:
            dates.append(date.strftime('%Y%m%d'))
    return data[0], dates

def crawl_data(date,symbol):
    #下載股價
    r = requests.get('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date='+date+'&type=ALLBUT0999')
    r_text = [i for i in r.text.split('\n') if len(i.split('",'))==17 and i[0] != '=' ]
    df = pd.read_csv(StringIO("\n".join(r_text)),header= 0)
    
    df = df.drop(columns = ['Unnamed: 16'])
    filter_df = df[df["證券代號"]==symbol]
    filter_df.insert(0,"日期",date)
    return list(filter_df.iloc[0]),filter_df.columns
