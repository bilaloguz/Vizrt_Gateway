#global modules import
import json
from enum import Enum

class CommandStatus(Enum):
    Received = 1
    Sent = 2
    Failed = 3

class Command:

    def __init__(self, JSONString):
       
        JSONDict = json.loads(JSONString, strict=False)
        self.type = JSONDict['Command']
        self.layer = JSONDict['Layer']
        self.scene = JSONDict['Scene']
        self.items = JSONDict['Items']
        self.status = None
        if self.type:
            self.status = CommandStatus.Received
