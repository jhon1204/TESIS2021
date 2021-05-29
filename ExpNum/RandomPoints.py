import random
import json
southLat=-12.0605
northLat=-12.0350
westLon=-77.0566
eastLon=-77.0026

def generatePoints(N):
    data={}
    data['StartPoints']=[]
    data['EndPoints']=[]
    for i in range(N):
        data['StartPoints'].append(getRandomPoint(southLat,northLat,westLon,eastLon))
    for i in range(N):
        data['EndPoints'].append(getRandomPoint(southLat,northLat,westLon,eastLon))
    with open('randomPoints.json','w') as outFile:
        json.dump(data,outFile)


def getRandomPoint(southLat,northLat,westLon,eastLon):
    response={}
    lat= random.uniform(southLat,northLat)
    lon= random.uniform(westLon,eastLon)
    response['lat']=lat
    response['lon']=lon
    return response

if __name__=='__main__':
    generatePoints(10)