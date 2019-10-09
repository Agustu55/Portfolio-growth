# import sys
# import pandas_datareader as web
# from datetime import datetime,date
# import random
#
# import pandas as pd
# import holidays
# from dateutil import easter
#
# startDate = datetime(2008,1,1)
# endDate = datetime(2018,12,31)
#
# print(startDate)
# print(endDate)
#
# day = 0
#
# file = open('stockList.txt','r')
# file.readline()
#
# ticker = file.readline().rstrip()
# sNP = web.DataReader('^GSPC','yahoo',startDate,endDate)
# print(sNP)
# print(sNP.index)
# df = pd.read_csv('Nasdaq/^IXIC.CSV')
# df = df.set_index(df['Date'])
# df.drop(['Date'],axis=1,inplace=True)
# df.index = pd.to_datetime(df.index)
# print(df)
#
# sliceDate = datetime(2010,1,1)
# #
# print(df.index)
# #
# dfSlice = df[df.index >= sliceDate]
#
# print(dfSlice)
#
# print(date(2008,12,25) in holidays.US())
#
# print(holidays.US(years=2015))
# print(date(2015,4,3) in holidays.UnitedKingdom())
# print(holidays.UnitedKingdom(years=2015))
#
# print(date(2008,12,25))
# if date(2008,12,25) in holidays.US():
#     holidayName = holidays.US().get(date(2008,12,25))
#
# print(holidayName)
# investmentDate = input('enter a date \n')
# investmentDate = datetime.strptime(investmentDate,'%Y-%m-%d')
# print(investmentDate)


stockInput = input('Enter a list of stock tickers (seperated by commas) for your portfolio\n')
stocks = stockInput.split(',')
print(stocks)
