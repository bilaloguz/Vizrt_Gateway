from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired, Length
import configparser
from watchgod import watch, run_process
import multiprocessing
import os
import psutil

from gateway import Gateway
workerprocess = []
gw = Gateway()
app = Flask(__name__)
app.config['SECRET_KEY'] = '987412365Bil/*'

class WebServer():

    def __init__(self):
        self.isRunning = None

    def run(self): 
        app.run(host='0.0.0.0', port=int(self.getConfig()['WebPort']))
        self.pid = os.getpid()
        if self.pid:
            self.isRunning = True

    def stop(self):
        process = psutil.Process(self.pid)
        process.terminate()
        self.isRunning = False

    def getConfig(self):
        configFile = configparser.ConfigParser()
        configFile.read("Gateway.config")
        config = {}
        config['WebPort'] = str(configFile['Configuration']['WebPort'])
        config['ListenerPort'] = str(configFile['Configuration']['ListenerPort'])
        config['ServerIP'] = str(configFile['Configuration']['ServerIP'])
        config['ServerPort'] = str(configFile['Configuration']['ServerPort'])
        config['VizrtEmptyScenePath'] = str(configFile['Configuration']['EmptyScenePath'])
        config['ServerType'] = str(configFile['Configuration']['ServerType'])
        config['ChannelportScenesDirectoryPath'] = str(configFile['Configuration']['ChannelportScenesDirectoryPath'])
        return config

webServer = WebServer()

class ConfigForm(FlaskForm):
    webPort = StringField('Web Server Port')
    listenerPort = StringField('Listener Port')
    serverType = StringField('Server Type')
    serverIP = StringField('Server IP')
    emptyScenePath = StringField('Vizrt Empty Scene Path')
    channelportScenesDirectoryPath = StringField('Channelport Scenes Directory Path')
    submit = SubmitField('Save')

def getConfig():
    configFile = configparser.ConfigParser()
    configFile.read("Gateway.config")
    config = {}
    config['WebPort'] = str(configFile['Configuration']['WebPort'])
    config['ListenerPort'] = str(configFile['Configuration']['ListenerPort'])
    config['ServerIP'] = str(configFile['Configuration']['ServerIP'])
    config['ServerPort'] = str(configFile['Configuration']['ServerPort'])
    config['VizrtEmptyScenePath'] = str(configFile['Configuration']['EmptyScenePath'])
    config['ServerType'] = str(configFile['Configuration']['ServerType'])
    config['ChannelportScenesDirectoryPath'] = str(configFile['Configuration']['ChannelportScenesDirectoryPath'])
    return config

@app.route('/')
def retrieveConfig():
    config = getConfig()
    form = ConfigForm()
    form.webPort = str(config['WebPort'])
    form.listenerPort = str(config['ListenerPort'])
    form.serverType = str(config['ServerType'])
    form.serverIP = str(config['ServerIP'])
    form.emptyScenePath = str(config['VizrtEmptyScenePath'])
    form.channelportScenesDirectoryPath = str(config['ChannelportScenesDirectoryPath'])
    configForm = ConfigForm(obj=form)
    return render_template('config.html', form=configForm)

@app.route('/save', methods=['POST'])
def saveConfig():
    configFile = configparser.ConfigParser()
    configFile.read("Gateway.config")
    configFile.set('Configuration', 'webport', str(request.form.get('webPort')))
    configFile.set('Configuration', 'listenerport', str(request.form.get('listenerPort')))
    configFile.set('Configuration', 'servertype', str(request.form.get('serverType')))
    configFile.set('Configuration', 'serverip', str(request.form.get('serverIP')))
    configFile.set('Configuration', 'emptyscenepath', str(request.form.get('emptyScenePath')))
    configFile.set('Configuration', 'channelportscenesdirectorypath', str(request.form.get('channelportScenesDirectoryPath')))
    with open('Gateway.Config', 'w') as cfg:
        configFile.write(cfg)
    gw.setConfig(getConfig())
    return redirect(url_for('retrieveConfig'))  

def runGateway():

    print("RUNGATEWAY")
    conf = getConfig()
    print("getConfig OK")
    gw.setConfig(conf)
    gw.run()
        
def runWeb():
    if webServer.isRunning:
        webServer.stop()
    else:
        webServer.run()

if __name__ == '__main__':
    multiprocessing.freeze_support()
    webProcess = multiprocessing.Process(target=runWeb)
    webProcess.start()
    print("Started")
    run_process("path", runGateway)
    