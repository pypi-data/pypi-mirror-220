import uuid
import random
from datetime import datetime
from typing import List
from ProjectB_clientside_template_package.ClientSocketControl import DataStructure
from ProjectB_clientside_template_package.TradeControl.OrderActionConstants import Action, Direction, ExpiryDate, StrikePrice
from ProjectB_clientside_template_package.TradeControl.Profile import Profile
import json


class Order:
    def __init__(self, symbol, action, direction, sp, ed, quantity, remained, traded, averageTradePrice, lastUpdateDateTime, historyNodeOrNot):
        self.symbol = symbol
        self.orderid = 1
        self.orderDateTime = (datetime.now()).strftime("%Y%m%d%H%M%S")
        self.action = action
        self.direction = direction
        self.sp = sp
        self.ed = ed
        self.quantity = quantity
        if remained is None:
            self.remained = quantity
            self.traded = 0
            self.averageTradePrice = 0
        else:
            self.remained = remained
            self.traded = traded
            self.averageTradePrice = averageTradePrice
        if lastUpdateDateTime is None:
            self.lastUpdateDateTime = self.orderDateTime
        else:
            self.lastUpdateDateTime = lastUpdateDateTime
        if(historyNodeOrNot==False):
            self.history = [json.dumps(self.__dict__)]

    def trade(self, profile: Profile, data: DataStructure, slippage: float) -> json:
        if data.type != "interval":
            if self.direction is None and self.sp is None and self.ed is None:
                if self.remained > 0:
                    temp_trade_amount = min(data.volumn, self.remained)
                    self.traded += temp_trade_amount
                    self.remained -= temp_trade_amount
                    temp_trade_price = data.index + ((data.index * slippage) * (1 if random.randint(0, 1) == 0 else -1))
                    self.averageTradePrice = (self.averageTradePrice + (temp_trade_amount * temp_trade_price)) / self.traded
                    self.history.append(json.dumps(self.__dict__))
                    # Update profile
                    if self.action == "SELL":
                        temp_trade_amount *= -1
                    profile.update(self.symbol, temp_trade_amount, temp_trade_price)
                    return json.dumps(self.__dict__)
        return None