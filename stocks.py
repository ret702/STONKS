import robin_stocks.robinhood as r
import pyotp
from schedule import every, repeat, run_pending
import time

totp  = pyotp.TOTP("").now()
login = r.login("","")

stock_list=None


def on_start():
     while True:
        schedule.run_pending()
        time.sleep(1)

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
    buy_option_limit_stop()

def buy_option_limit_stop():
    r.robinhood.orders.order_buy_option_stop_limit(positionEffect,creditOrDebit,price,symbol,
               quantity,expirationDate,strike,optionType,timeInForce,jsonify)

on_start()
   

