import csv
import datetime
import math
import matplotlib.pyplot as graph
import pandas as pd
import numpy as np

import yfinance as yf
import talib
from numpy import savetxt



pd.set_option("display.max_rows", None, "display.max_columns", None)
##date={}
##close=[]
###futre : add boilinger bands and test if volitily is high or lower and buy options
##def import_csv(path):
##    #only works for yahoo data so far
##    with open(path) as csv_file:
##        reader=csv.reader(csv_file,delimiter=",")
##        local_index=0
##        line_number=0
##        for whole in reader:
##            #print("printing line number " , line_number)
##            line_number+=1
##            if local_index == 0:
##                local_index=1
##                pass
##            else:
##                day=whole[local_index-1]
##                print("measured date  " , whole[local_index-1])
##                format="%Y-%m-%d"
##                values=[]
##                sub_index=0
##                for portion in whole:
##                    if(sub_index==0):
##                        sub_index+=1
##                        pass
##                    else:
##                        price=0.00
##                        price=float(portion)
##                        price=round(price,2)       
##                        values.append(price)
##                date[day]=values
##
##                local_index=0
##
##  
##
##    
##import_csv('C:\\Users\\ret\\Documents\\AAPL.csv')


    
    
##de  get_trending():
##    
##    fut_close_values=[]
##    value=0.00
##    prev_close_value=[]
##    index=0
##
##    for k,v in date.items():
##        fut_close_values.append(float(v[3]))
##
##        close.append(float(v[3]))
##  
##    for key,value in date.items(): #depending on input data, might need to reverse array
##        prev_close_value.append(float(value[3]))
##        #print("index ", index+1)
##        #print("len  ", len(fut_close_values))
##        if(index+1 < len(fut_close_values)):
##            print("Prev close: " ,prev_close_value[index])
##            print("Future close: ", fut_close_values[index+1])
##            #if we are finding trending stocks long term, we need to check prices by week not days
##            try:
##                if  prev_close_value[index] < fut_close_values[index+1]  :
##                    print("Close was greater" ,key)
##          
##                else:
##                    print("Close was lower " , key)
##                    
##                index+=1
##            except Exception as ex:
##                continue
               
def calculate_20d_SMA(data):
    return data['Close'].rolling(window=20).mean()
        


def calculate_50d_SMA(data):
    return data['Close'].rolling(window=50).mean()
        


def plot_20sma(data):
    graph.plot(data)
    graph.title("20 day sma")
    graph.show()

def plot_50sma(data):
    graph.plot(data)
    graph.title("50 day sma")
    graph.show()
        
def get_history(ticker, _period):
    return yf.Ticker(ticker).history(period=_period)


def get_goldenCross(data1,data2,):
    for x,v in zip(data1, data2):
        if(x > v):
            print("GOLDEN CROSS ACHIEVED!")
            print("BUY @", round(x,2))
       


    
##calculate_20d_SMA(close_prices)
##calculate_50d_SMA(close_prices)
close_prices=get_history("msft","1y")
results1=calculate_20d_SMA(close_prices)
results2=calculate_50d_SMA(close_prices)


##plot_20sma()

get_goldenCross(results1,results2)
