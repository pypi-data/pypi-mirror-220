from enum import Enum


class Action(Enum):
    BUY = "BUY"
    SELL = "SELL"
    CLOSE = "CLOSE"
    
    def getAction(self):
        return self.value