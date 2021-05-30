import numpy as np
from Utils.Distance import getDistanceFromLatLonInKm
# import should be like from Utils.Distance import getDistanceFromLatLonInKm, if testing
"""
IDW implementation adapted from : 'https://www.geodose.com/2019/09/creating-idw-interpolation-from-scratch-python.html'
"""
degrees=0.001*100/111 
class IDW:
    def __init__(self,p=2):
        self.p=p
        self.weights=[]
    
    def setWeights(self,x,y,metricsCoord):
        self.weights=[]
        print("Setting weights: ", metricsCoord)
        for coord in metricsCoord:
            d=getDistanceFromLatLonInKm(x,y,coord[0],coord[1])*1000 # Transform to meters
            if d>0 and abs(x-coord[0])>degrees and abs(x-coord[0])>degrees: # makes sure that is not in the cell
                w=1/(d**self.p)
                self.weights.append(w)
            else:
                self.weights.append(0)
    def calculateIDW(self,metrics):
        idwResult=0
        print("metrics: ", metrics)
        if 0 in self.weights:
            index=self.weights.index(0)
            idwResult=metrics[index]
        else:
            wT= np.transpose(self.weights)
            idwResult=np.dot(metrics,wT)/sum(self.weights)
        
        return idwResult