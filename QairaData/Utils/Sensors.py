import json
import requests
from datetime import datetime,date,timedelta
import os
import psycopg2
from psycopg2 import DatabaseError as Error
from Utils.Distance import getDistanceFromLatLonInKm
# import should be like from Utils.Distance import getDistanceFromLatLonInKm, if testing class
class Sensors:
    schema=""
    def __init__(self):
        """Loading configuration for the database requests"""
        f = open("/var/www/html/TESIS2021/QairaData/Configuration/config.json","r")
        # Development route
        data = json.load(f)
        f.close()
        self.schema=data['schema']
        self.mydb=psycopg2.connect(host=data['host'],port=data['port'],database=data['database'],user=data['username'],password=data['password'])
        cursor=self.mydb.cursor()
        query=("select * from {}.Qaira_Sensors where \"Activo\"=1".format(self.schema))
        cursor.execute(query)
        self.sensorsList= list(cursor.fetchall())

        
    
    def getClosestN(self,x,y,n=4):
        self.sensorsList=sorted(self.sensorsList,key= lambda i:(getDistanceFromLatLonInKm(x,y,i[3],i[4])),reverse=False)
        return self.sensorsList[:n]