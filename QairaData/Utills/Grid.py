from Distance import altoLargo,getCoordinates
from Qaira import Qaira
from Sensors import Sensors
import math
degrees=0.001*200/111      #how many degrees are 200m
class MyGrid:
    def __init__(self):
        self.setted=False
        self.size=altoLargo()
        self.coordinates= getCoordinates()
        self.matrix=[[{} for i in range(math.ceil(self.size[0]/0.2))] for j in range(math.ceil(self.size[1]/0.2))] # Is divided between 0.2 to know how many cells are going to be needed
        self.QairaApi= Qaira()
        self.sensors= Sensors()
    
    def initializeMatrix(self):
        sizeX= len(self.matrix)
        sizeY= len(self.matrix[0])
        for i in range(sizeX):
            for j in range(sizeY):
                midpoint=[0,0]
                if i != sizeX-1:
                    midpoint[0]= self.coordinates[2]-(i*degrees)-(degrees/2) 
                else:
                    midpoint[0]= self.coordinates[0]+((abs(self.coordinates[0]-self.coordinates[2])-(i*degrees))/2)
                
                if j != sizeY-1:
                    midpoint[1]= self.coordinates[1]+(j*degrees)+(degrees/2)
                else:
                    midpoint[1]= self.coordinates[3]-((abs(self.coordinates[3]-self.coordinates[1])-(j*degrees))/2)
                
                self.matrix[i][j]['midpoint']=midpoint
    
    def updateAQMatrix(self):
        if self.setted:
            ...   # Save matrix to DB
        sizeX= len(self.matrix)
        sizeY= len(self.matrix[0])
        for i in range(sizeX):
            for j in range(sizeY):
                self.matrix[i][j]['pollutants']=self.getInterpolated(self.matrix[i][j]['midpoint'])
        
        self.setted=True
    
    def getInterpolated(self,midpoint):
        """
                "CO_ug_m3":-1,
                "H2S_ug_m3":-1,
                "NO2_ug_m3":-1,
                "O3_ug_m3":-1,
                "PM10":-1,
                "PM25":-1,
                "SO2_ug_m3":-1,
                "SPL":-1,
                "UV":-1,
                "humidity":-1,
                "lat":0.00,
                "lon":0.00,
                "pressure":-1,
                "temperature":-1,
                "timestamp_zone":"Sun, 1 Jan 2021 00:00:00 GMT"
        """
        ids = self.sensors.getClosestN(midpoint[0],midpoint[1],3)
        metricsCO=[]
        metricsH2S=[]
        metricsNO2=[]
        metricsO3=[]
        metricsPM10=[]
        metricsPM25=[]
        metricsSO2=[]
        metricsCoord=[]
        for sensorID in ids:
            response=self.QairaApi.getAirQuality(sensorID)
            if response["CO_ug_m3"] != -1:
                metricsCO.append(response["CO_ug_m3"])
                metricsH2S.append(response["H2S_ug_m3"])
                metricsNO2.append(response["NO2_ug_m3"])
                metricsO3.append(response["O3_ug_m3"])
                metricsPM10.append(response["PM10"])
                metricsPM25.append(response["PM25"])
                metricsSO2.append(response["SO2_ug_m3"])
                metricsCoord.append([response["lat"],response["lon"]])
        
             
        return self.getIDW(metricsCO,metricsH2S,metricsNO2,metricsO3,metricsPM10,metricsPM25,metricsSO2,metricsCoord)
    
    def getIDW(self,metricsCO,metricsH2S,metricsNO2,metricsO3,metricsPM10,metricsPM25,metricsSO2,metricsCoord):
        return []
