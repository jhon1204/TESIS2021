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
        cell0_0={'CO': 1182.6161416198095, 'H2S': 14.67262796298921, 'NO2': 73.92981327290985, 'O3': 64.3148956116276, 'PM10': 77.07262249431716, 'PM25': 21.64832321574118, 'SO2': 16.35321889599812}
        cell1_2={'CO': 1187.505020112994, 'H2S': 14.587687458418387, 'NO2': 73.74343575088561, 'O3': 64.2434805257983, 'PM10': 75.93127750211394, 'PM25': 21.356088687953775, 'SO2': 16.241950339270552}
        cell0_9={'CO': 1324.8761620875737, 'H2S': 16.663813539099436, 'NO2': 75.45807078816495, 'O3': 67.84867286621923, 'PM10': 79.91151859594693, 'PM25': 22.319215750718197, 'SO2': 13.569559891055327}
        
        for key in cell0_0.keys():
            self.assertEqual(grid.matrix[0][0]['pollutants'][key],cell0_0[key],'Error in updating matrix')
        for key in cell1_2.keys():
            self.assertEqual(grid.matrix[1][2]['pollutants'][key],cell1_2[key],'Error in updating matrix')
        for key in cell0_9.keys():
            self.assertEqual(grid.matrix[0][9]['pollutants'][key],cell0_9[key],'Error in updating matrix')

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
