import robin_stocks.robinhood as r
import pyotp

totp  = pyotp.TOTP("XILXBFWCNNOMVNZM").now()
login = r.login("","")
watchlist_name="Automated Buys"
stock_list=None

def get_stock_list():
    stock_list = r.build_holdings()
    print("LOG: loading holdings...")
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


def get_watchlists():
    watch_lists=r.account.get_watchlist_by_name(watchlist_name)
    my_list=[]
    print("LOG: print watchlists...")
    for key,value in watch_lists.items():
         print("LOG: printing watchlist:"+watchlist_name + "..."+ "\n")
         for li in value:
            my_list.append(li['symbol'])
    return my_list

def get_open_options():
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

get_alert_IV_options()    
