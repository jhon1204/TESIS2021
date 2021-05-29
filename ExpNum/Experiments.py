import math
import json
import requests
from RandomPoints import generatePoints
# http://localhost:8989/maps/?point=-12.044777%2C-77.047291&point=-12.050653%2C-77.022486&locale=es-ES&elevation=false&profile=qairapm2&use_miles=false
# http://localhost:8989/maps/?point=-12.047421%2C-77.034416&point=-12.054598%2C-77.032871&locale=es-ES&elevation=false&profile=foot&algorithm=astar&astar.approximation=Qaira&use_miles=false&layer=Omniscale
urlBase="http://localhost:8989/route"
def baseExperimentation():
    with open('randomPoints.json') as json_File:
        data=json.load(json_File)
        # print('START POINTS------------------------------------------------------')
        # for point in data['StartPoints']:
        #     print("LAT: "+str(point['lat'])+"  LON: "+ str(point['lon']))
        # print('END POINTS------------------------------------------------------')
        # for point in data['EndPoints']:
        #     print("LAT: "+str(point['lat'])+"  LON: "+ str(point['lon']))
        responses={}
        # responses['responsesDijkstra']=[]
        # responses['responsesAstar']=[]
        responses['responsesACO']=[]
        for i in range(len(data['StartPoints'])):
            start=data['StartPoints'][i]
            end= data['EndPoints'][i]
            requestACO="?point="+str(start['lat'])+","+str(start['lon'])+"&point="+str(end['lat'])+","+str(end['lon'])+"&type=json&locale=es-ES&elevation=false&profile=foot&algorithm=aco&use_miles=false"
            responseACO= requests.get(urlBase+requestACO)
            if responseACO.status_code==200:
                responses['responsesACO'].append(responseACO.json())
            # requestdijkstra="?point="+str(start['lat'])+","+str(start['lon'])+"&point="+str(end['lat'])+","+str(end['lon'])+"&type=json&locale=es-ES&elevation=false&profile=foot&algorithm=dijkstra&use_miles=false"
            # requestastar="?point="+str(start['lat'])+","+str(start['lon'])+"&point="+str(end['lat'])+","+str(end['lon'])+"&type=json&locale=es-ES&elevation=false&profile=foot&algorithm=astar&astar.approximation=BeelineAccurate&use_miles=false"
            # response = requests.get(urlBase+requestdijkstra)
            # if response.status_code ==200:
            #     responses['responsesDijkstra'].append(response.json())
            # response2=requests.get(urlBase+requestastar)
            # if response2.status_code==200:
            #     responses['responsesAstar'].append(response2.json())
        with open('baseExperimentsACO.json','w') as outFile:
            json.dump(responses,outFile)

def COExperimentation():
    with open('randomPoints.json') as json_File:
        data=json.load(json_File)
        # print('START POINTS------------------------------------------------------')
        # for point in data['StartPoints']:
        #     print("LAT: "+str(point['lat'])+"  LON: "+ str(point['lon']))
        # print('END POINTS------------------------------------------------------')
        # for point in data['EndPoints']:
        #     print("LAT: "+str(point['lat'])+"  LON: "+ str(point['lon']))
        responses={}
        responses['responsesDijkstra']=[]
        responses['responsesAstar']=[]
        #responses['responsesACO']=[]
        for i in range(len(data['StartPoints'])):
            start=data['StartPoints'][i]
            end= data['EndPoints'][i]
            # requestACO="?point="+str(start['lat'])+","+str(start['lon'])+"&point="+str(end['lat'])+","+str(end['lon'])+"&type=json&locale=es-ES&elevation=false&profile=qairaco&algorithm=aco&use_miles=false"
            # responseACO= requests.get(urlBase+requestACO)
            # if responseACO.status_code==200:
            #     responses['responsesACO'].append(responseACO.json())
            requestdijkstra="?point="+str(start['lat'])+","+str(start['lon'])+"&point="+str(end['lat'])+","+str(end['lon'])+"&type=json&locale=es-ES&elevation=false&profile=qairaco&algorithm=dijkstra&use_miles=false"
            requestastar="?point="+str(start['lat'])+","+str(start['lon'])+"&point="+str(end['lat'])+","+str(end['lon'])+"&type=json&locale=es-ES&elevation=false&profile=qairaco&algorithm=astar&astar.approximation=Qaira&use_miles=false"
            response = requests.get(urlBase+requestdijkstra)
            if response.status_code ==200:
                responses['responsesDijkstra'].append(response.json())
            response2=requests.get(urlBase+requestastar)
            if response2.status_code==200:
                responses['responsesAstar'].append(response2.json())
        with open('COExperiments2505.json','w') as outFile:
            json.dump(responses,outFile)
def NO2Experimentation():
    with open('randomPoints.json') as json_File:
        data=json.load(json_File)
        # print('START POINTS------------------------------------------------------')
        # for point in data['StartPoints']:
        #     print("LAT: "+str(point['lat'])+"  LON: "+ str(point['lon']))
        # print('END POINTS------------------------------------------------------')
        # for point in data['EndPoints']:
        #     print("LAT: "+str(point['lat'])+"  LON: "+ str(point['lon']))
        responses={}
        responses['responsesDijkstra']=[]
        responses['responsesAstar']=[]
        #responses['responsesACO']=[]
        for i in range(len(data['StartPoints'])):
            start=data['StartPoints'][i]
            end= data['EndPoints'][i]
            # requestACO="?point="+str(start['lat'])+","+str(start['lon'])+"&point="+str(end['lat'])+","+str(end['lon'])+"&type=json&locale=es-ES&elevation=false&profile=qairano&algorithm=aco&use_miles=false"
            # responseACO= requests.get(urlBase+requestACO)
            # if responseACO.status_code==200:
            #     responses['responsesACO'].append(responseACO.json())
            requestdijkstra="?point="+str(start['lat'])+","+str(start['lon'])+"&point="+str(end['lat'])+","+str(end['lon'])+"&type=json&locale=es-ES&elevation=false&profile=qairano&algorithm=dijkstra&use_miles=false"
            requestastar="?point="+str(start['lat'])+","+str(start['lon'])+"&point="+str(end['lat'])+","+str(end['lon'])+"&type=json&locale=es-ES&elevation=false&profile=qairano&algorithm=astar&astar.approximation=Qaira&use_miles=false"
            response = requests.get(urlBase+requestdijkstra)
            if response.status_code ==200:
                responses['responsesDijkstra'].append(response.json())
            response2=requests.get(urlBase+requestastar)
            if response2.status_code==200:
                responses['responsesAstar'].append(response2.json())
        with open('NO2Experiments2505.json','w') as outFile:
            json.dump(responses,outFile)
def PM10Experimentation():
    with open('randomPoints.json') as json_File:
        data=json.load(json_File)
        # print('START POINTS------------------------------------------------------')
        # for point in data['StartPoints']:
        #     print("LAT: "+str(point['lat'])+"  LON: "+ str(point['lon']))
        # print('END POINTS------------------------------------------------------')
        # for point in data['EndPoints']:
        #     print("LAT: "+str(point['lat'])+"  LON: "+ str(point['lon']))
        responses={}
        responses['responsesDijkstra']=[]
        responses['responsesAstar']=[]
        #responses['responsesACO']=[]
        for i in range(len(data['StartPoints'])):
            start=data['StartPoints'][i]
            end= data['EndPoints'][i]
            # requestACO="?point="+str(start['lat'])+","+str(start['lon'])+"&point="+str(end['lat'])+","+str(end['lon'])+"&type=json&locale=es-ES&elevation=false&profile=qairapm1&algorithm=aco&use_miles=false"
            # responseACO= requests.get(urlBase+requestACO)
            # if responseACO.status_code==200:
            #     responses['responsesACO'].append(responseACO.json())
            requestdijkstra="?point="+str(start['lat'])+","+str(start['lon'])+"&point="+str(end['lat'])+","+str(end['lon'])+"&type=json&locale=es-ES&elevation=false&profile=qairapm1&algorithm=dijkstra&use_miles=false"
            requestastar="?point="+str(start['lat'])+","+str(start['lon'])+"&point="+str(end['lat'])+","+str(end['lon'])+"&type=json&locale=es-ES&elevation=false&profile=qairapm1&algorithm=astar&astar.approximation=Qaira&use_miles=false"
            response = requests.get(urlBase+requestdijkstra)
            if response.status_code ==200:
                responses['responsesDijkstra'].append(response.json())
            response2=requests.get(urlBase+requestastar)
            if response2.status_code==200:
                responses['responsesAstar'].append(response2.json())
        with open('PM10Experiments2505.json','w') as outFile:
            json.dump(responses,outFile)

def PM25Experimentation():
    with open('randomPoints.json') as json_File:
        data=json.load(json_File)
        # print('START POINTS------------------------------------------------------')
        # for point in data['StartPoints']:
        #     print("LAT: "+str(point['lat'])+"  LON: "+ str(point['lon']))
        # print('END POINTS------------------------------------------------------')
        # for point in data['EndPoints']:
        #     print("LAT: "+str(point['lat'])+"  LON: "+ str(point['lon']))
        responses={}
        responses['responsesDijkstra']=[]
        responses['responsesAstar']=[]
        #responses['responsesACO']=[]
        for i in range(len(data['StartPoints'])):
            start=data['StartPoints'][i]
            end= data['EndPoints'][i]
            # requestACO="?point="+str(start['lat'])+","+str(start['lon'])+"&point="+str(end['lat'])+","+str(end['lon'])+"&type=json&locale=es-ES&elevation=false&profile=qairapm2&algorithm=aco&use_miles=false"
            # responseACO= requests.get(urlBase+requestACO)
            # if responseACO.status_code==200:
            #     responses['responsesACO'].append(responseACO.json())
            requestdijkstra="?point="+str(start['lat'])+","+str(start['lon'])+"&point="+str(end['lat'])+","+str(end['lon'])+"&type=json&locale=es-ES&elevation=false&profile=qairapm2&algorithm=dijkstra&use_miles=false"
            requestastar="?point="+str(start['lat'])+","+str(start['lon'])+"&point="+str(end['lat'])+","+str(end['lon'])+"&type=json&locale=es-ES&elevation=false&profile=qairapm2&algorithm=astar&astar.approximation=Qaira&use_miles=false"
            response = requests.get(urlBase+requestdijkstra)
            if response.status_code ==200:
                responses['responsesDijkstra'].append(response.json())
            response2=requests.get(urlBase+requestastar)
            if response2.status_code==200:
                responses['responsesAstar'].append(response2.json())
        with open('PM25Experiments2505.json','w') as outFile:
            json.dump(responses,outFile)


if __name__=="__main__":
    PM25Experimentation()