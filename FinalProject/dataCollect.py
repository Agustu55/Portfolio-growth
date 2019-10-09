import pandas_datareader as web
import os
from datetime import datetime

## used to collect CSV files from a list of stocks. Mostly for local testing.

directoryPath = 'Data'
fileList = os.listdir(directoryPath)
for fileName in fileList:
    os.remove(directoryPath + "/" + fileName)

startDate = datetime(1971,2,4)
endDate = datetime.today()

file = open('stockList.txt','r')

stockList = {}
for i in range (40): ## 20 stocsk, stock + company name
    if i % 2 == 0:
        stockList[file.readline().rstrip()] = file.readline().rstrip()

print(stockList)

tickers = stockList.keys()

print(tickers)

for ticker in tickers:
    df = web.DataReader(ticker,'yahoo',startDate,endDate)
    df.to_csv('Data/'+ticker+'.CSV')
    print('success:',ticker)


