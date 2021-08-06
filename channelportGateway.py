import socket
import json
import logging
import time
import os
from os.path import isfile, join
from xml.dom import minidom

from command import Command, CommandStatus
from channelportCommands import ChannelportCommands
from TCPServer import TCPServer

class ChannelportGateway:

    def __init__(self, config):
        serverAddress = (str(config["ServerIP"]), int(config["ServerPort"]))
        self.sockDriver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sockDriver.connect(serverAddress)
        except Exception as e:
            logging.error(str(e))
        self.scenesPath = config['ChannelportScenesDirectoryPath']
        self.channelportCommands = ChannelportCommands(config["ChannelportScenesDirectoryPath"])
        self.version = self.getVersion()
        self.loadedScenes = {"1": "", "2": "", "3": "", "4":"", "5":"", "6":"", "7":"", "8":""}

    def hide(self, command):
        try:
            self.sockDriver.sendall(self.channelportCommands.hideLayerSceneCommand(command.layer))
            self.loadedScenes[str(command.layer)] = ""
            return response
        except Exception as e:
            logging.error(str(e))
       
    def show(self, command):
        if len(command.items) == 0:
            try:
                self.sockDriver.sendall(self.channelportCommands.showLayerSceneCommand(command.layer, command.scene))
                self.loadedScenes[str(command.layer)] = str(command.scene)
                command.status = CommandStatus.Sent
            except Exception as e:
                logging.error(e)
                command.status = CommandStatus.Failed
        else:
            cutUpCmd = "3" + command.layer + " 0:"
            self.sockDriver.sendall(cutUpCmd.encode('utf-8'))
            self.sockDriver.sendall(self.channelportCommands.showLayerSceneCommand(command.layer, command.scene))
            time.sleep(1)
            items = self.getItems(command.layer)
            for item in command.items:
                if item['Visibility'] == "true":
                    try:
                        fieldID = items[item['Name']]
                        self.sockDriver.sendall(self.channelportCommands.setLayerItemText(command.layer, fieldID, item['Text']))
                        cutDownCmd = "3" + command.layer + " 1:"
                        self.sockDriver.sendall(cutDownCmd.encode('utf-8'))
                        command.status = CommandStatus.Sent
                    except Exception as e:
                        logging.error(e)
                if item['Visibility'] == "False":
                    try:
                        self.sockDriver.sendall(self.channelportCommands.hideLayerItem(command.layer, item['Text']))
                        command.Status = CommandStatus.Sent
                    except Exception as e:
                        logging.error(e)
  
    def getVersion(self):
        received = ""
        try:
            self.sockDriver.sendall(bytes(self.channelportCommands.getVersionCommand()))
            received = str(self.sockDriver.recv(1024), encoding='utf-8')
            received = received.rstrip(received[-1])
        except:
            received = ""
        return str(received[2:])

    def getScenes(self, command):
        sceneFilesList = os.listdir(self.scenesPath)
        scenes = ""
        for sceneFile in sceneFilesList:
                scenes += sceneFile + ","
        scenes = scenes.rstrip(",")
        return scenes

    def executeCommand(self, command):
        response = "{'Response':'Unsupported command'}"
        if command.type == "Hide":  
            response = self.hide(command)
        elif command.type == "Show":
            response = self.show(command)
        elif command.type == "GetScenes":
            response = self.getScenes(command)
        return response
    
    def getItems(self, layer):
        initMsg = "RD " + layer + " 0:"
        self.sockDriver.sendall(initMsg.encode('utf-8'))
        received = str(self.sockDriver.recv(1024))
        bytesStart = int(received[6:9])
        bytesCount = int(received[10:13])
        isFinished = int(received[14:15])
        msg = received[16:-2]
        while isFinished == 1:
            sendMsg = "RD " + str(layer)  + " " + str(bytesCount - 1) + ":"
            self.sockDriver.sendall(sendMsg.encode("utf-8"))
            received = str(self.sockDriver.recv(1024))
            bytesStart = int(received[6:9])
            bytesCount = int(received[10:13])
            isFinished = int(received[14:15])
            msg += received[16:-2]
        mydoc = minidom.parseString(msg)
        components = mydoc.getElementsByTagName('component')
        items = {}
        for component in components:
            items[component.attributes['label'].value] = component.attributes['id'].value
        return items