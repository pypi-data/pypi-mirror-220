from enum import Enum


class ExpiryDate(Enum):
    _200001 = "200001"
    _200002 = "200002"
    
    def getExpiryDate(self):
        return self.value