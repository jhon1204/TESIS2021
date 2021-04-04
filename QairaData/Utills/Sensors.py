import json
class Sensors:
    def __init__(self):
        """Loading sensors list"""
        f = open("../Configuration/SensorsL.json",)
        data = json.load(f)
        self.sensorsList=data.Sensors
        self.sensorsList=sorted(self.sensorsList,key= lambda i:(i['x'],i['y']))
    
    def getClosestN(self,x,y,n):
        ...