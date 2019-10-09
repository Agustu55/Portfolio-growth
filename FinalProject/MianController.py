from datetime import datetime
from FinalProject import DecisionTree
import pandas_datareader as web
from FinalProject.Robots import HoldBoT,RandomBoT,stephens,zach,todd,todd2,Jacob1
import pandas as pd
import matplotlib.pyplot as pt

## THIS IS SUPER SCETCH.... PREFERABLY DON'T KEEP (so that it doesn't show an error when setting numtickers on plot)
import warnings
warnings.filterwarnings("ignore")


startDate = datetime(1971,2,4)
endDate = datetime.today()
youngestStock = startDate

tickers = []
robots = {}

selectRobots = {1:'Hold Only',2:'Random Cat',3:'Holiday Buy/Sell',4:'15% Cash',5:'8/21 Crossover',6:'50 Day Crossover',7:'Chaikin Money Flow'}
keyboardInputRobotEntry = {1:HoldBoT,2:RandomBoT,3:Jacob1,4:stephens,5:todd,6:todd2,7:zach}


stockDataframes = {}

cash = float(input('how much cash do you want to start with?\n'))

stockInput = input('Enter a list of stock tickers (seperated by commas) for your portfolio\n')
stocks = stockInput.split(',')

## cycles through array of tickers provifded by user and gets a dataframe from yahoo. stock dfs are stored in a dictionary were the dataframe can be referenced by
## the ticker name. Start date is constantly updated to the earliest date from the provided stocsk (to save time) but also because
## the start date has to be after the earliest stock.
for stock in stocks:
    df = web.DataReader(stock, 'yahoo', startDate, endDate)
    stockDataframes[stock] = df
    if df.index[0] >= youngestStock:
        youngestStock = df.index[0]
        startDate = youngestStock

print('The youngest stock in your portfolio is',youngestStock.date())

investingDate = (input('Please choose a date that is after your youngest stock to start investing \n'))

print('Please choose which robots you would like to use')
print(selectRobots,'\n')
selectedBots = input('Using the number pad indicate which robots you would like to use (seperated by commas)\n')


## distributes stocks in portfolio evenly accross total holdings
def createHoldPortfolio(cash,stocks,stockDataframes):
    portfolio = {}
    for share in stockDataframes.keys():
        cashAvailable = cash/stocks
        price = stockDataframes[share].iloc[0]['Adj Close']
        sharesBought = cashAvailable/price
        portfolio[share] = [sharesBought,cashAvailable]

    portfolio['cash'] = [0,0.0]
    return portfolio

## creates the portfolio for each robot. the robot has its own portfolio global variable, this is where it is initialized to hold
## a portfolio of stock tickers, all starting with [0shares,0value] the portfolio values are what is updated when the program is run.
def createStandardPortfolio(cash):
    portfolio = {}
    for share in stockDataframes.keys():
        portfolio[share] = [0,float(0)]
    portfolio['cash'] = [cash,cash]
    return portfolio


investingDate = datetime.strptime(investingDate,'%Y-%m-%d')

## creates nasdaq dataframe and slices it at the investing start date (provdied by user).
nasdaq = [0.0, cash]
nasdaqDF = pd.read_csv('Nasdaq/^GSPC.CSV')
nasdaqDF = nasdaqDF.set_index(nasdaqDF['Date'])
nasdaqDF.drop(['Date'], axis=1, inplace=True)
nasdaqDF.index = pd.to_datetime(nasdaqDF.index)
nasdaqDF = nasdaqDF[nasdaqDF.index >= investingDate]
x = nasdaqDF.index.tolist()


## edits size of df for investingDate
for share in stockDataframes.keys():
    df = stockDataframes[share]
    df = df[df.index >= investingDate]
    stockDataframes[share] = df


## creates an dcitionary of robots that hold the robot class that the user selected. This method also calls the create portfolio method
for i in selectedBots:
    if i != ',':
        robot = keyboardInputRobotEntry[int(i)]

        if int(i) == 1:
            robot.portfolio = createHoldPortfolio(cash,len(stocks),stockDataframes)
        else:
            robot.portfolio = createStandardPortfolio(cash)

        robots[robot] = selectRobots[int(i)]

print('you are going to start investing on',investingDate.date(),'with',len(robots),'robots')
print('\n')

## PLOT NASDAQ/S&P LINE ##
line = DecisionTree.createNasdaqPlot(nasdaq,nasdaqDF,cash)
pt.figure(1)
pt.plot(x,line,'k--',label = 'S&P',alpha=0.5)
pt.figure(2)
pt.plot(x,line,'k--',label = 'S&P',alpha=0.5)

colors = ['r','b','g','c','m','y','orange','violet']
i = 0
## runs through the array of robot classes and for each robot performs the start investing method which begins running through every day in the S&P dataframe
## and every stock in the robots portfolio. A cash balance is included in the robots portfolio but not in the stockDataframes
for robot in robots.keys():
    if robots[robot] == 'Hold Only': ## because in most cases if the startdate is early 1980-2000 the hold only strategy will yield crazy returns so two graphs are plotted
        robot.plot = DecisionTree.startInvesting(robot,robot.portfolio,stockDataframes,nasdaqDF)
        pt.figure(2)
        pt.plot(x, robot.plot,colors[i],label=robots[robot])
    else:
        robot.plot = DecisionTree.startInvesting(robot,robot.portfolio,stockDataframes,nasdaqDF)
        pt.figure(1)
        pt.plot(x, robot.plot,colors[i],label=robots[robot])
        pt.figure(2)
        pt.plot(x, robot.plot,colors[i],label=robots[robot])
    print('success:',robots[robot])
    i += 1

print('\n')
print('**********************************************************')
value = int(round(nasdaqDF.iloc[-1]['Adj Close'] * cash))
print('S&P value:','$'+format(value, ',d'))
print('***************** portfolio values today *****************')
for robot in robots.keys():
    value = int(round(robot.plot[-1]))
    print(robots[robot]+':','$'+format(value,',d'))
print('**********************************************************')

pt.figure(1)
pt.title(stocks)
pt.locator_params(numticks=12)
pt.legend(loc='upper left')

pt.figure(2)
pt.title(stocks)
pt.locator_params(numticks=12)
pt.legend(loc='upper left')

pt.show()
