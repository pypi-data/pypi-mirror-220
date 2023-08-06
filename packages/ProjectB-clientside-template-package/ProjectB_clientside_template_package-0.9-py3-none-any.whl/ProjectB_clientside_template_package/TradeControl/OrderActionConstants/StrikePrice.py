from enum import Enum


class StrikePrice(Enum):
    _100 = 100
    _200 = 200
    
    def getStrikePrice(self):
        return self.value