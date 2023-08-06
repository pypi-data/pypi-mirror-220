import math

class BollingerBands:
    def __init__(self, period, multiplier):
        self.prices = []
        self.period = period
        self.multiplier = multiplier
    
    def addPrice(self, price):
        self.prices.append(price)
        if len(self.prices) > self.period:
            self.prices.pop(0)
    
    def getUpperBand(self):
        sma = self.getSMA()
        stdDev = self.getStdDev()
        return sma + (stdDev * self.multiplier)
    
    def getMiddleBand(self):
        return self.getSMA()
    
    def getLowerBand(self):
        sma = self.getSMA()
        stdDev = self.getStdDev()
        return sma - (stdDev * self.multiplier)
    
    def getSMA(self):
        if len(self.prices) < self.period:
            return 0
        return sum(self.prices[-self.period:]) / self.period
    
    def getStdDev(self):
        if len(self.prices) < self.period:
            return 0
        sma = self.getSMA()
        sum = 0.0
        for price in self.prices[-self.period:]:
            diff = price - sma
            sum += diff * diff
        variance = sum / self.period
        return math.sqrt(variance)