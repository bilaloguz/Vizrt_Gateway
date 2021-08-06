class VizrtCommands:

    def __init__(self, emptyScenePath):
        self.emptyScenePath = emptyScenePath

    def getVersionCommand(self):
        return "0 MAIN VERSION\0".encode('utf-8')
    
    def setExternalOnCommand(self):
        return "0 MAIN SWITCH_EXTERNAL ON\0".encode('utf-8')

    def showLayerSceneCommand(self, layer, scene):
        command1 = "0 RENDERER*" + layer + " SET_OBJECT SCENE*" + scene + "\0"
        command2 = "0 RENDERER SET_OBJECT SCENE*" + scene + "\0"
        if len(layer) != 0:
            return command1.encode('utf-8')
        else:
            return command2.encode('utf-8')

    def hideLayerSceneCommand(self, layer):
        command1 = "0 RENDERER*" + layer + " SET_OBJECT SCENE*" + self.emptyScenePath + "\0"
        command2 = "0 RENDERER SET_OBJECT SCENE*" + self.emptyScenePath + "\0"
        if len(layer) != 0:
            return command1.encode("utf-8")
        else:
            return command2.encode('utf-8')

    def setLayerItemText(self, layer, scene, itemNodeFullPath, text):
        node = ""
        if "$" in itemNodeFullPath:
            node = itemNodeFullPath
        else:
            node = "object$" + itemNodeFullPath
        msg = "0 RENDERER*TREE*$" + node + "*GEOM*TEXT SET " + text +"\0"
        return msg.encode('utf-8')

    def hideLayerItem(self, layer, itemNodeFullPath):
        command1 = "0 RENDERER*" + layer + "*TREE*" + itemNodeFullPath + "*ACTIVE SET Off\0"
        command2 = "0 RENDERER*TREE*" + itemNodeFullPath + "*ACTIVE SET Off\0"
        if len(layer) != 0:
            return command1.encode('utf-8')
        else:
            return command2.encode('utf-8')
