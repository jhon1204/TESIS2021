import unittest
import datetime
from Utils.Grid import MyGrid
import numpy as np

class TestGrid(unittest.TestCase):
    def testConstructor(self):
        grid=MyGrid()
        self.assertEqual(grid.setted,False,'Error in constructor')
        self.assertEqual(grid.size[0],2.835470629436158,'Error in constructor')
        self.assertEqual(grid.size[1],5.872549022186773,'Error in constructor')
        shape = np.array(grid.matrix).shape
        self.assertAlmostEqual(shape[0],59,'Error creating matrix')
        self.assertAlmostEqual(shape[1],29,'Error creating matrix')
    def testInitializeMatrix(self):
        grid=MyGrid()
        grid.initializeMatrix()
        cell0_0=[-12.035450450450451, -77.05614954954956]
        cell1_2=[-12.036351351351351, -77.05434774774776]
        cell0_9=[-12.035450450450451, -77.04804144144146]
        self.assertEqual(grid.matrix[0][0]['midpoint'],cell0_0,'Error in  initializing cells ')
        self.assertEqual(grid.matrix[1][2]['midpoint'],cell1_2,'Error in  initializing cells ')
        self.assertEqual(grid.matrix[0][9]['midpoint'],cell0_9,'Error in  initializing cells ')
    def testUpdatedAQMatrix(self):
        # Values are time dependant
        grid=MyGrid()
        grid.initializeMatrix()
        grid.updateAQMatrix()
        cell0_0={'CO': 2008.8620880424091, 'H2S': 20.229989798588093, 'NO2': 78.92910401178264, 'O3': 65.07853301248132, 'PM10': 68.5375929390606, 'PM25': 21.083110889673325, 'SO2': 14.587962958667989}
        cell1_2={'CO': 2010.400510122323, 'H2S': 20.210651131195515, 'NO2': 78.92180599639161, 'O3': 65.07936740621825, 'PM10': 67.74699914727245, 'PM25': 21.009710784361847, 'SO2': 14.477238363309402}
        cell0_9={'CO': 2538.796731158202, 'H2S': 21.693143639336043, 'NO2': 77.99873055404586, 'O3': 64.70843075625719, 'PM10': 70.72366196536949, 'PM25': 21.427175371889103, 'SO2': 11.439026368121965}
        for key in cell0_0.keys():
            self.assertAlmostEqual(grid.matrix[0][0]['pollutants'][key],cell0_0[key],'Error in updating matrix')
        for key in cell1_2.keys():
            self.assertAlmostEqual(grid.matrix[1][2]['pollutants'][key],cell1_2[key],'Error in updating matrix')
        for key in cell0_9.keys():
            self.assertAlmostEqual(grid.matrix[0][9]['pollutants'][key],cell0_9[key],'Error in updating matrix')

    def testGetIDW(self):
        grid=MyGrid()
        midpoint=[-12,-77]
        metricsCO=[10,11,12]
        metricsCoord= [[-12.5,-77.3],[-12.4,-77.2],[-12.3,-77]]
        expected={'CO': 11.42515698536339, 'H2S': 11.42515698536339, 'NO2': 11.42515698536339, 'O3': 11.42515698536339, 'PM10': 11.42515698536339, 'PM25': 11.42515698536339, 'SO2': 11.42515698536339}
        response=grid.getIDW(metricsCO,metricsCO,metricsCO,metricsCO,metricsCO,metricsCO,metricsCO,metricsCoord,midpoint)
        for key in expected.keys():
            self.assertAlmostEqual(expected[key],response[key],'Error in getting IDW')
        

if __name__=='__main__':
    unittest.main()
