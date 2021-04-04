import json
import requests
import datetime
class Qaira:
    url = ""
    def __init__(self):
        """Loading configuration for the api requests"""
        f = open("../Configuration/config.json",)
        data = json.load(f)
        self.url=data.qairaUrl

    def getAirQuality (self,ID):
        parameters = {
            "qhawax_id":ID,
            "company_id":3,
            "initial_timestamp": datetime.datetime.utcnow(),
            "final_timestamp":datetime.datetime(2200,1,1)
        }
        response = requests.get(self.url,params=parameters)
        if response.status_code =="200":
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