import unittest
from datetime import datetime
from Utils.IDW import IDW
from Utils import Distance
class TestIDW(unittest.TestCase):
    def testConstructor(self):
        idw = IDW(1)
        self.assertAlmostEqual(idw.p,1,'Error assingning parameter p in costructor')
        self.assertAlmostEqual(len(idw.weights),0,'Error creating list of weights')
    def testSetWeights(self):
        idw=IDW(1)
        x=-12.00
        y=-77.00
        coords=[[-12.3,-77.5],[-12.4,-77.6],[-12.5,-77.7]]
        idw.setWeights(x,y,coords)
        weights=[1.5680747804743054e-05, 1.2668746858361315e-05, 1.0613824488129554e-05] # Values calculated
        self.assertAlmostEqual(idw.weights[0],weights[0],'Error calculating first weight')
        self.assertAlmostEqual(idw.weights[1],weights[1],'Error calculating second weight')
        self.assertAlmostEqual(idw.weights[2],weights[2],'Error calculating third weight')
    def testCalculateIDW(self):
        idw=IDW(1)
        x=-12.00
        y=-77.00
        coords=[[-12.3,-77.5],[-12.4,-77.6],[-12.5,-77.7]]
        metrics=[5,4,3]
        idwResult=4.130043421017253
        idw.setWeights(x,y,coords)
        self.assertAlmostEqual(idw.calculateIDW(metrics),idwResult,'Error calculating IDW')

if __name__=='__main__':
    unittest.main()