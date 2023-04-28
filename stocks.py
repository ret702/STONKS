import robin_stocks.robinhood as r
import pyotp
from schedule import every, repeat, run_pending
import time
import requests
import pandas as pd
import numpy as np
import yfinance as yf
from threading import Thread
import math
from datetime import date


chain=None

def on_start():
    totp  = pyotp.TOTP("").now()
    login = r.login("","")
    stock_list=None
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
def get_option_high_low(symbol):
    for option in chain:
        print(float(math.fabs(option["strike_price"]) - float(r.stocks.get_latest_price(symbol))))
def get_chain(ticker):
    return chain
def get_stock_list():
    stock_list = r.build_holdings()
    print("LOG: loading holdings...")
    print(stock_list)
    return stock_list
        
def get_profile(key=""):
    profile=r.profiles.load_account_profile()
    if key:
        print("LOG: no portfolio key provided...")
        return profile[key]
    else:
        print("LOG: returning profile...")
        return profile

def get_basic_profile():
    basic_profile=r.profiles.load_basic_profile()
    print("LOG: loading basic profile information...")
    return basic_profile

"""
def buy_stock():
    available_cash=float(get_profile("portfolio_cash"))
    print("LOG: Available Cash "+str(available_cash)+"...")
    stock_list=get_stock_list().items()
    if(available_cash>0):
        for key,value in stock_list:
            print("LOG: current holdings   Key: " + key + "...")
            if(float(value["quantity"])  < 100):
                print("LOG: buying quantity of "+key+" current quantity is "+value["quantity"]+"...") 
                #BUY STOCK HERE
            else:
                li=get_watchlists()
                for item in li:
                    #BUY NEW STOCK ON WATCHLIST HERE
                    print("test")
    else:
        print("LOG: Cash not available")
    return ""

    """


def get_watchlists(watchlist_name):
    watch_lists=r.account.get_watchlist_by_name(watchlist_name)
    my_list=[]
    print("LOG: print watchlists...")
    for key,value in watch_lists.items():
         print("LOG: printing watchlist:"+watchlist_name + "..."+ "\n")
         for li in value:
            my_list.append(li['symbol'])
    return my_list

def get_open_options():
    print("LOG: getting open options...")
    return r.options.get_open_option_positions()

def get_alert_IV_options():
    stock_list=get_stock_list()
    
    for li in stock_list:
        for stock_name,id_stock in stock_list.items():

            stock_id=id_stock['id']
            print("LOG: option chain for stock item "+li+"...")
            print("LOG: stock id  "+stock_id+"...")
            tradeable_options=r.options.find_tradable_options(stock_name)
            for option_chain in tradeable_options:
                try:
                    ##! MATCH STRIKE PRICE WITH GREEKS !##
                    market_data=r.options.get_option_market_data_by_id(option_chain['id'])
                    for data in market_data:
                        print(data)
                        #print(market_data['delta'])
                   
                except:
                    print("hi")
            
    return None
"""positionEffect (str) – Either ‘open’ for a buy to open effect or ‘close’ for a buy to close effect.
creditOrDebit (str) – Either ‘debit’ or ‘credit’.
limitPrice (float) – The limit price to trigger a buy of the option.
stopPrice (float) – The price to trigger the limit order.
symbol (str) – The stock ticker of the stock to trade.
quantity (int) – The number of options to buy.
expirationDate (str) – The expiration date of the option in ‘YYYY-MM-DD’ format.
strike (float) – The strike price of the option.
optionType (str) – This should be ‘call’ or ‘put’
timeInForce (Optional[str]) – Changes how long the order will be in effect for. ‘gtc’ = good until cancelled. ‘gfd’ = good for the day. ‘ioc’ = immediate or cancel. ‘opg’ execute at opening.
jsonify (Optional[str]) – If set to False, function will return the request object which contains status code and headers."""
@repeat(every().day.at("12:00","America/New_York"))
def buy_option(positionEffect,creditOrDebit,price,symbol,
               quantity,expirationDate,strike,optionType,timeInForce,jsonify ):
    buy_option_limit_stop(positionEffect,creditOrDebit,price,symbol,
               quantity,expirationDate,strike,optionType,timeInForce,jsonify)

def buy_option_limit_stop(positionEffect,creditOrDebit,price,symbol,
               quantity,expirationDate,strike,optionType,timeInForce,jsonify):
    r.robinhood.orders.order_buy_option_stop_limit(positionEffect,creditOrDebit,price,symbol,
               quantity,expirationDate,strike,optionType,timeInForce,jsonify)


def historic():
    # Define the ticker symbol and date range
    ticker = "^VIX"
    start_date = "2010-01-01"
    end_date = "2022-04-25"

    # Get the data from Yahoo Finance
    vix_data = yf.download(ticker, start=start_date, end=end_date)

    # Calculate the daily returns
    daily_returns = np.log(1 + vix_data['Adj Close'].pct_change())

    # Calculate the historical volatility
    historical_volatility = daily_returns.std() * np.sqrt(252)

    print(f"The historical volatility of {ticker} is {historical_volatility:.2f}%")

def vix():
    # Define the API endpoint and parameters
    endpoint = "https://www.alphavantage.co/query"
    function = "TIME_SERIES_INTRADAY"
    symbol = "APPL"
    interval = "5min"
    apikey = "YOUR_API_KEY"

    # Define the request URL
    url = f"{endpoint}?function={function}&symbol={symbol}&interval={interval}&apikey={apikey}"

    # Send the request and parse the JSON response
    response = requests.get(url)
    data = response.json()

    # Extract the data from the response and convert it to a DataFrame
    data = data["Time Series (5min)"]
    df = pd.DataFrame.from_dict(data, orient="index")
    df.index.name = "Timestamp"
    df.columns = ["Open", "High", "Low", "Close", "Volume"]

    # Convert the data types and sort the DataFrame by the timestamp
    df = df.astype(float).sort_index()

    print(df)


def start_thread(ticker,period,interval):
    thread = Thread(target = get_live_data, args = (ticker,period,interval))
    thread.start()
    thread.join()

def get_live_data(tickers,period,interval):    
    data= yf.download(tickers=tickers,period=period,interval=interval)
    analyze_data(data)
  

def get_option_chain(ticker):
    global chain
    chain = r.options.find_options_by_expiration(ticker,str(date.today()),"call")
    print(chain)
def analyze_data(data):
    value = 0
    increasing = False
    for x in data["Open"]:
        x = truncate(x,2)
        if(x>value):
            increasing = True
        else:
            increasing = False  
        value = x  
    return increasing

def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n

on_start()
get_live_data("SPY","5m","1m")
get_option_chain("SPY")
get_option_high_low("SPY")

