class DataStructure:
    def __init__(self, dataSourceID=None, type=None, symbol=None, market=None, strike_price=None, expiry_date=None, date=None, time=None, datetime=None, index=None, open=None, high=None, low=None, close=None, volumn=None, total_volumn=None, error=None, done=None):
        self.dataSourceID = dataSourceID
        self.type = type
        self.symbol = symbol
        self.market = market
        self.strike_price = strike_price
        self.expiry_date = expiry_date
        self.date = date
        self.time = time
        self.datetime = datetime
        self.index = index
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volumn = volumn
        self.total_volumn = total_volumn
        self.error = error
        self.done = done