import datetime
import sys
import time
import sqlite3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # 瀏覽器配置
from selenium.webdriver.support.ui import WebDriverWait  # 等待工具
from selenium.webdriver.support import expected_conditions  # 預定義條件，供 WebDriverWait 使用
from selenium.webdriver.common.by import By  # 定位元素
# Selenium v4 compatible Code Block
# https://stackoverflow.com/questions/64717302/deprecationwarning-executable-path-has-been-deprecated-selenium-python
from selenium.webdriver.chrome.service import Service
import pandas as pd
import yfinance as yf
import talib
import csv
from db_select import *
# 目前日期
current_date = datetime.date.today()  # 這裡改成今天的日期

# stock_tw = []
# for i in stock_id:
#     stock_tw.append(f"{i}.TW")

# 策略設計
# 步驟1: 獲取股價數據
# def get_stock_data(symbol, start_date):
#     stock_data = yf.download(symbol, start=start_date)
#     return stock_data
def get_stock_data():
    stock_data = select_data()
    return stock_data

# 步驟2: 計算技術指標
def calculate_technical_indicators(data):
    # RSI (相對強弱指標)
    data['RSI'] = talib.RSI(data['Adj Close'], timeperiod=14)


    # MA20 (移動平均線)
    data['MA20'] = talib.SMA(data['Adj Close'], timeperiod=20)


    # MA50 (移動平均線)
    data['MA50'] = talib.SMA(data['Adj Close'], timeperiod=50)


    # MACD (移動平均收斂與分歧)
    data['MACD'], data['Signal_Line'], _ = talib.MACD(data['Adj Close'], fastperiod=12, slowperiod=26, signalperiod=9)


    # KD (隨機指標)
    data['K'], data['D'] = talib.STOCH(data['high'], data['low'], data['Adj Close'], fastk_period=9, slowk_period=3, slowd_period=3)


    return data


# 步驟3: 制定交易策略
def generate_signals(data):
    # 這裡你可以根據你的策略定義買入和賣出的條件
    # 這只是一個簡單的例子，實際的策略可能會更複雜
    signals = pd.DataFrame(index=data.index)
   
    # 買入條件1：RSI小於30
    buy_condition1 = (data['RSI'] < 30)


    # 買入條件2：價格在今天的MA20金叉MA50
    buy_condition2 = (data['MA20'] > data['MA50']) & (data['MA20'].shift(1) < data['MA50'].shift(1))


    # 買入條件3：MACD金叉, MACD第二個條件是用來確保前一天跟今天發生金叉
    buy_condition3 = (data['MACD'] > data['Signal_Line']) & (data['MACD'].shift(1) < data['Signal_Line'].shift(1))


    # 買入條件4：隨機指標K穿越D
    buy_condition4 = (data['K'] > data['D']) & (data['K'].shift(1) < data['D'].shift(1)) & (data['K'] < 20)


    # 買入條件達成的數量
    signals['Buy_Conditions_Met'] = buy_condition1.astype(int) + buy_condition2.astype(int) + buy_condition3.astype(int) + buy_condition4.astype(int)


    signals['Buy_Signal'] = signals['Buy_Conditions_Met'] >= 2


    # 賣出條件1：RSI大於70
    sell_condition1 = (data['RSI'] > 70)


    # 賣出條件2：價格在今天的MA20死叉MA50
    sell_condition2 = (data['MA20'] < data['MA50']) & (data['MA20'].shift(1) > data['MA50'].shift(1))


    # 賣出條件3：MACD死叉, MACD第二個條件是用來確保前一天跟今天發生死叉
    sell_condition3 = (data['MACD'] < data['Signal_Line']) & (data['MACD'].shift(1) > data['Signal_Line'].shift(1))


    # 賣出條件4：隨機指標K穿越D，且目前處於超買區域
    sell_condition4 = (data['K'] < data['D']) & (data['K'].shift(1) > data['D'].shift(1)) & (data['K'] > 80)


    # 賣出條件達成的數量
    signals['Sell_Conditions_Met'] = sell_condition1.astype(int) + sell_condition2.astype(int) + sell_condition3.astype(int) + sell_condition4.astype(int)


    signals['Sell_Signal'] = signals['Sell_Conditions_Met'] >= 2


    # signals = signals[signals.any(axis=1)]


    return signals


# 步驟4: 主程式
def main():
    total_signal = pd.DataFrame()
    total_stock_data = []
    for symbol in select_stock_n():
        # 設定參數
        # 股票代號
        try:
            today_date = datetime.date.today()
            previous_date = today_date - datetime.timedelta(days=1)
            start_date = previous_date


            # 獲取股價數據
            stock_data = stock_data


            # 計算技術指標
            stock_data = calculate_technical_indicators(stock_data)


            # 生成交易信號
            signals = generate_signals(stock_data)


            signals.reset_index(inplace=True)
            signals['symbol_with_date'] = signals['Date']
            signals['SYMBOL'] = symbol  # 寫入股票代號
            signals['symbol_with_date'] = signals.apply(lambda row: f"{row['Date'].strftime('%Y-%m-%d')}_{row.name}_{row['SYMBOL']}", axis=1)
            signals.set_index('symbol_with_date', inplace=True)
            # print(signals.index)
            total_signal = pd.concat([total_signal, signals])
            total_stock_data.append(stock_data)
        except Exception as e :
            continue

        # 顯示交易信號
        # print(symbol)
        # print(signals[signals['Buy_Signal'] | signals['Sell_Signal']])

    print(total_signal)
    # 合併列表中的 DataFrame
    combined_signal = pd.DataFrame(total_signal)
    combined_signal.to_csv('origin_combine.csv')
    combined_signal = combined_signal[combined_signal['Buy_Signal'] | combined_signal['Sell_Signal']]


    combined_signal = combined_signal.reindex(["SYMBOL","Date","Buy_Conditions_Met","Buy_Signal","Sell_Conditions_Met"], axis="columns")
    # 修改這行程式碼
    combined_stock_data = pd.concat(total_stock_data, axis=0)
    # combined_stock_data = pd.DataFrame(total_stock_data, axis=1)
    # 寫入 CSV 文件
    print(combined_stock_data)
    # print(combined_signal)


    absolute_path = 'C:\\Users\\Victor\\Desktop\\sideProject\\python\\result.csv'
    combined_signal.to_csv(absolute_path, index=False)
    # combined_stock_data.to_csv('source.csv', index=False)


if __name__ == "__main__":


    main()