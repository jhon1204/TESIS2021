import unittest
import datetime
from Utils.Grid import MyGrid
from Utils.Qaira import Qaira
import numpy as np

class TestGrid2(unittest.TestCase):
    def testFillGrid(self):
        qaira=Qaira()
        qaira.getAll()
        grid=MyGrid()
        grid.initializeMatrix()
        grid.updateAQMatrix()

if __name__=='__main__':
    unittest.main()