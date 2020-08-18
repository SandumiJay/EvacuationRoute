
# coding: utf-8

# In[319]:


import googlemaps
import csv
import json
import random
import numpy as np
import heapq
import collections
from math import radians, cos, sin, asin, sqrt


# In[320]:


gmaps = googlemaps.Client(key='AIzaSyBtcjoz5jSOsIywzlwpLtZldwpWa_aTu2Y')


# In[68]:


with open('C:\\SLIIT\\Research\\Implementation\\PythonModel\\junction_network.json') as json_file:
    data =json.load(json_file)


# In[69]:


data['features']


# In[105]:


Location = collections.namedtuple("Location", "ID Longitude Latitude".split())
junction={}
for i in range(len(data['features'])):
#     print(data['features'][i]['attributes']['FID'])
#     arr.append(data['features'][i]['attributes']['FID'])
#     junction['ID']=data['features'][i]['attributes']['FID']
#     junction['Coordination']=data['features'][i]['geometry']
#     arr={'ID':data['features'][i]['attributes']['FID'],
#              'Longitude':data['features'][i]['geometry']['x'],
#                 'Latitude':data['features'][i]['geometry']['y']}
    id,lon,lat=int(data['features'][i]['attributes']['FID']),data['features'][i]['geometry']['x'],data['features'][i]['geometry']['y']
    junction[i]=Location(id,lon,lat)


# In[106]:


junction.values()


# In[316]:


from math import cos,sqrt
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


# In[317]:





# In[318]:


print(sorted(junction.values(), key= lambda d: distance(d.Longitude, d.Latitude,79.899511,6.9424922)))


# In[302]:


junction[0]


# In[77]:


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


# In[102]:


def getFloodStatus(ID):
    floodstatus=random.choice(flood)
    return lvfloodStatus[floodstatus]
getFloodStatus(0)   


# In[103]:


def getDamageStatus(ID):
    damagestatus=random.choice(damage)
    return lvDamageStatus[damagestatus]
getDamageStatus(0)   


# In[80]:


junction


# In[104]:


def calHeuristic(ID):   
    floodStatus=getFloodStatus(ID)
    damageStatus=getDamageStatus(ID)
    
    heuristic=floodStatus+damageStatus
    
    return heuristic/9
        


# In[329]:


def getneighbors(startlocation, n=4):
    return sorted(junction, key=lambda x: distance(junction[startlocation].Longitude,junction[startlocation].Latitude, junction[x].Longitude,junction[x].Latitude))[1:n+1]


# In[360]:


def getParent(closedlist, index):
    path = []
    while index is not None:
        path.append(index)
        print(path)
        index = closedlist.get(index, None)
        print(index)
    return [junction[i] for i in path[::-1]]


# In[361]:


def evacuationRoute(junction,source,destination):
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
        print(currentLocation[1].ID)
        if currentLocation[1].ID in closedlist:
            continue
            
        print(currentLocation[1].ID)
        closedlist[currentLocation[1].ID] = currentLocation[1].parentID
        print(closedlist)
        print("***************")
        if currentLocation[1].ID == destination.ID:
            print("Complete")
            print(closedlist)
            for p in getParent(closedlist, currentLocation[1].ID):
                print(p)
            break
            
        for other in getneighbors(currentLocation[1].ID):
            g = currentLocation[1].G+distance(currentLocation[1].Longitude,currentLocation[1].Latitude, junction[other].Longitude, junction[other].Latitude)
            h = distance(junction[other].Longitude, junction[other].Latitude, destination.Longitude, destination.Latitude)
            f = (g + h) * calHeuristic(currentLocation[1].ID)
            heapq.heappush(openlist, (f, Node(junction[other].ID, f, g, h, currentLocation[1].ID,junction[other].Longitude,junction[other].Latitude)))
        i=i+1


# In[374]:


evacuationRoute(junction,33,45)

