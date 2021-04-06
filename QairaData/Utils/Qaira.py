import json
import requests
import datetime
import os

class Qaira:
    url = ""
    def __init__(self):
        """Loading configuration for the api requests"""
        f = open("C:\\Users\\Jhon\\Documents\\TESIS\\Proyecto\\TESIS2021\\QairaData\\Configuration\\config.json","r")
        data = json.load(f)
        f.close()
        self.url=data['qairaUrl']

    def getAirQuality (self,ID,initial_timestamp=datetime.datetime.utcnow()):
        parameters = "?qhawax_id="+str(ID)+"&company_id=3&initial_timestamp="+initial_timestamp.strftime("%d-%m-%Y %H:%M:%S")+"&final_timestamp="+initial_timestamp.strftime("%d-%m-%Y %H:%M:%S")
        response = requests.get(self.url+parameters)
        if response.status_code ==200:
            return response.json()[len(response.json())-1]
        else:
            
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