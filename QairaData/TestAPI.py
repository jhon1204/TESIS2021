import unittest
from datetime import datetime
import json
import requests
class TestAPI(unittest.TestCase):
    def test_qaira(self):
        message="Success"
        response= requests.get('http://127.0.0.1:5000/qaira')
        self.assertEqual(message,response.json()['result'])
        
    def test_idw(self):
        message="Success"
        response=requests.get('http://127.0.0.1:5000/idw')
        self.assertEqual(message,response.json()['result'])

    def test_sensors(self):
        sensor={"id": 41,"lat": -12.0466446528819,"lon": -77.0802620815967,"pollutantValue": 0.0}
        response=requests.get('http://127.0.0.1:5000/sensors')
        first=response.json()['sensors'][0]
        self.assertAlmostEqual(sensor['id'],first['id'])
        self.assertAlmostEqual(sensor['lat'],first['lat'])
        self.assertAlmostEqual(sensor['lon'],first['lon'])
        self.assertAlmostEqual(sensor['pollutantValue'],first['pollutantValue'])
    
    def test_densityMap(self):
        cell={"geometry": {"coordinates": [[[-12.035900900900902,-77.0566],[-12.035,-77.0566],[-12.035,-77.05569909909912],[-12.035900900900902,-77.05569909909912],[-12.035900900900902,-77.0566]]],"type": "Polygon"},"id": "00_00","properties": {"name": "00_00","pollution": 0.0},"type": "Feature"}
        coordinates= cell['geometry']['coordinates'][0]
        response=requests.get('http://127.0.0.1:5000/densityMap')
        first=response.json()['features'][0]
        firstCoord=first['geometry']['coordinates'][0]
        self.assertAlmostEqual(cell['id'],first['id'])
        self.assertAlmostEqual(coordinates[0][0],firstCoord[0][0])
        self.assertAlmostEqual(coordinates[1][0],firstCoord[1][0])
        self.assertAlmostEqual(coordinates[2][0],firstCoord[2][0])
        self.assertAlmostEqual(coordinates[3][0],firstCoord[3][0])
        self.assertAlmostEqual(coordinates[4][0],firstCoord[4][0])
        self.assertAlmostEqual(coordinates[0][1],firstCoord[0][1])
        self.assertAlmostEqual(coordinates[1][1],firstCoord[1][1])
        self.assertAlmostEqual(coordinates[2][1],firstCoord[2][1])
        self.assertAlmostEqual(coordinates[3][1],firstCoord[3][1])
        self.assertAlmostEqual(coordinates[4][1],firstCoord[4][1])
        


if __name__=="__main__":
    unittest.main()