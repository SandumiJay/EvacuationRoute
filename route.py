import csv
from flask import jsonify
import json
import random
import numpy as np
import heapq
import collections
from math import radians, cos, sin, asin, sqrt

with open('C:\\SLIIT\\Research\\Implementation\\PythonModel\\junction_network.json') as json_file:
    data =json.load(json_file)

Location = collections.namedtuple("Location", "ID Longitude Latitude".split())
junction={}
for i in range(len(data['features'])):
    id,lon,lat=int(data['features'][i]['attributes']['FID']),data['features'][i]['geometry']['x'],data['features'][i]['geometry']['y']
    junction[i]=Location(id,lon,lat)
	
r=6371000 #radius of the earth in m
def distance(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

# print(sorted(junction.values(), key= lambda d: distance(d.Longitude, d.Latitude,79.899511,6.9424922)))

lvfloodStatus = {
    'no flood': 1,
    'minor flood': 2,
    'moderate flood': 3,
    'major flood': 4,
    'record flood': 5
}

lvDamageStatus = {
    'fully damage': 4,
    'moderate damage': 3,
    'minor damage': 2,
    'no damage': 1
}

flood = ['no flood', 'minor flood', 'moderate flood', 'major flood', 'record flood']
damage = ['fully damage', 'moderate damage', 'minor damage', 'no damage']





def getFloodStatus(ID):
    floodstatus=random.choice(flood)
    return lvfloodStatus[floodstatus]
getFloodStatus(0)   


def getDamageStatus(ID):
    damagestatus=random.choice(damage)
    return lvDamageStatus[damagestatus]
getDamageStatus(0) 


def calHeuristic(ID):   
    floodStatus=getFloodStatus(ID)
    damageStatus=getDamageStatus(ID)
    
    heuristic=floodStatus+damageStatus
    
    return heuristic/9
	
def getjunction(ID):
    lvJunction ={
		"id": junction[ID].ID,
        "Longitude" : junction[ID].Longitude,
         "Latitude" : junction[ID].Latitude
    }
    return lvJunction
	
def getNearestLocation(startL_Longitude,startL_Latitude,n=4):
    lvnearest=sorted(junction, key=lambda x: distance(startL_Longitude,startL_Latitude, junction[x].Longitude,junction[x].Latitude))[1:n+1]
    return getjunction(lvnearest[0])	
def getneighbors(startlocation, n=4):
    return sorted(junction, key=lambda x: distance(junction[startlocation].Longitude,junction[startlocation].Latitude, junction[x].Longitude,junction[x].Latitude))[1:n+1]
	
def getParent(closedlist, index):
    path = []
    while index is not None:
        path.append(index)
        print(path)
        index = closedlist.get(index, None)
        print(index)
    return [junction[i] for i in path[::-1]]
	
	
def evacuationRoute(junction,source,destination):
    output=[]
    Node = collections.namedtuple("Node", "ID F G H parentID Longitude Latitude".split())
    source=junction[source]
    destination=junction[destination]
    print(source)
    h = distance(source.Longitude,source.Latitude, destination.Longitude,destination.Latitude)
    openlist = [(h, Node(source.ID,h,0, h, None,source.Longitude,source.Latitude))] # heap
    closedlist = {} # map visited nodes to parent
    i=0
    while len(openlist) >= 1:
        print("-------------------------------")
        print(i)
       
        currentLocation = heapq.heappop(openlist)
        #print(currentLocation[1].ID)
        if currentLocation[1].ID in closedlist:
            continue
            
        #print(currentLocation[1].ID)
        closedlist[currentLocation[1].ID] = currentLocation[1].parentID
        #print(closedlist)
        print("***************")
        if currentLocation[1].ID == destination.ID:
            print("Complete")
            print(closedlist)
            for p in getParent(closedlist, currentLocation[1].ID):
                output.append(p)
                print(p)
            break
            
        for other in getneighbors(currentLocation[1].ID):
            g = currentLocation[1].G+distance(currentLocation[1].Longitude,currentLocation[1].Latitude, junction[other].Longitude, junction[other].Latitude)
            h = distance(junction[other].Longitude, junction[other].Latitude, destination.Longitude, destination.Latitude)
            f = (g + h) * calHeuristic(currentLocation[1].ID)
            print(currentLocation[1].ID)
            print(f)
            heapq.heappush(openlist, (f, Node(junction[other].ID, f, g, h, currentLocation[1].ID,junction[other].Longitude,junction[other].Latitude)))
        i=i+1
    return output