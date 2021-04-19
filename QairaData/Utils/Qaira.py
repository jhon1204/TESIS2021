import json
import requests
from datetime import datetime,date,timedelta
import os
import mysql.connector as SQLConn
from mysql.connector import Error

class Qaira:
    url = ""
    def __init__(self):
        """Loading configuration for the api requests"""
        f = open("C:\\Users\\Jhon\\Documents\\TESIS\\Proyecto\\TESIS2021\\QairaData\\Configuration\\config.json","r") # Development route
        data = json.load(f)
        f.close()
        self.url=data['qairaUrl']
        self.mydb=SQLConn.connect(user=data['username'],password=data['password'],host=data['host'],database=data['database'])

    def getAll(self):
        cursor=self.mydb.cursor(buffered=True)
        try:
            getSensors=('select * from qaira_sensors')
            cursor.execute(getSensors)
            sensors=list(cursor.fetchall())
            for (qHawax_ID,company,activo,lat,lon) in sensors:
                self.getAirQuality(qHawax_ID)
        except Error as error:
            print(error)
        finally:
            cursor.close()
            

    def getAirQuality (self,ID,initial_timestamp=datetime.utcnow()):
        YEAR = str(initial_timestamp.year)
        MONTH = str(initial_timestamp.month).zfill(2)
        DATE = str(initial_timestamp.day).zfill(2)
        HOUR = str(initial_timestamp.hour).zfill(2)
        parameters = "?qhawax_id="+str(ID)+"&company_id=3&initial_timestamp="+DATE+'-'+MONTH+'-'+YEAR+' '+HOUR+':00:00'+"&final_timestamp="+DATE+'-'+MONTH+'-'+YEAR+' '+HOUR+':00:00'
        response = requests.get(self.url+parameters)
        if response.status_code ==200 and len(response.json())==1:
            self.saveToDB(response.json()[len(response.json())-1],ID)
            return response.json()[len(response.json())-1]
        else:
            self.saveToDB({},ID)
            return {
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
                }
    
    def saveToDB(self,response,ID=-1):
        if len(response)!=0:
            cursor = self.mydb.cursor(buffered=True)
            updateSensor= ('Update qaira_sensors set Activo=1 where qHawax_ID=%(id)s')
            data={'id':ID}
            cursor.execute(updateSensor,data)
            cursor.close()
            cursor = self.mydb.cursor(buffered=True)
            getPollutants =("Select * from pollutant")
            cursor.execute(getPollutants)
            for (idPollutant,pollutantName,pollutantMetric) in cursor:
                getMetrics=('select * from metricslima where qHawaxID=%(id)s and timestamp=%(timestam)s and idPollutant=%(pollutant)s')
                insertMeasure=('Insert into metricslima ''(qHawaxID,timestamp,idPollutant,Value)''values (%(id)s,%(timestam)s,%(pollutant)s,%(val)s)')
                timestamp= datetime.strptime(response['timestamp_zone'],'%a, %d %b %Y %H:%M:%S GMT')
                cursor=self.mydb.cursor(buffered=True)
                mdata={'id':ID,'timestam':timestamp,'pollutant':idPollutant}
                cursor.execute(getMetrics,mdata)
                print('id: ',ID,'------rowcount:  ',cursor.rowcount,'  pollutant: ',pollutantName)
                if cursor.rowcount==0:
                    if pollutantName not in ("PM10","PM25"):
                        measure= {'id':ID,'timestam':timestamp,'pollutant':idPollutant,'val':response[pollutantName+'_ug_m3']}
                    else:
                        measure={'id':ID,'timestam':timestamp,'pollutant':idPollutant,'val':response[pollutantName]}
                    # Insert new measure
                    try:
                        cursor = self.mydb.cursor(buffered=True)
                        cursor.execute(insertMeasure,measure)
                        self.mydb.commit()
                    except Error as error:
                        print(error)
                    finally:
                        cursor.close()
                else:
                    editMetric=('update metricslima set Value=%(val)s where qHawaxID=%(id)s and timestamp=%(timestam)s and idPollutant=%(pollutant)s')
                    if pollutantName not in ("PM10","PM25"):
                        measure= {'id':ID,'timestam':timestamp,'pollutant':idPollutant,'val':response[pollutantName+'_ug_m3']}
                    else:
                        measure={'id':ID,'timestam':timestamp,'pollutant':idPollutant,'val':response[pollutantName]}
                    # Insert new measure
                    try:
                        cursor = self.mydb.cursor(buffered=True)
                        cursor.execute(editMetric,measure)
                        self.mydb.commit()
                    except Error as error:
                        print(error)
                    finally:
                        cursor.close()    
            

        else:
            # set sensor as inactive
            deactivateSensor= ('Update qaira_sensors set Activo=0 where qHawax_ID=%(id)s')
            sensorData={'id':ID}
            try:
                cursor = self.mydb.cursor(buffered=True)
                cursor.execute(deactivateSensor,sensorData)
                self.mydb.commit()
            except Error as error:
                print(error)
            finally:
                cursor.close()

if __name__=='__main__':
    qaira=Qaira()
    qaira.getAll()