import json
import requests
from datetime import datetime,date,timedelta
import os
import mysql.connector as SQLConn
from mysql.connector import Error
from Distance import getDistanceFromLatLonInKm
class Sensors:
    def __init__(self):
        """Loading configuration for the database requests"""
        f = open("C:\\Users\\Jhon\\Documents\\TESIS\\Proyecto\\TESIS2021\\QairaData\\Configuration\\config.json","r")
        # Development route
        data = json.load(f)
        f.close()
        self.mydb=SQLConn.connect(user=data['username'],password=data['password'],host=data['host'],database=data['database'])
        cursor= self.mydb.cursor(buffered=True)
        query=("select * from Qaira_Sensors where Activo=1")
        cursor.execute(query)
        self.sensorsList= list(cursor.fetchall())

        
    
    def getClosestN(self,x,y,n=4):
        self.sensorsList=sorted(self.sensorsList,key= lambda i:(getDistanceFromLatLonInKm(x,y,i[3],i[4])),reverse=False)
        return self.sensorsList[:n]