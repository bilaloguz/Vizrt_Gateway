#global modules import
import socket
import json
import logging
import os
import importlib
import datetime
import psutil

#own-modules import statement
from command import Command
from TCPServer import TCPServer
from vizrtGateway import VizrtGateway
from channelportGateway import ChannelportGateway

class Gateway:

    def __init__(self):
        self.tcpServerCreated = False
        

        
    def run(self):
        self.TCPServer.run()

    def setConfig(self, config):
        print("SETCONFIG")
        
        if (self.tcpServerCreated):
            print("Stopping TCP Server")
            self.TCPServer.stop()
        
        if config['ServerType'].lower() == "vizrt":
            self.gateway = VizrtGateway(config)
        elif config['ServerType'].lower() == "channelport":
            self.gateway = ChannelportGateway(config)
        self.listenPort = int(config["ListenerPort"])
        logging.basicConfig(level=logging.INFO, filename="Graphic_Gateway.log", format="%(asctime)s::%(message)s")
        self.TCPServer = TCPServer(self.listenPort, self.dataReceived)
        self.tcpServerCreated = True

    def dataReceived(self, receivedData, dataToSend):
        responseData = ""
        response = {}
        try:
            command = Command(receivedData)
            if command.type == "CheckStatus":
                graphicVersion = self.gateway.getVersion()
                response["GraphicVersion"] = str(graphicVersion)
                response["GatewayVersion"] = "0.1.0"
                response["Time"] = str(datetime.datetime.now())
                responseData = json.dumps(response)   
            else:
                try:
                    responseData = self.gateway.executeCommand(command)
                except Exception as e:
                    logging.error(e)
            if responseData != "":
                dataToSend.append(responseData)
        except Exception as e:
            logging.error(e)
            dataToSend.append("{'Response':'JSON parse error'}")


        
       

