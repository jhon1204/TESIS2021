import unittest
from Utils.Sensors import Sensors
class TestSensors(unittest.TestCase):
    def testConstructor(self):
        sensors= Sensors()
        sensList=[(39, 3, 1, -12.041124623734971, -77.04345586507056), (40, 3, 1, -12.04419055791394, -77.05088348594276), (41, 3, 1, -12.046644652881913, -77.08026208159671), (42, 3, 1, -12.039951513735225, -77.01584089685007), (43, 3, 1, -12.045005797916042, -77.02781454597633), (45, 3, 1, -12.04748286005016, -77.0353502908302), (47, 3, 1, -12.054859153087671, -77.02981627116439), (48, 3, 1, -12.044250680280344, -77.01244024902448), (49, 3, 1, -12.051540246704734, -77.07794193651347), (50, 3, 1, -12.042452500222415, -77.03347248594088), (51, 3, 1, -12.046722314468239, -77.04760633498275), (52, 3, 1, -12.045357679869403, -77.03684834722615), (54, 3, 1, -12.057576952834065, -77.0717816233441), (55, 3, 1, -12.060045095590336, -77.03772574086719)]
        for i in range(len(sensList)):
            for j in range(len(sensList[0])):
                self.assertEqual(sensors.sensorsList[i][j],sensList[i][j],'Error in constructor while reading sensors')
    def testGetClosestN(self):
        sensors = Sensors()
        closest=[(48, 3, 1, -12.044250680280344, -77.01244024902448), (42, 3, 1, -12.039951513735225, -77.01584089685007), (43, 3, 1, -12.045005797916042, -77.02781454597633), (47, 3, 1, -12.054859153087671, -77.02981627116439)]
        response=sensors.getClosestN(0,0)
        for i in range(len(closest)):
            for j in range(len(closest[0])):
                self.assertEqual(response[i][j],closest[i][j],'Error in getClosestN sensors')


if __name__=='__main__':
    unittest.main()