import flask
from flask import request, jsonify
from Utils.Qaira import Qaira
from Utils.Grid import MyGrid
from apscheduler.scheduler import Scheduler
import atexit


app = flask.Flask(__name__)
app.config["DEBUG"] = True
cron = Scheduler(daemon=True)
cron.start()

@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for QAira Data.</p>"

@app.route('/qaira', methods=['GET'])
def getQaira():
    message={}
    message['result']="Success"
    try:
        qaira=Qaira()
        qaira.getAll()
    except:
        message['result']="Error al actualizar las mediciones"
    return jsonify(message)
@app.route('/idw',methods=['GET'])
def getInterpolated():
    message={}
    message['result']="Success"
    try:
        grid = MyGrid()
        grid.initializeMatrix()
        grid.updateAQMatrix()
    except:
        message['result']="Error al generar las medidas interpoladas con IDW"
    return jsonify(message)


@cron.interval_schedule(hours=1)
def updateAQMap():
    message={}
    message['result']="Success"
    try:
        print('starting...')
        qaira=Qaira()
        qaira.getAll()
        grid = MyGrid()
        grid.initializeMatrix()
        grid.updateAQMatrix()
    except:
        message['result']="Error al generar las medidas interpoladas con IDW"



atexit.register(lambda: cron.shutdown(wait=False))
if __name__=="__main__":
    app.run()