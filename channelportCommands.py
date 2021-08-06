class ChannelportCommands:

    def __init__(self, scenesPath):
        self.scenesPath = scenesPath
    
    def getVersionCommand(self):
        return "Xb:".encode('utf-8')
    
    def showLayerSceneCommand(self, layer, scene):
        command = "R0" + layer + scene + ":"
        return command.encode('utf-8')

    def hideLayerSceneCommand(self, layer):
        command = "A" + layer + ":"
        return command.encode('utf-8')

    def setLayerItemText(self, layer, itemFieldNumber, text):
        itemFieldNo = int(itemFieldNumber)
        if itemFieldNo < 10:
            itemField = "0" + str(itemFieldNo)
        else:
            itemField = str(itemFieldNo)
        command = "Z0" + layer + itemField + "1" + text + ":"
        return command.encode('utf-8')
