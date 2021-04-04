from Distance import altoLargo
from Qaira import Qaira

degrees=0.001*200/111      #how many degrees are 200m
class MyGrid:
    def __init__(self):
        size=altoLargo()
        self.matrix=[[{} for i in range(size[0])] for j in range(size[1])]
        self.QairaApi= Qaira()
    


