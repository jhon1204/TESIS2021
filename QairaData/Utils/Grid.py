from Utils.Distance import altoLargo,getCoordinates
# Import should be like from Utils.Distance import altoLargo,getCoordinates, if testing
from Utils.Qaira import Qaira
# Import should be like from Utils.Qaira import Qaira, if testing
from Utils.Sensors import Sensors
# Import should be like from Utils.Sensors import Sensors, if testing
import math
from Utils.IDW import IDW
# Import should be like from Utils.IDW import IDW, if testing
import json
import psycopg2
from psycopg2 import DatabaseError as Error
import os
import datetime
degrees=0.001*100/111      #how many degrees are 100m
class MyGrid:
    schema=""
    def __init__(self):
        """Loading configuration for the database requests"""
        f = open("C:\\Users\\Jhon\\Documents\\TESIS\\Proyecto\\TESIS2021\\QairaData\\Configuration\\config.json","r")
        # Development route
        data = json.load(f)
        f.close()
        self.mydb=psycopg2.connect(host=data['host'],port=data['port'],database=data['database'],user=data['username'],password=data['password'])
        self.schema=data['schema']
        self.setted=False
        self.size=altoLargo()
        self.coordinates= getCoordinates()
        self.matrix=[[{} for i in range(math.ceil(self.size[0]/0.1))] for j in range(math.ceil(self.size[1]/0.1))] # Is divided between 0.1 to know how many cells are going to be needed
        self.QairaApi= Qaira()
        self.sensors= Sensors()

    
    def initializeMatrix(self):
        sizeX= len(self.matrix)
        sizeY= len(self.matrix[0])
        for i in range(sizeX):
            for j in range(sizeY):
                midpoint=[0,0]
                midpoint[0] = self.coordinates[2]-(i*degrees)-(degrees/2)
                midpoint[1] = self.coordinates[1]+(j*degrees)+(degrees/2)
                # if i != sizeX-1:
                #     midpoint[0]= self.coordinates[2]-(i*degrees)-(degrees/2) 
                # else:
                #     midpoint[0]= self.coordinates[0]+((abs(self.coordinates[0]-self.coordinates[2])-(i*degrees))/2)
                
                # if j != sizeY-1:
                #     midpoint[1]= self.coordinates[1]+(j*degrees)+(degrees/2)
                # else:
                #     midpoint[1]= self.coordinates[3]-((abs(self.coordinates[3]-self.coordinates[1])-(j*degrees))/2)
                
                self.matrix[i][j]['midpoint']=midpoint
                try:
                    cursor1= self.mydb.cursor()
                    getCells=('select * from {}.cellsData'.format(self.schema))
                    cursor1.execute(getCells)
                    cells= list(cursor1.fetchall())
                    if len(cells)==0:
                        insertGrid=("insert into {}.cellsData(\"idcell\",\"midLat\",\"midLon\") values (%(id)s,%(lat)s,%(lon)s)".format(self.schema))
                        values= { 'id': str(i).zfill(2) +'_'+str(j).zfill(2), 'lat': self.matrix[i][j]['midpoint'][0], 'lon': self.matrix[i][j]['midpoint'][1]}
                        try:
                            cursor = self.mydb.cursor()
                            cursor.execute(insertGrid,values)
                            self.mydb.commit()
                        except Error as error:
                            print(error)
                        finally:
                            cursor.close()
                except Error as error:
                    print(error)
                finally:
                    cursor1.close()
        self.setted = True
    
    def updateAQMatrix(self):
        """
        1	CO	ug/m3
        2	H2S	ug/m3
        3	NO2	ug/m3
        4	O3	ug/m3
        5	PM10	ug/m3
        6	PM25	ug/m3
        7	SO2	ug/m3
        """
        # Save interpolation to DB            
        sizeX= len(self.matrix)
        sizeY= len(self.matrix[0])
        YEAR = str(datetime.date.today().year)
        MONTH = str(datetime.date.today().month).zfill(2)
        DATE = str(datetime.date.today().day).zfill(2)
        HOUR = str(datetime.datetime.now().hour).zfill(2)
        timestamp = datetime.datetime.strptime( YEAR+'-'+MONTH+'-'+DATE+' '+HOUR+':00:00', '%Y-%m-%d %H:%M:%S')
        first =False
        for i in range(sizeX):
            for j in range(sizeY):
                self.matrix[i][j]['pollutants']=self.getInterpolated(self.matrix[i][j]['midpoint'])
                try:
                    count=0
                    try:
                        cursorQ=self.mydb.cursor()
                        query= ("select * from {}.interpolatedmetrics limit 1".format(self.schema))
                        cursorQ.execute(query)
                        count=cursorQ.rowcount
                        if i==0 and j==0 and count==0 :
                            first=True
                    except Error as error:
                        print(error)
                    finally:
                        cursorQ.close()
                    if first:
                        insertIP=("insert into {}.interpolatedmetrics(\"idinterpolation_algorithm\",\"idcell\",\"idPollutant\",\"interpolatedValiue\",\"timestamp\") values (%(algorithm)s,%(id)s,%(poll)s,%(val)s,%(time)s)".format(self.schema))
                        cursor = self.mydb.cursor()
                        getPoll= ("select * from {}.pollutant".format(self.schema))
                        cursor.execute(getPoll)
                        pollutants  = list(cursor.fetchall())
                        print('poll  ',pollutants,'----------')
                        cursor.close()
                        for (idpoll,polName,metric) in pollutants:
                            print('metrics: ',polName,'--------',self.matrix[i][j]['pollutants'][polName])
                            values={'algorithm':'IDW', 'id': str(i).zfill(2) +'_'+str(j).zfill(2), 'poll':int(idpoll),'val':float(self.matrix[i][j]['pollutants'][polName]),'time':timestamp }
                            cursor=self.mydb.cursor()
                            cursor.execute(insertIP,values)
                            self.mydb.commit()
                    else:
                        updateIP=("update {}.interpolatedmetrics set \"interpolatedValiue\"=%(val)s, \"timestamp\"=%(time)s where \"idinterpolation_algorithm\"=%(algorithm)s and \"idcell\"=%(id)s and \"idPollutant\"=%(poll)s ".format(self.schema))
                        cursor = self.mydb.cursor()
                        getPoll= ("select * from {}.pollutant".format(self.schema))
                        cursor.execute(getPoll)
                        pollutants  = list(cursor.fetchall())
                        print('poll  ',pollutants,'----------u')
                        cursor.close()
                        for (idpoll,polName,metric) in pollutants:
                            print('metrics: ',polName,'--------',self.matrix[i][j]['pollutants'][polName])
                            values={'algorithm':'IDW', 'id': str(i).zfill(2) +'_'+str(j).zfill(2), 'poll':int(idpoll),'val':float(self.matrix[i][j]['pollutants'][polName]),'time':timestamp }
                            cursor=self.mydb.cursor()
                            cursor.execute(updateIP,values)
                            self.mydb.commit()
                except Error as error:
                    print(error)
                finally:
                    cursor.close()


    
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
        print('into interpolated')
        ids = self.sensors.getClosestN(midpoint[0],midpoint[1],3)
        metricsCO=[]
        metricsH2S=[]
        metricsNO2=[]
        metricsO3=[]
        metricsPM10=[]
        metricsPM25=[]
        metricsSO2=[]
        metricsCoord=[]
        initial_timestamp=datetime.datetime.now()
        for sensorID in ids:
            YEAR = str(initial_timestamp.year)
            MONTH = str(initial_timestamp.month).zfill(2)
            DATE = str(initial_timestamp.day).zfill(2)
            HOUR = str(initial_timestamp.hour).zfill(2)
            timestamp = datetime.datetime.strptime( YEAR+'-'+MONTH+'-'+DATE+' '+HOUR+':00:00', "%Y-%m-%d %H:%M:%S")
            getMetrics= ("select a.\"qHawaxID\",a.\"timestamp\",a.\"idPollutant\",a.\"Value\",b.\"pollutantName\",c.\"lat\",c.\"lon\" from {}.metricslima a,{}.pollutant b, {}.qaira_sensors c where a.\"idPollutant\"=b.\"idPollutant\" and a.\"qHawaxID\"=c.\"qHawax_ID\"  and a.\"qHawaxID\"=%(id)s and a.\"timestamp\"=%(time)s".format(self.schema,self.schema,self.schema))
            values={'id':int(sensorID[0]),'time': timestamp}
            cursor=self.mydb.cursor()
            try:
                cursor.execute(getMetrics,values)
                metrics=list(cursor.fetchall())
                count=0
                # while len(metrics)==0 and count <10:
                #     print('no metrics')
                #     count+=1
                #     initial_timestamp=initial_timestamp-datetime.timedelta(hours=1)
                #     YEAR = str(initial_timestamp.year)
                #     MONTH = str(initial_timestamp.month).zfill(2)
                #     DATE = str(initial_timestamp.day).zfill(2)
                #     HOUR = str(initial_timestamp.hour).zfill(2)
                #     timestamp = datetime.datetime.strptime( YEAR+'-'+MONTH+'-'+DATE+' '+HOUR+':00:00', '%Y-%m-%d %H:%M:%S')
                #     values={'id':sensorID[0],'time': timestamp}
                #     cursor.execute(getMetrics,values)
                #     metrics=list(cursor.fetchall())
                lat1=0
                lon1=0
                for (qhawax_id,timestamp,idpoll,metric,pollutantName,lat,lon) in metrics:
                    if pollutantName=='CO':
                        metricsCO.append(metric)
                    if pollutantName=='H2S':
                        metricsH2S.append(metric)
                    if pollutantName=='NO2':
                        metricsNO2.append(metric)
                    if pollutantName=='O3':
                        metricsO3.append(metric)
                    if pollutantName=='PM10':
                        metricsPM10.append(metric)
                    if pollutantName=='PM25':
                        metricsPM25.append(metric)
                    if pollutantName=='SO2':
                        metricsSO2.append(metric)
                    lat1=lat
                    lon1=lon
                metricsCoord.append([lat1,lon1])
            except Error as error:
                print(error)
            finally:
                cursor.close()
             
        return self.getIDW(metricsCO,metricsH2S,metricsNO2,metricsO3,metricsPM10,metricsPM25,metricsSO2,metricsCoord,midpoint)
    
    def getIDW(self,metricsCO,metricsH2S,metricsNO2,metricsO3,metricsPM10,metricsPM25,metricsSO2,metricsCoord,midpoint):
        """Loading configuration for the api requests"""
        f = open("C:\\Users\\Jhon\\Documents\\TESIS\\Proyecto\\TESIS2021\\QairaData\\Configuration\\config.json","r") # Development route
        data = json.load(f)
        f.close()
        self.idw=IDW(data['p'])
        print("MetricsCoord: ", len(metricsCoord)," ------------- - - - - - -- sadsd")
        self.idw.setWeights(midpoint[0],midpoint[1],metricsCoord)
        idwResponse={}
        idwResponse['CO'] = self.idw.calculateIDW(metricsCO)
        idwResponse['H2S'] = self.idw.calculateIDW(metricsH2S)
        idwResponse['NO2'] = self.idw.calculateIDW(metricsNO2)
        idwResponse['O3'] = self.idw.calculateIDW(metricsO3)
        idwResponse['PM10'] = self.idw.calculateIDW(metricsPM10)
        idwResponse['PM25'] = self.idw.calculateIDW(metricsPM25)
        idwResponse['SO2'] = self.idw.calculateIDW(metricsSO2)
        return idwResponse

if __name__=="__main__":
    grid = MyGrid()
    grid.initializeMatrix()
    grid.updateAQMatrix()
