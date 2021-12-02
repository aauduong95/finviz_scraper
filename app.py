import finviz

import pandas as pd

from apscheduler.schedulers.blocking import BlockingScheduler

from datetime import datetime

import sqlite3

database = r"/home/alvin/Desktop/py_projects/finviz.db"

tickers = [
    'MSFT', 'AAPL', 'V', 'MA', 'PTON', 'LMT', 'BABA', 'AMD', 'NVDA', 'COST', 'INTC', 'FB', 'CHWY', 'GOOG', 'WM', 'SQ', 'NET', 'DIS', 'ABNB', 'LULU', 'AQN',
'SNOW', 'SHOP', 'CRM', 'AMZN', 'QQQ', 'SPY'
]

''' 
placeholder: 
'''

# list of finviz parameters to scrape
finvizParameters = [
    'Market Cap', 'Income', 'Sales', 'Employees', 'Recom', 'P/E', 'Forward P/E', 'PEG', 'P/S', 'P/B', 'P/C', 'P/FCF', 'Quick Ratio', 'Current Ratio', 'Debt/Eq',
    'LT Debt/Eq', 'SMA20', 'EPS (ttm)', 'EPS this Y', 'EPS next Y', 'EPS past 5Y', 'Sales past 5Y', 'Sales Q/Q',
    'EPS Q/Q', 'SMA50', 'Insider Own', 'Insider Trans', 'Inst Own', 'Inst Trans', 'ROA', 'ROE', 'ROI', 'Gross Margin', 'Oper. Margin', 'Profit Margin', 'Payout',
    'SMA200', 'Short Float', 'Short Ratio', 'Target Price', '52W High', '52W Low', 'RSI (14)', 'Rel Volume', 'Avg Volume', 'Volume', 'Perf Week', 'Perf Month',
    'Perf Quarter', 'Perf Half Y', 'Perf Year', 'Perf YTD', 'Prev Close', 'Price', 'Change', 'Ticker', 'Date Time'
]

def main():

    conn = sqlite3.connect(database)
    print("database connection opened at: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    for ticker in tickers:

        tickerData = finviz.get_stock(ticker) # returns dict

        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        tickerData['Date Time'] = now
        tickerData['Ticker'] = ticker

        tickerDataTrimmed = {k: tickerData[k] for k in finvizParameters} # only obtain parameters listed in finvizParameters

        df = pd.DataFrame([tickerDataTrimmed])
        df.to_sql("stockData", conn, schema=None, if_exists="append", index=True)

        conn.commit()
    
    conn.close()
    print("database connection closed at: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    return

scheduler = BlockingScheduler()
scheduler.add_job(main, 'interval', hours=1)
scheduler.start()
