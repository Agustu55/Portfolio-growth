import random

## robot that holds every day. never buys / sells
portfolio = {}

def buySellHold(stockName,df,day,shareAmt):
    return 'hold'

## this is the same for all robots
def holdFunction(df,day,shareAmt):
    ## to give amt of stocks based on how much cash per security
    price = df.iloc[day]['Adj Close']
    position = price * shareAmt
    return position



