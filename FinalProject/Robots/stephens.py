
## robot that buys on mondays and sells on firdays. Maintains an 15% cash balance though. Sells all stocks on friday

portfolio = {}
plot = []

def buySellHold(stockName,df,day,shareAmt):
  buydotw = 0
  selldotw = 4
  if df.index[day].weekday() == selldotw:
      return 'sell'
  elif df.index[day].weekday() == buydotw:
      return 'buy'
  else:
       return 'hold'

def buyFunction(df,day,shareAmt,cashAmt,shareBudget,numStocks):
  if cashAmt == 0:
      price = df.iloc[day]['Adj Close']
      position = price * shareAmt
      return cashAmt,shareAmt,position
  else:
      price = df.iloc[day]['Adj Close']

      maxPurchaseAmount = int((shareBudget * (0.85/len(numStocks))/price))
      sharesBought = maxPurchaseAmount
      value = price * sharesBought

      cashAmt = cashAmt - value
      shareAmt = shareAmt + sharesBought
      position = price * shareAmt
      return cashAmt,shareAmt,position


def sellFunction(df,day,shareAmt,cashAmt,shareBudget,numStocks):
  if shareAmt == 0:
      return cashAmt,shareAmt,0.0
  else:
      sharesSold = shareAmt
      price = df.iloc[day]['Adj Close']
      value = price * sharesSold

      cashAmt = cashAmt + value
      shareAmt = shareAmt - sharesSold
      position = price * shareAmt
      return cashAmt,shareAmt,position

## this is the same for all robots
def holdFunction(df, day, shareAmt):
      if shareAmt == 0:
          return 0.0
      else:
          price = df.iloc[day]['Adj Close']
          position = price * shareAmt
          return position