
## robot that uses Chaikin Money Flow indicator to determine when to buy/sell/hold

portfolio = {}
plot = []
stockNameGlobal = ''


CHMFglobal = {}
lookbackPeriod = 21

## on day 0 calculates the Chaikin indicator per day for the stock. Indicators are stored in a global dictionary with the stock name and array.
## lookback period is 21 days so first 21 day indicators are not calculated. this period can be changed.
def calculateIndicator(df, stockName):
    CHMF = []
    MFMs = []
    MFVs = []
    periodVolumesList = []
    x = lookbackPeriod
    y = lookbackPeriod

    while x < len(df.index):
        periodVolume = 0
        volRange = df.iloc[x - lookbackPeriod: x]['Volume']
        for eachVol in volRange:
            periodVolume += eachVol
        periodVolumesList.append(periodVolume)

        moneyFlowMultiplier = ((df.iloc[x]['Close'] - df.iloc[x]['Low']) - (
                df.iloc[x]['High'] - df.iloc[x]['Close'])) / (df.iloc[x]['High'] - df.iloc[x]['Low'])
        moneyFlowVolume = moneyFlowMultiplier * periodVolume
        MFMs.append(moneyFlowMultiplier)
        MFVs.append(moneyFlowVolume)
        x += 1

    for z in periodVolumesList:
        consider = MFVs[y - lookbackPeriod:y]
        tfsMFV = 0

        for eachMFV in consider:
            tfsMFV = + eachMFV
        tfsCMF = tfsMFV / z
        CHMF.append(tfsCMF)
        y += 1

    global CHMFglobal
    CHMFglobal[stockName] = CHMF



def indicatorDecision(stockName, day, CHMF,shareAmt):  # return CMIDecision, a variable from [0,2] that indicates buy, sell, and hold depending on the Chaikin Money indicator for that day.
    buyMarker = .5
    sellMarker = -.5

    global stockNameGlobal
    stockNameGlobal = stockName

    if CHMF[stockName][day - (lookbackPeriod + 1)] > buyMarker and (shareAmt == 0):  # buy
        CMIDecision = 1
    elif CHMF[stockName][day - (lookbackPeriod + 1)] < sellMarker and shareAmt > 0:  # sell
        CMIDecision = 2
    else:
        CMIDecision = 0  # hold
    return CMIDecision



def buySellHold(stockName, df, day,shareAmt):  # CMIDecision (0,1,2), hold, buy, sell # this is where the the function is pieced together.

    if day < 22:
        if day == 0:
            calculateIndicator(df, stockName)
        return 'hold'

    else:
        global CHMFglobal
        chaikinMoney = CHMFglobal
        decision = indicatorDecision(stockName, day, chaikinMoney, shareAmt)

        if decision == 0:
            return 'hold'
        elif decision == 1:
            return 'buy'
        else:
            return 'sell'


def holdFunction(df, day, shareAmt):  # need to hold for 21 days
    if shareAmt == 0:
        return 0.0
    else:
        price = df.iloc[day]['Adj Close']
        position = price * shareAmt
        return position

def capitalAllocation(day): #return allocationState, a variable from [0,2] that is a proxy for the strength of the signal. A larger signal will indicate more money will be placed on the bet.
   buyMarker = .5

   if CHMFglobal[stockNameGlobal][day - (lookbackPeriod + 1)] > buyMarker and CHMFglobal[stockNameGlobal][day - (lookbackPeriod + 1)] <= .65:
       allocationState = 1
   elif CHMFglobal[stockNameGlobal][day - (lookbackPeriod + 1)] > .65 and CHMFglobal[stockNameGlobal][day - (lookbackPeriod + 1)] <= .80:
       allocationState = 2
   else:
       allocationState = 3

   return allocationState


def buyFunction(df, day, shareAmt, cashAmt, shareBudget, numStocks):
    # per cent of max risk that will be bought
    # 1 = 30%
    # 2 = 50%
    # 3 = 100%

    allocationState = capitalAllocation(day)

    if cashAmt == 0:
        price = df.iloc[day]['Adj Close']
        position = price * shareAmt
        return cashAmt, shareAmt, position
    else:
        price = df.iloc[day]['Adj Close']
        maxRiskPerTrade = int((cashAmt * .10) / price)  # no more than 10% of rtotal capital availiable

        if allocationState == 1:
            sharesBought = .3 * maxRiskPerTrade
        elif allocationState == 2:
            sharesBought = .5 * maxRiskPerTrade
        else:
            sharesBought = maxRiskPerTrade

        value = price * sharesBought

        cashAmt = cashAmt - value
        shareAmt = shareAmt + sharesBought
        position = price * shareAmt
        return cashAmt, shareAmt, position


def sellFunction(df, day, shareAmt, cashAmt, shareBudget, numStocks):
    if shareAmt == 0:
        return cashAmt.shareAmt, 0.0
    else:
        sharesSold = shareAmt
        price = df.iloc[day]['Adj Close']
        value = price * sharesSold

        cashAmt = cashAmt + value
        shareAmt = shareAmt - sharesSold
        position = price * shareAmt
        return cashAmt, shareAmt, position
