#global modules import
import socket
import json
import logging
import os
import time

#own-modules import statement
from command import Command, CommandStatus
from vizrtCommands import VizrtCommands
from TCPServer import TCPServer

class VizrtGateway:

    def __init__(self,config):
        serverAddress = (str(config["ServerIP"]), int(config["ServerPort"]))
        self.sockDriver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sockDriver.connect(serverAddress)
        except Exception as e:
            logging.error(str(e))
        self.vizrtCommands = VizrtCommands(config["VizrtEmptyScenePath"])
        self.VizrtVersion = self.getVersion()
        self.loadedScenes = {"FRONT_LAYER": "", "MIDDLE_LAYER": "", "BACK_LAYER": ""}
    
    def hide(self, command):
        try:
            self.sockDriver.sendall(self.vizrtCommands.hideLayerSceneCommand(command.layer))
            if len(layer) != 0:
                self.loadedScenes[str(command.layer)] = ""
            else:
                self.loadedScenes['MIDDLE_LAYER'] = ""
            response = str(Response(str(self.sockDriver.recv(1024), encoding='utf-8'), ResponseType.Success), encoding='utf-8')
            return response
        except Exception as e:
            logging.error(str(e))
            
    def show(self, command):
        if len(command.items) == 0:
            try:
                self.sockDriver.sendall(self.vizrtCommands.showLayerSceneCommand(command.layer, command.scene))
                if len(command.layer) != 0:
                    self.loadedScenes[str(command.layer)] = str(command.scene)
                else:
                    self.loadedScenes['MIDDLE_LAYER'] = str(command.scene)
                command.status = CommandStatus.Sent
            except Exception as e:
                logging.error(str(e))
                command.status = CommandStatus.Failed
        else:
            for item in command.items:
                #TEXT ITEM
                if item['Visibility'] == "true":
                    try:
                        self.sockDriver.sendall(self.vizrtCommands.showLayerSceneCommand(command.layer, command.scene))
                        self.sockDriver.sendall(self.vizrtCommands.setLayerItemText(command.layer, command.scene, item['Name'], item['Text']))
                        command.status = CommandStatus.Sent
                    except Exception as e:
                        logging.error(str(e))
                if item['Visibility'] == "false":
                    try:
                        self.sockDriver.sendall(self.vizrtCommands.hideLayerItem(command.layer, item['Name']))
                        command.Status = CommandStatus.Sent
                    except Exception as e:
                        logging.error(str(e))
  
    def getVersion(self):
        self.sockDriver.sendall(self.vizrtCommands.getVersionCommand())
        response = str(self.sockDriver.recv(1024), encoding='utf-8')[11:]
        response = response.rstrip("\x00")
        return response

    def executeCommand(self, command):
        response = "{'Response':'Unsupported command'}"
        if command.type == "Hide":  
            response = self.hide(command)
        elif command.type == "Show":
            response = self.show(command)   
        response = response.rstrip("\x00") 
        return response
        
