from datetime import datetime,timedelta
import pandas as pd
import matplotlib.pyplot as pt
from FinalProject.Robots import HoldBoT,RandomBoT,stephens,zach,todd,todd2,Jacob1
import copy

## creates constant plot for S&P or nasdaq (coded with nasdaq variables because that was what was planned. can be anything)
def createConstantPlots(day,cash,nasdaq,nasdaqDF):
    price =  nasdaqDF.iloc[day]['Adj Close']

    if day == 0:
        shares = cash / price
        nasdaq[0] = shares


    nasdaq[1] = nasdaq[0] * price
    return nasdaq[1]

## cycles through each share provided on the day to call the robots action and buy/sell/hold method
def createInvestmentPlots(robot,day,portfolio,stockDataframes,tickers):
    # print(portfolio)

    daysCash = float(portfolio['cash'][1])
    numStocks = (len((tickers)))
    shareBudget = daysCash/numStocks

    for share in tickers:
        action = robot.buySellHold(share,stockDataframes[share],day,portfolio[share][0] )
        if action== 'hold':
            portfolio[share][1] = robot.holdFunction(stockDataframes[share], day, portfolio[share][0])
        elif action == 'buy':
            portfolio['cash'][1], portfolio[share][0],portfolio[share][1] = robot.buyFunction(stockDataframes[share], day, portfolio[share][0], portfolio['cash'][1],shareBudget,tickers)
        elif action == 'sell':
            portfolio['cash'][1],portfolio[share][0],portfolio[share][1] = robot.sellFunction(stockDataframes[share], day, portfolio[share][0], portfolio['cash'][1],shareBudget,tickers)
        else:
            print(robot,'in else for some stupid reason')

    portfolioValue = 0

    ##value shares (cash included)
    for asset in portfolio.values():
        portfolioValue += asset[1]

    return portfolioValue

## calls constants plot to plot the constant line on the S&P or Nasdaq or any index
def createNasdaqPlot(nasdaq,nasdaqDF,cash):
    plot = []
    for day in range(nasdaqDF.shape[0]):
        nasdaqValue = (createConstantPlots(day,cash,nasdaq,nasdaqDF))
        plot.append(nasdaqValue)

    return plot

## method that cycles through every day in the provided nasdaq dataframe. for every day it calls the create inestment plot with neccessary info passed in.
def startInvesting(robot,portfolio,stockDataframes,nasdaqDF):
    tickers = stockDataframes.keys()

    plot = [] ## an array of portfolio values on the date is returned so each robot has a stored array of portfolio values starting at day 0

    for day in range(nasdaqDF.shape[0]):  # for day in range (10):
        portfolioValue = (createInvestmentPlots(robot,day, portfolio, stockDataframes, tickers))
        plot.append(portfolioValue)


    return plot



#######################    FOR TESTING    ###################################
# startDate = datetime(1971,2,4)
# endDate = datetime.today()
# file = open('stockList.txt','r')
#
#
# tickers = []
# robots = {}
#
# # selectRobots = {1:'Hold Only',2:'Weekly Hold',3:'Random Buy/Sell/Hold',4:'Holiday Buy/Sell',5:'15% Cash',6:'8/21 Crossover',7:'50 Day Crossover',8:'Chaikin Money Flow'}
# # keyboardInputRobotEntry = {1:HoldBoT,2:Jacob2,3:RandomBoT,4:Jacob1,5:stephens,6:todd,7:todd2,8:zach}
#
# selectRobots = {1:'Hold Only',2:'Random Buy/Sell/Hold',3:'Holiday Buy/Sell',4:'15% Cash',5:'8/21 Crossover',6:'50 Day Crossover',7:'Chaikin Money Flow'}
# keyboardInputRobotEntry = {1:HoldBoT,2:RandomBoT,3:Jacob1,4:stephens,5:todd,6:todd2,7:zach}
#
# stockDataframes = {}
#
# cash = 100000
#
#
#
# # stocks = ['HAS','CAT','BF-B','CPB','IP','MRK','SEE','T','ADP','D']
# # stocks = ['HAS','CAT']
# stocks = ['APA']
#
# for stock in stocks:
#     df = pd.read_csv('Data/' + stock + '.CSV')
#     df = df.set_index(df['Date'])
#     df.drop(['Date'], axis=1, inplace=True)
#     df.index = pd.to_datetime(df.index)
#     stockDataframes[stock] = df
#
#
# # selectedBots = '1,2,3,4,5,6,7'
# selectedBots = '1'
# ## distributes stocks in portfolio evenly accross total holdings
# def createHoldPortfolio(cash,stocks,stockDataframes):
#     portfolio = {}
#     for share in stockDataframes.keys():
#         cashAvailable = cash/stocks
#         price = stockDataframes[share].iloc[0]['Adj Close']
#         sharesBought = cashAvailable/price
#         portfolio[share] = [sharesBought,cashAvailable]
#
#     portfolio['cash'] = [0,0.0]
#     return portfolio
#
# def createStandardPortfolio(cash):
#     portfolio = {}
#     for share in stockDataframes.keys():
#         portfolio[share] = [0,float(0)]
#     portfolio['cash'] = [cash,cash]
#     return portfolio
#
#
# investingDate = datetime(2000,1,1)
#
# ##nasdaq part
# nasdaq = [0.0, cash]
# nasdaqDF = pd.read_csv('Nasdaq/^GSPC.CSV')
# nasdaqDF = nasdaqDF.set_index(nasdaqDF['Date'])
# nasdaqDF.drop(['Date'], axis=1, inplace=True)
# nasdaqDF.index = pd.to_datetime(nasdaqDF.index)
# nasdaqDF = nasdaqDF[nasdaqDF.index >= investingDate]
# x = nasdaqDF.index.tolist()
#
#
# ## edits size of df for stardate
# for share in stockDataframes.keys():
#     df = stockDataframes[share]
#     df = df[df.index >= investingDate]
#     stockDataframes[share] = df
#
#
#
# for i in selectedBots:
#     if i != ',':
#         robot = keyboardInputRobotEntry[int(i)]
#
#         if int(i) == 1:
#             robot.portfolio = {}
#             robot.portfolio = createHoldPortfolio(cash,len(stocks),stockDataframes)
#         else:
#             robot.portfolio = {}
#             robot.portfolio = createStandardPortfolio(cash)
#
#         robots[robot] = selectRobots[int(i)]
#
# print('you are going to start investing on',investingDate.date(),'with',len(robots),'robots')
#
# ## PLOT S&P LINE ##
# line = createNasdaqPlot(nasdaq,nasdaqDF,cash)
# pt.figure(1)
# pt.plot(x,line,'k--',label = 'S&P',alpha=0.5)
# pt.figure(2)
# pt.plot(x,line,'k--',label = 'S&P',alpha=0.5)
#
# colors = ['r','b','g','c','m','y','orange','violet']
# i = 0
# for robot in robots.keys():
#     if robots[robot] != 'Hold Only' or robots[robot] != 'Weekly Hold':
#         robot.plot = startInvesting(robot,robot.portfolio,stockDataframes,nasdaqDF)
#         pt.figure(2)
#         pt.plot(x, robot.plot,colors[i],label=robots[robot])
#     else:
#         robot.plot = startInvesting(robot,robot.portfolio,stockDataframes,nasdaqDF)
#         pt.figure(2)
#         pt.plot(x, robot.plot,colors[i],label=robots[robot])
#         pt.figure(1)
#         pt.plot(x, robot.plot, colors[i], label=robots[robot])
#     i += 1
#
#
# print('**********************************************************')
# print('S&P value:',int(round(nasdaqDF.iloc[-1]['Adj Close'] * cash)))
# print('***************** portfolio values today *****************')
# for robot in robots.keys():
#     print(robots[robot]+':',int(round(robot.plot[-1])))
# print('**********************************************************')
#
# pt.figure(2)
# pt.locator_params(numticks=12)
# pt.legend(loc='upper left')
# pt.figure(1)
# pt.locator_params(numticks=12)
# pt.legend(loc='upper left')
#
# pt.show()
