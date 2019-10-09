import pandas_datareader as web
import os
from datetime import datetime

startDate = datetime(1971,2,4)
endDate = datetime.today()

df = web.DataReader('^GSPC','yahoo',startDate,endDate)
df.to_csv('Nasdaq/^GSPC.CSV')
print('success:','^GSPC')
