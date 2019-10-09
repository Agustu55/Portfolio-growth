import random

portfolio = {}
plot = []

## robot chooses when to buy/sell/hold randomly and chooses how much stocks to buy or sell randomly. Only allowed to spend 10% of total cash per share though
## want to return current value of the all owned shares on the date of the transaction

def buySellHold(stockName,df,day,shareAmt):
    value = random.randint(0,2)
    if value == 0: return 'hold'
    elif value == 1: return 'buy'
    else: return 'sell'

## this is the same for all robots
def holdFunction(df,day,shareAmt):
    if shareAmt == 0:
        return 0.0
    else:
        price = df.iloc[day]['Adj Close']
        position = price * shareAmt
        return position

def buyFunction(df,day,shareAmt,cashAmt,shareBudget,numStocks):
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

