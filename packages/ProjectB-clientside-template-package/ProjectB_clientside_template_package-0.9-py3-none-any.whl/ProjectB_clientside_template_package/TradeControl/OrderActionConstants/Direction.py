from enum import Enum


class Direction(Enum):
    CALL = "CALL"
    PUT = "PUT"
    
    def getDirection(self):
        return self.value