import json
from Distance import getDistanceFromLatLonInKm
class Sensors:
    def __init__(self):
        """Loading sensors list"""
        f = open("../Configuration/SensorsL.json",)
        data = json.load(f)
        self.sensorsList=data.Sensors
        
    
    def getClosestN(self,x,y,n):
        self.sensorsList=sorted(self.sensorsList,key= lambda i:(getDistanceFromLatLonInKm(x,y,i['x'],i['y'])),reverse=False)
        return self.sensorsList[:n]

