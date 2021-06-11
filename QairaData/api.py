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
f = open("/var/www/html/TESIS2021/QairaData/Configuration/config.json","r") # Development route
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
    initial_timestamp=datetime.utcnow()-timedelta(hours=1,minutes=10)
    YEAR = str(initial_timestamp.year)
    MONTH = str(initial_timestamp.month).zfill(2)
    DATE = str(initial_timestamp.day).zfill(2)
    HOUR = str(initial_timestamp.hour).zfill(2)
    timestamp = datetime.strptime( YEAR+'-'+MONTH+'-'+DATE+' '+HOUR+':00:00', '%Y-%m-%d %H:%M:%S')
    pollutant=request.args.get("pollutant")
    print('pollutant:   ',pollutant,' -----------')
    try:
        mydb=psycopg2.connect(host=data['host'],port=data['port'],database=data['database'],user=data['username'],password=data['password'])
        print('connected')
        getPollutants =("select s.\"qHawax_ID\", s.lat,s.lon,m.\"Value\" from {}.qaira_sensors s, {}.pollutant p, (select * from {}.metricslima  where \"timestamp\"=%(timestam)s) m where m.\"idPollutant\"= p.\"idPollutant\" and p.\"pollutantName\"=%(poll)s and s.\"qHawax_ID\"=m.\"qHawaxID\"".format(schema,schema,schema))
        if pollutant is not None:
            param={'timestam':timestamp,'poll':pollutant}
            cursor=mydb.cursor()
            cursor.execute(getPollutants,param)
            sensors=list(cursor.fetchall())
            if len(sensors)!=0:
                for (qhawax_id,lat,lon,value) in sensors:
                    if value is None:
                        value=0
                    sensor={'id':qhawax_id,'lat':lat,'lon':lon, 'pollutantValue':value}
                    message['sensors'].append(sensor)
            else:
                cursor= mydb.cursor()
                getMet=("SELECT \"timestamp\" FROM {}.metricslima order by \"timestamp\" desc limit 1;".format(schema))
                cursor.execute(getMet)
                aux=list(cursor.fetchall())
                tims=0
                for (time) in aux:
                    tims=time[0]
                param={'timestam':tims,'poll':pollutant}
                cursor=mydb.cursor()
                cursor.execute(getPollutants,param)
                sensors=list(cursor.fetchall())
                timestamp=tims
                for (qhawax_id,lat,lon,value) in sensors:
                    if value is None:
                        value=0
                    sensor={'id':qhawax_id,'lat':lat,'lon':lon, 'pollutantValue':value}

                    message['sensors'].append(sensor)
        else:
            print('not poll')
            param={'timestam':timestamp,'poll':'CO'}
            cursor=mydb.cursor()
            cursor.execute(getPollutants,param)
            sensors=list(cursor.fetchall())
            if len(sensors)!=0:
                print('got sensors')
                for (qhawax_id,lat,lon,value) in sensors:
                    if value is None:
                        value=0
                    sensor={'id':qhawax_id,'lat':lat,'lon':lon, 'pollutantValue':0.00}
                    message['sensors'].append(sensor)
            else:
                print('not recent metrics')
                tims=0
                try:
                    cursor1= mydb.cursor()
                    getMet=("SELECT \"timestamp\" FROM {}.metricslima order by \"timestamp\" desc limit 1;".format(schema))
                    cursor1.execute(getMet)
                    aux=list(cursor1.fetchall())
                    tims=0
                    for (time) in aux:
                        tims=time[0]
                    print(tims)
                    timestamp=tims
                except Error as error:
                    print(error)
                finally:
                    cursor1.close()
                param={'timestam':tims,'poll':'CO'}
                try:
                    cursor2=mydb.cursor()
                    cursor2.execute(getPollutants,param)
                    sensors=list(cursor2.fetchall())
                except Error as error:
                    print(error)
                finally:
                    cursor2.close()
                for (qhawax_id,lat,lon,value) in sensors:
                    if value is None:
                        value=0
                    sensor={'id':qhawax_id,'lat':lat,'lon':lon, 'pollutantValue':0.00}
                    message['sensors'].append(sensor)

    except Exception as error:
        print(error)

    finally:
        cursor.close()
        mydb.close()
    message['timestamp']=timestamp
    return jsonify(message)
@app.route('/cells',methods=['GET'])
def getCells():
    message={}
    message['cells']=[]
    try:
        mydb=psycopg2.connect(host=data['host'],port=data['port'],database=data['database'],user=data['username'],password=data['password'])
        getCells=("select * from {}.cellsdata".format(schema))
        cursor=mydb.cursor()
        cursor.execute(getCells)
        cells=list(cursor.fetchall())
        for(idcell,midLat,midLon) in cells:
            cell={}
            cell['id']=idcell
            cell['coords']=[midLon,midLat]
            message['cells'].append(cell)
    except Error as error:
        print(error)
    finally:
        cursor.close()
        mydb.close()
    return jsonify(message)

def getColor(value,poll):
    i=0
    if not poll:
        return 'green'
    else:
        if poll=='CO':
            i=value*100/10000
            if i>0 and i<50:
                return 'green'
            else:
                if i>50 and i<100:
                    return 'yellow'

                else:
                    if i>100 and i<150:
                        return 'orange'
                    else:
                        return 'red'
        if poll=='H2S':
            i=value*100/150
            if i>0 and i<50:
                return 'green'
            else:
                if i>50 and i<100:
                    return 'yellow'

                else:
                    if i>100 and i<1000:
                        return 'orange'
                    else:
                        return 'red'
        if poll=='NO2':
            i=value*100/200
            if i>0 and i<50:
                return 'green'
            else:
                if i>50 and i<100:
                    return 'yellow'

                else:
                    if i>100 and i<150:
                        return 'orange'
                    else:
                        return 'red'
        if poll=='O3':
            i=value*100/120
            if i>0 and  i<50:
                return 'green'
            else:
                if i>50 and i<100:
                    return 'yellow'

                else:
                    if i>100 and i<175:
                        return 'orange'
                    else:
                        return 'red'


        if poll=='PM10':
            i=value*100/150
            if i>0 and i<50:
                return 'green'
            else:
                if i>50 and i<100:
                    return 'yellow'

                else:
                    if i>100 and i<167:
                        return 'orange'
                    else:
                        return 'red'
        if poll=='PM25':
            i=value*100/25
            if i>0 and i<50:
                return 'green'
            else:
                if i>50 and i<100:
                    return 'yellow'
                else:
                    if i>100 and i<500:
                        return 'orange'
                    else:
                        return 'red'
        if 'SO2':
            i=value*100/20
            if i>0 and i<50:
                return 'green'
            else:
                if i>50 and i<100:
                    return 'yellow'

                else:
                    if i>100 and i<625:
                        return 'orange'
                    else:
                        return 'red'
    return 'green'
@app.route('/densityMap',methods=['GET'])
def getDensity():
    message={}
    message['type']="FeatureCollection"
    message['features']=[]
    pollutant=request.args.get("pollutant")
    time=0
    try:
        mydb=psycopg2.connect(host=data['host'],port=data['port'],database=data['database'],user=data['username'],password=data['password'])
        getMap =("select j.idcell,j.\"interpolatedValiue\",j.\"timestamp\",\"midLat\"-(0.001*100/222) as southLat, \"midLat\"+(0.001*100/222) as northLat,\"midLon\"-(0.001*100/222) as westLon,\"midLon\"+(0.001*100/222) as eastLon from (select i.idcell,i.\"interpolatedValiue\",i.\"timestamp\",p.\"pollutantName\" from {}.pollutant p inner join {}.interpolatedmetrics i on p.\"idPollutant\"=i.\"idPollutant\"	where p.\"pollutantName\"=%(poll)s) j inner join {}.cellsdata c on j.idcell=c.idcell".format(schema,schema,schema))
        if pollutant is not None:
            param={'poll':pollutant}
            cursor=mydb.cursor()
            cursor.execute(getMap,param)
            sensors=list(cursor.fetchall())
            for (idcell,value,timestamp,southLat,northLat,westLon,eastLon) in sensors:
                time=timestamp
                prop={'name':idcell,'pollution':value,'color':getColor(value,pollutant)}
                geom={'type':'Polygon','coordinates':[[[westLon,southLat],[westLon,northLat],[eastLon,northLat],[eastLon,southLat],[westLon,southLat]]]}
                cell={'type':'Feature', 'id':idcell, 'properties':prop, 'geometry': geom}
                message['features'].append(cell)
            message['timestamp']=time
        else:
            param={'poll':'CO'}
            cursor=mydb.cursor()
            cursor.execute(getMap,param)
            sensors=list(cursor.fetchall())
            for (idcell,value,timestamp,southLat,northLat,westLon,eastLon) in sensors:
                time=timestamp
                prop={'name':idcell,'pollution':0.00,'color':'red'}
                geom={'type':'Polygon','coordinates':[[[westLon,southLat],[westLon,northLat],[eastLon,northLat],[eastLon,southLat],[westLon,southLat]]]}
                cell={'type':'Feature', 'id':idcell, 'properties':prop, 'geometry': geom}
                message['features'].append(cell)
            message['timestamp']=time


    except Error as error:
        print(error)
    finally:
        cursor.close()
        mydb.close()
    return jsonify(message)


def changeCoords(response):
    coords=response['paths'][0]['points']['coordinates']
    for  i in range(len(coords)):
        coords[i]=[coords[i][1],coords[i][0]]
    response['paths'][0]['points']['coordinates']=coords
    return response

@app.route('/route',methods=['GET'])
def getRoutes():
    pollutant=request.args.get('pollutant')
    startpointlat=request.args.get('startpointlat')
    startpointlon=request.args.get('startpointlon')
    endpointlat=request.args.get('endpointlat')
    endpointlon=request.args.get('endpointlon')
    if startpointlat is None or startpointlon is None or endpointlat is None or endpointlon is None:
        return "Es necesario un punto de inicio y uno de fin"
    else:
        if pollutant is None:
            requestdijkstra="?point="+str(startpointlat)+","+str(startpointlon)+"&point="+str(endpointlat)+","+str(endpointlon)+"&type=json&locale=es-ES&elevation=false&profile=foot&algorithm=dijkstra&use_miles=false&points_encoded=false"
            response=requests.get(routingUrl+requestdijkstra)
            response=response.json()
            return jsonify(response)
        elif pollutant=='CO':
            requestdijkstra="?point="+str(startpointlat)+","+str(startpointlon)+"&point="+str(endpointlat)+","+str(endpointlon)+"&type=json&locale=es-ES&elevation=false&profile=qairaco&algorithm=dijkstra&use_miles=false&points_encoded=false"
            response=requests.get(routingUrl+requestdijkstra)
            response=response.json()
            return jsonify(response)
        elif pollutant=='H2S':
            requestdijkstra="?point="+str(startpointlat)+","+str(startpointlon)+"&point="+str(endpointlat)+","+str(endpointlon)+"&type=json&locale=es-ES&elevation=false&profile=qairah2&algorithm=dijkstra&use_miles=false&points_encoded=false"
            response=requests.get(routingUrl+requestdijkstra)
            response=response.json()
            return jsonify(response)
        elif pollutant=='NO2':
            requestdijkstra="?point="+str(startpointlat)+","+str(startpointlon)+"&point="+str(endpointlat)+","+str(endpointlon)+"&type=json&locale=es-ES&elevation=false&profile=qairano&algorithm=dijkstra&use_miles=false&points_encoded=false"
            response=requests.get(routingUrl+requestdijkstra)
            response=response.json()
            return jsonify(response)
        elif pollutant=='O3':
            requestdijkstra="?point="+str(startpointlat)+","+str(startpointlon)+"&point="+str(endpointlat)+","+str(endpointlon)+"&type=json&locale=es-ES&elevation=false&profile=qairao3&algorithm=dijkstra&use_miles=false&points_encoded=false"
            response=requests.get(routingUrl+requestdijkstra)
            response=response.json()
            return jsonify(response)
        elif pollutant=='PM10':
            requestdijkstra="?point="+str(startpointlat)+","+str(startpointlon)+"&point="+str(endpointlat)+","+str(endpointlon)+"&type=json&locale=es-ES&elevation=false&profile=qairapm1&algorithm=dijkstra&use_miles=false&points_encoded=false"
            response=requests.get(routingUrl+requestdijkstra)
            response=response.json()
            return jsonify(response)
        elif pollutant=='PM25':
            requestdijkstra="?point="+str(startpointlat)+","+str(startpointlon)+"&point="+str(endpointlat)+","+str(endpointlon)+"&type=json&locale=es-ES&elevation=false&profile=qairapm2&algorithm=dijkstra&use_miles=false&points_encoded=false"
            response=requests.get(routingUrl+requestdijkstra)
            response=response.json()
            return jsonify(response)
        elif pollutant=='SO2':
            requestdijkstra="?point="+str(startpointlat)+","+str(startpointlon)+"&point="+str(endpointlat)+","+str(endpointlon)+"&type=json&locale=es-ES&elevation=false&profile=qairaso2&algorithm=dijkstra&use_miles=false&points_encoded=false"
            response=requests.get(routingUrl+requestdijkstra)
            response=response.json()
            return jsonify(response)
""" 
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


 """
atexit.register(lambda: cron.shutdown(wait=False))
if __name__=="__main__":
    socketio.run(app,host='0.0.0.0', port=5001)

