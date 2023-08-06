from abc import ABC, abstractmethod
import datetime
from ProjectB_clientside_template_package.ClientSocketControl.SocketClient import SocketClient
from ProjectB_clientside_template_package.ClientSocketControl.DataStructure import DataStructure
from ProjectB_clientside_template_package.TradeControl.OrderActionConstants.Action import Action
from ProjectB_clientside_template_package.TradeControl.TradeController import TradeController

import json

class MainController(ABC):
    
    dataStreaming = None
    dataStreamingRequest = None
    tradeController = None
    
    def login(self, loginname, password):
        try:
            self.dataStreaming = SocketClient(loginname, password)
        except:
            self.dataStreaming = None
            raise Exception("Login fail")
    
    def createDataStreamingRequest(self, dataStreamingRequest):
        if(self.dataStreaming is None):
            raise Exception("Please login first");
        else:
            self.dataStreaming.request(dataStreamingRequest)
            
    def projectBTradeController(slippageRangeInPercentage):
        tradeController = TradeController()
        tradeController.setSlippage(0.0005)
    
    @abstractmethod
    def logicHandler(datastructure:DataStructure):
        pass
        
    def run(self):
        while True:
            #get the response
            response = self.dataStreaming.getResponse()
            if response:
                #Convert response JSON message to Python dictionary
                dataStructure_dict = json.loads(response)
                dataStructure = DataStructure(**dataStructure_dict)
                
                #Check response finished or not
                if dataStructure.done:
                    break
                
                #Check error caused or not
                if dataStructure.error:
                    print(dataStructure.error)
                    break
                
                #check the order allow to trade or not
                self.tradeController.tradeCheckingAndBalanceUpdate(dataStructure)
                
                '''
                You may write your back test program below within the while loop
                >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                '''
                
                self.logicHandler(dataStructure);
                
                '''
                <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                '''
    
