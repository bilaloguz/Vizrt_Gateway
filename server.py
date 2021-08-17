#global modules import
import configparser
import os, signal
from watchgod import watch, run_process
import socket
import multiprocessing

#own-modules import
from gateway import Gateway

def getConfig():
    configFile = configparser.ConfigParser()
    configFile.read("Gateway.config")
    config = {}
    config['WebPort'] = int(configFile['Configuration']['WebPort'])
    config['ListenerPort'] = int(configFile['Configuration']['ListenerPort'])
    config['ServerIP'] = str(configFile['Configuration']['ServerIP'])
    config['ServerPort'] = int(configFile['Configuration']['ServerPort'])
    config['VizrtEmptyScenePath'] = str(configFile['Configuration']['EmptyScenePath'])
    config['ServerType'] = str(configFile['Configuration']['ServerType'])
    config['ChannelportScenesDirectoryPath'] = str(configFile['Configuration']['ChannelportScenesDirectoryPath'])
    return config

def runGateway():
    config = getConfig()
    gw = Gateway()
    gw.setConfig(config)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    run_process("Gateway.config", runGateway)
    
