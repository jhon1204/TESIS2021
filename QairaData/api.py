import flask
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin
from flask import request, jsonify
import requests
from Utils.Qaira import Qaira
from Utils.Grid import MyGrid
from apscheduler.scheduler import Scheduler
import atexit
import json
import os
import psycopg2
from psycopg2 import DatabaseError as Error
from datetime import datetime,date,timedelta


app = flask.Flask(__name__)
app.config["DEBUG"] = True
socketio = SocketIO(app,cors_allowed_origins="*",async_handlers=True)
CORS(app)

cron = Scheduler(daemon=True)
cron.start()
f = open("/home/ubuntu/Benites/TESIS2021/QairaData/Configuration/config.json","r") # Development route
data = json.load(f)
f.close()
schema=data['schema']
routingUrl=data['routingUrl']
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

@app.route('/sensors',methods=['GET'])
def getSensors():
    message={}
    message['sensors']=[]
    initial_timestamp=datetime.now()- timedelta(hours=5)
    YEAR = str(initial_timestamp.year)
    MONTH = str(initial_timestamp.month).zfill(2)
    DATE = str(initial_timestamp.day).zfill(2)
    HOUR = str(initial_timestamp.hour).zfill(2)
    timestamp = datetime.strptime( YEAR+'-'+MONTH+'-'+DATE+' '+HOUR+':00:00', '%Y-%m-%d %H:%M:%S')
    pollutant=request.form.get("pollutant")
    try:
        mydb=psycopg2.connect(host=data['host'],port=data['port'],database=data['database'],user=data['username'],password=data['password'])
        print('connected')
        getPollutants =("select s.\"qHawax_ID\", s.lat,s.lon,m.\"Value\" from {}.qaira_sensors s, {}.pollutant p, (select * from {}.metricslima  where \"timestamp\"=%(timestam)s) m where m.\"idPollutant\"= p.\"idPollutant\" and p.\"pollutantName\"=%(poll)s and s.\"qHawax_ID\"=m.\"qHawaxID\"".format(schema,schema,schema))
        if pollutant is not None:
            param={'timestam':timestamp,'poll':pollutant}
            cursor=mydb.cursor()
            cursor.execute(getPollutants,param)
            sensors=list(cursor.fetchall())
            for (qhawax_id,lat,lon,value) in sensors:
                sensor={'id':qhawax_id,'lat':lat,'lon':lon, 'pollutantValue':value}
                message['sensors'].append(sensor)
        else:
            print('not poll')
            print(getPollutants)
            param={'timestam':timestamp,'poll':'CO'}
            cursor=mydb.cursor()
            print(param)
            cursor.execute(getPollutants,param)
            print("sdads",cursor.rowcount)
            sensors=list(cursor.fetchall())
            print(sensors)
            for (qhawax_id,lat,lon,value) in sensors:
                sensor={'id':qhawax_id,'lat':lat,'lon':lon, 'pollutantValue':0.00}
                message['sensors'].append(sensor)

    except Exception as error:
        print(error)

    finally:
        cursor.close()
        mydb.close()
    return jsonify(message)

@app.route('/densityMap',methods=['GET'])
def getDensity():
    message={}
    message['type']="FeatureCollection"
    message['features']=[]
    pollutant=request.form.get("pollutant")
    try:
        mydb=psycopg2.connect(host=data['host'],port=data['port'],database=data['database'],user=data['username'],password=data['password'])
        getMap =("select j.idcell,j.\"interpolatedValiue\",\"midLat\"-(0.001*100/222) as southLat, \"midLat\"+(0.001*100/222) as northLat,\"midLon\"-(0.001*100/222) as westLon,\"midLon\"+(0.001*100/222) as eastLon from (select i.idcell,i.\"interpolatedValiue\",p.\"pollutantName\" from {}.pollutant p inner join {}.interpolatedmetrics i on p.\"idPollutant\"=i.\"idPollutant\"	where p.\"pollutantName\"=%(poll)s) j inner join {}.cellsdata c on j.idcell=c.idcell".format(schema,schema,schema))
        if pollutant is not None:
            param={'poll':pollutant}
            cursor=mydb.cursor()
            cursor.execute(getMap,param)
            sensors=list(cursor.fetchall())
            for (idcell,value,southLat,northLat,westLon,eastLon) in sensors:
                prop={'name':idcell,'pollution':value}
                geom={'type':'Polygon','coordinates':[[[southLat,westLon],[northLat,westLon],[northLat,eastLon],[southLat,eastLon],[southLat,westLon]]]}
                cell={'type':'Feature', 'id':idcell, 'properties':prop, 'geometry': geom}
                message['features'].append(cell)
        else:
            param={'poll':'CO'}
            cursor=mydb.cursor()
            cursor.execute(getMap,param)
            sensors=list(cursor.fetchall())
            for (idcell,value,southLat,northLat,westLon,eastLon) in sensors:
                prop={'name':idcell,'pollution':0.00}
                geom={'type':'Polygon','coordinates':[[[southLat,westLon],[northLat,westLon],[northLat,eastLon],[southLat,eastLon],[southLat,westLon]]]}
                cell={'type':'Feature', 'id':idcell, 'properties':prop, 'geometry': geom}
                message['features'].append(cell)


    except Error as error:
        print(error)
    finally:
        cursor.close()
        mydb.close()
    return jsonify(message)

@app.route('/route',methods=['GET'])
def getRoutes():
    pollutant=request.form.get('pollutant')
    startpoint=request.form.get('startpoint')
    endpoint=request.form.get('endpoint')
    message={}
    if startpoint is None or endpoint is None:
        return "Es necesario un punto de inicio y uno de fin"
    else:
        if pollutant is None:
            requestdijkstra="?point="+str(startpoint['lat'])+","+str(startpoint['lon'])+"&point="+str(endpoint['lat'])+","+str(endpoint['lon'])+"&type=json&locale=es-ES&elevation=false&profile=foot&algorithm=dijkstra&use_miles=false&points_encoded=false"
            response=requests.get(routingUrl+requestdijkstra)
            return jsonify(response.json())
        elif pollutant=='CO':
            requestdijkstra="?point="+str(startpoint['lat'])+","+str(startpoint['lon'])+"&point="+str(endpoint['lat'])+","+str(endpoint['lon'])+"&type=json&locale=es-ES&elevation=false&profile=qairaco&algorithm=dijkstra&use_miles=false&points_encoded=false"
            response=requests.get(routingUrl+requestdijkstra)
            return jsonify(response.json())
        elif pollutant=='H2S':
            requestdijkstra="?point="+str(startpoint['lat'])+","+str(startpoint['lon'])+"&point="+str(endpoint['lat'])+","+str(endpoint['lon'])+"&type=json&locale=es-ES&elevation=false&profile=qairah2&algorithm=dijkstra&use_miles=false&points_encoded=false"
            response=requests.get(routingUrl+requestdijkstra)
            return jsonify(response.json())
        elif pollutant=='NO2':
            requestdijkstra="?point="+str(startpoint['lat'])+","+str(startpoint['lon'])+"&point="+str(endpoint['lat'])+","+str(endpoint['lon'])+"&type=json&locale=es-ES&elevation=false&profile=qairano&algorithm=dijkstra&use_miles=false&points_encoded=false"
            response=requests.get(routingUrl+requestdijkstra)
            return jsonify(response.json())
        elif pollutant=='O3':
            requestdijkstra="?point="+str(startpoint['lat'])+","+str(startpoint['lon'])+"&point="+str(endpoint['lat'])+","+str(endpoint['lon'])+"&type=json&locale=es-ES&elevation=false&profile=qairao3&algorithm=dijkstra&use_miles=false&points_encoded=false"
            response=requests.get(routingUrl+requestdijkstra)
            return jsonify(response.json())
        elif pollutant=='PM10':
            requestdijkstra="?point="+str(startpoint['lat'])+","+str(startpoint['lon'])+"&point="+str(endpoint['lat'])+","+str(endpoint['lon'])+"&type=json&locale=es-ES&elevation=false&profile=qairapm1&algorithm=dijkstra&use_miles=false&points_encoded=false"
            response=requests.get(routingUrl+requestdijkstra)
            return jsonify(response.json())
        elif pollutant=='PM25':
            requestdijkstra="?point="+str(startpoint['lat'])+","+str(startpoint['lon'])+"&point="+str(endpoint['lat'])+","+str(endpoint['lon'])+"&type=json&locale=es-ES&elevation=false&profile=qairapm2&algorithm=dijkstra&use_miles=false&points_encoded=false"
            response=requests.get(routingUrl+requestdijkstra)
            return jsonify(response.json())
        elif pollutant=='SO2':
            requestdijkstra="?point="+str(startpoint['lat'])+","+str(startpoint['lon'])+"&point="+str(endpoint['lat'])+","+str(endpoint['lon'])+"&type=json&locale=es-ES&elevation=false&profile=qairaso2&algorithm=dijkstra&use_miles=false&points_encoded=false"
            response=requests.get(routingUrl+requestdijkstra)
            return jsonify(response.json())

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
    socketio.run(app,host='0.0.0.0', port=5001)

