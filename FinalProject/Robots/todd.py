import random
from FinalProject.Robots import RandomBoT

## 8/21 crossover robot

portfolio = {}
plot = []

def buySellHold(stockName,df,day,shareAmt):
   eightDay = df[day-9:day]['Adj Close']
   twentyOneDay = df[day-22:day]['Adj Close']
   nineDay = df[day-10:day]['Adj Close']
   twentyTwoDay = df[day-23:day]['Adj Close']
   if day < 23:
       return 'hold'
   if  eightDay.mean() > twentyOneDay.mean() and nineDay.mean() < twentyTwoDay.mean():
       return 'buy'
   elif eightDay.mean() < twentyOneDay.mean() and nineDay.mean() < twentyTwoDay.mean():
       return 'sell'
   else: return 'hold'


def holdFunction(df, day, shareAmt):
    if shareAmt == 0:
        return 0.0
    else:
        price = df.iloc[day]['Adj Close']
        position = price * shareAmt
        return position

def buyFunction(df, day, shareAmt, cashAmt, shareBudget,numStocks):
    if cashAmt == 0:
        price = df.iloc[day]['Adj Close']
        position = price * shareAmt
        return cashAmt,shareAmt,position
    else:
        price = df.iloc[day]['Adj Close']

        maxPurchaseAmt = int((cashAmt * 0.10)/price)
        if maxPurchaseAmt <= 1:
            position = holdFunction(df, day, shareAmt)
            return cashAmt, shareAmt, position
        sharesBought = random.randint(1,maxPurchaseAmt)
        value = price * sharesBought

        cashAmt = cashAmt - value
        shareAmt = shareAmt + sharesBought
        position = price * shareAmt
        return cashAmt,shareAmt,position


def sellFunction(df,day,shareAmt,cashAmt,shareBudget,numStocks):
    if shareAmt == 0:
        return cashAmt,shareAmt,0.0
    else:
        sharesSold = random.randint(1,shareAmt)
        price = df.iloc[day]['Adj Close']
        value = price * sharesSold

        cashAmt = cashAmt + value
        shareAmt = shareAmt - sharesSold
        position = price * shareAmt
        return cashAmt,shareAmt,position