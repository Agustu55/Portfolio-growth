from datetime import datetime, timedelta
import holidays

## robot that buys before holidays and sells after. Maintains cash balance on inter holiday periods.

portfolio = {}
plot = []

# (datetime.date(2016, 1, 1), "New Year's Day")
# (datetime.date(2016, 1, 18), 'Martin Luther King, Jr. Day')
# (datetime.date(2016, 2, 15), "Washington's Birthday")
# (datetime.date(2016, 5, 30), 'Memorial Day')
# (datetime.date(2016, 7, 4), 'Independence Day')
# (datetime.date(2016, 9, 5), 'Labor Day')
# (datetime.date(2016, 10, 10), 'Columbus Day')
# (datetime.date(2016, 11, 11), 'Veterans Day')
# (datetime.date(2016, 11, 24), 'Thanksgiving')
# (datetime.date(2016, 12, 25), 'Christmas Day')
# (datetime.date(2016, 12, 26), 'Christmas Day (Observed)')

us_holidays = holidays.UnitedStates()

#for ptr in holidays.UnitedStates(years = 2016).items():
#    print(ptr)

buyHolidays = ["New Year's Day","Labor Day","Independence Day","Thanksgiving"]

def buySellHold(share, df, day,budget):
   #print("Date being tested", df.index[day])
   #print("Date being tested+2", df.index[day] + timedelta(days=1))
#    print(day)
   if day < 4:
       return 'hold'
   if us_holidays.get((df.index[day]+ timedelta(days=2)).strftime("%m-%d-%Y")) in buyHolidays:
       return 'buy'
   elif us_holidays.get((df.index[day] - timedelta(days=2)).strftime("%m-%d-%Y")) in buyHolidays:
       return 'sell'
   else:
       return 'hold'

def buyFunction(df,day,shareAmt,cashAmt, shareBudget,tickers):
   if cashAmt == 0:
       price = df.iloc[day]['Adj Close']
       position = price * shareAmt
       return cashAmt,shareAmt,position
   else:
       price = df.iloc[day]['Adj Close']

       maxPurchaseAmt = int(shareBudget/price)
       sharesBought = maxPurchaseAmt
       value = price * sharesBought

       cashAmt = cashAmt - value
       shareAmt = shareAmt + sharesBought
       position = price * shareAmt
       return cashAmt,shareAmt,position

def sellFunction(df, day, shareAmt, cashAmt, shareBudget, tickers):
       if shareAmt == 0:
           return cashAmt, shareAmt, 0.0
       else:
           sharesSold = shareAmt
           price = df.iloc[day]['Adj Close']
           value = price * sharesSold

           cashAmt = cashAmt + value
           shareAmt = shareAmt - sharesSold
           position = price * shareAmt
           return cashAmt, shareAmt, position

def holdFunction(df, day, shareAmt):
       if shareAmt == 0:
           return 0.0
       else:
           price = df.iloc[day]['Adj Close']
           position = price * shareAmt
           return position