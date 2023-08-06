import urllib
import requests
import json
import threading
import socket


class SocketClient:    
    clientID = ""
    apiAccessCode = ""
    serverIPaddress = ""
    serverPort = 0
    JSONrequest = ""
    JSONresponse = []
    

    def __init__(self, loginname, password):
        obj = {'clientID': loginname, 'password': password}
        data = json.dumps(obj).encode('utf-8')
        result = self.post_request('https://www.projectb.click/ProjectB/APIgetAccessCode.php', data)
        if 'type' in result and result['type'] == 'error':
            raise Exception(result['message'])
        else:
            self.clientID = result['clientID']
            self.apiAccessCode = result['accessCode']
            print('Login successful')
            self.get_the_server_ip_address()
    
    def get_the_server_ip_address(self):
        obj = {'clientID': self.clientID, 'apiAccessCode': self.apiAccessCode}
        data = json.dumps(obj).encode('utf-8')
        result = self.post_request('https://www.projectb.click/ProjectB/GetTheServerIPaddress.php', data)
        if 'type' in result and result['type'] == 'error':
            raise Exception(result['message'])
        else:
            self.serverIPaddress = result['ipaddress']
            self.serverPort = result['port']
            print(f'Server {self.serverIPaddress}, Port {self.serverPort} available')
            
    def request(self, request):
        if self.clientID is None or self.apiAccessCode is None:
            raise Exception("No available API access code")
        else:
            self.JSONrequest = request
            self.JSONrequest['clientID'] = self.clientID
            self.JSONrequest['accessCode'] = self.apiAccessCode
            print("Server processing request")
            # Run program
            thread = threading.Thread(target=self.run)
            thread.start()
    
    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.serverIPaddress, int(self.serverPort))
        sock.connect(server_address)
        
        #send request
        sock.send(str(self.JSONrequest).encode())

        #get response
        tempCompleteMessageFromServer = ""
        tempRemainMessageFromServer = ""
        while True:
            messageFromServer = sock.recv(1024*1024*1024)
            messageFromServer = messageFromServer.decode()
            if(messageFromServer is not None):
                messageFromServer = tempRemainMessageFromServer + messageFromServer
                tempCompleteMessageFromServer = messageFromServer[0:messageFromServer.rfind('\n')]
                tempRemainMessageFromServer = messageFromServer[messageFromServer.rfind('\n'):len(messageFromServer)]
                splitMessage = tempCompleteMessageFromServer.split("\n")
                for sm in splitMessage:
                    if(sm is not None):
                        if(sm == "done"):
                            self.JSONresponse.append(None)
                            break
                        self.JSONresponse.append(sm)
            
    def post_request(self, url, data):
        req = urllib.request.Request(url, data, headers={'Content-Type': 'application/json'})
        response = urllib.request.urlopen(req)
        return json.loads(response.read().decode('utf-8'))
                
    def getResponse(self):
        if(len(self.JSONresponse)>0):
            temp_JSONresponse = self.JSONresponse[0]
            self.JSONresponse.pop(0)
            return temp_JSONresponse
        else:
            return ""

