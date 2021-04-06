import unittest
from datetime import datetime
from Utils.Qaira import Qaira
class TestQaira(unittest.TestCase):
    def test_getAirQuality1(self):
        qaira=Qaira()
        
        ids=37
        response1={
            "CO_ug_m3": 1678.661,
            "H2S_ug_m3": 31.948,
            "NO2_ug_m3": 76.407,
            "O3_ug_m3": 84.643,
            "PM10": 39.49,
            "PM25": 14.152,
            "SO2_ug_m3": 6.563,
            "SPL": 67.83,
            "UV": 0,
            "humidity": 78.982,
            "lat": -12.072736,
            "lon": -77.0826870000001,
            "pressure": 990.07,
            "temperature": 22.525,
            "timestamp_zone": "Sun, 28 Feb 2021 01:00:00 GMT"}
        
        timestamp=datetime.strptime('2021-02-28 01:00:00', '%Y-%m-%d %H:%M:%S')
        resp1=qaira.getAirQuality(ids,timestamp)
        
        

        self.assertAlmostEqual(resp1['CO_ug_m3'],response1['CO_ug_m3'])
        self.assertAlmostEqual(resp1['H2S_ug_m3'],response1['H2S_ug_m3'])
        self.assertAlmostEqual(resp1['NO2_ug_m3'],response1["NO2_ug_m3"])
        self.assertAlmostEqual(resp1['O3_ug_m3'],response1["O3_ug_m3"])
        self.assertAlmostEqual(resp1['PM10'],response1["PM10"])
        self.assertAlmostEqual(resp1['PM25'],response1["PM25"])
        self.assertAlmostEqual(resp1['SO2_ug_m3'],response1["SO2_ug_m3"])
        self.assertAlmostEqual(resp1['SPL'],response1["SPL"])
        self.assertAlmostEqual(resp1['UV'],response1["UV"])
        self.assertAlmostEqual(resp1['humidity'],response1["humidity"])
        self.assertAlmostEqual(resp1['lat'],response1["lat"])
        self.assertAlmostEqual(resp1['lon'],response1["lon"])
        self.assertAlmostEqual(resp1['pressure'],response1["pressure"])
        self.assertAlmostEqual(resp1['temperature'],response1["temperature"])
        self.assertAlmostEqual(resp1['timestamp_zone'],response1["timestamp_zone"])
        


    def test_getAirQuality2(self):
        qaira=Qaira()
        ids=39
        response2={"CO_ug_m3": 813.645,"H2S_ug_m3": 43.996,"NO2_ug_m3": 76.497,"O3_ug_m3": 67.029,"PM10": 39.813,"PM25": 12.903,"SO2_ug_m3": 24.881,"SPL": 71.084,"UV": 0,"humidity": 79.411,"lat": -12.072736,"lon": -77.0826870000001,"pressure": 994.1,"temperature": 22.364,"timestamp_zone": "Sun, 28 Feb 2021 01:00:00 GMT"}
        timestamp=datetime.strptime('2021-02-28 01:00:00', '%Y-%m-%d %H:%M:%S')
        resp2=qaira.getAirQuality(ids,timestamp)

        self.assertAlmostEqual(resp2['CO_ug_m3'],response2["CO_ug_m3"])
        self.assertAlmostEqual(resp2['H2S_ug_m3'],response2["H2S_ug_m3"])
        self.assertAlmostEqual(resp2['NO2_ug_m3'],response2["NO2_ug_m3"])
        self.assertAlmostEqual(resp2['O3_ug_m3'],response2["O3_ug_m3"])
        self.assertAlmostEqual(resp2['PM10'],response2["PM10"])
        self.assertAlmostEqual(resp2['PM25'],response2["PM25"])
        self.assertAlmostEqual(resp2['SO2_ug_m3'],response2["SO2_ug_m3"])
        self.assertAlmostEqual(resp2['SPL'],response2["SPL"])
        self.assertAlmostEqual(resp2['UV'],response2["UV"])
        self.assertAlmostEqual(resp2['humidity'],response2["humidity"])
        self.assertAlmostEqual(resp2['lat'],response2["lat"])
        self.assertAlmostEqual(resp2['lon'],response2["lon"])
        self.assertAlmostEqual(resp2['pressure'],response2["pressure"])
        self.assertAlmostEqual(resp2['temperature'],response2["temperature"])
        self.assertAlmostEqual(resp2['timestamp_zone'],response2["timestamp_zone"])

    def test_getAirQuality3(self):
        qaira=Qaira()
        ids=40
        timestamp=datetime.strptime('2021-02-28 01:00:00', '%Y-%m-%d %H:%M:%S')
        response3={"CO_ug_m3": 1109.398,"H2S_ug_m3": 40.583,"NO2_ug_m3": 68.641,"O3_ug_m3": 85.225,"PM10": 31.96,"PM25": 14.34,"SO2_ug_m3": 28.728,"SPL": 86.683,"UV": 0,"humidity": 81.706,"lat": -12.072736,"lon": -77.0826870000001,"pressure": 995.234,"temperature": 22.044,"timestamp_zone": "Sun, 28 Feb 2021 01:00:00 GMT"}
        resp3=qaira.getAirQuality(ids,timestamp)
        self.assertAlmostEqual(resp3['CO_ug_m3'],response3["CO_ug_m3"])
        self.assertAlmostEqual(resp3['H2S_ug_m3'],response3["H2S_ug_m3"])
        self.assertAlmostEqual(resp3['NO2_ug_m3'],response3["NO2_ug_m3"])
        self.assertAlmostEqual(resp3['O3_ug_m3'],response3["O3_ug_m3"])
        self.assertAlmostEqual(resp3['PM10'],response3["PM10"])
        self.assertAlmostEqual(resp3['PM25'],response3["PM25"])
        self.assertAlmostEqual(resp3['SO2_ug_m3'],response3["SO2_ug_m3"])
        self.assertAlmostEqual(resp3['SPL'],response3["SPL"])
        self.assertAlmostEqual(resp3['UV'],response3["UV"])
        self.assertAlmostEqual(resp3['humidity'],response3["humidity"])
        self.assertAlmostEqual(resp3['lat'],response3["lat"])
        self.assertAlmostEqual(resp3['lon'],response3["lon"])
        self.assertAlmostEqual(resp3['pressure'],response3["pressure"])
        self.assertAlmostEqual(resp3['temperature'],response3["temperature"])
        self.assertAlmostEqual(resp3['timestamp_zone'],response3["timestamp_zone"])