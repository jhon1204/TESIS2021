from Utils.Qaira import Qaira
from Utils.Grid import MyGrid
if __name__=="__main__":
    try:
        print('starting...')
        qaira=Qaira()
        qaira.getAll()
        grid = MyGrid()
        grid.initializeMatrix()
        grid.updateAQMatrix()
    except:
        print("Error al generar las medidas interpoladas con IDW")