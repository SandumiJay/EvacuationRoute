from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from flask_cors import CORS,cross_origin
import collections
import json
#import external methods
from route import evacuationRoute
from route import getNearestLocation
import tensorflow as tf
from flask import Flask, request, jsonify
import pickle
import numpy as np
import requests


app = Flask(__name__)
CORS(app)
app.config['MONGO_DBNAME'] = 'dhara'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/dhara'

mongo = PyMongo(app)
#default metods
with open('C:\\SLIIT\\Research\\Implementation\\PythonModel\\junction_network.json') as json_file:
    data =json.load(json_file)

Location = collections.namedtuple("Location", "ID Longitude Latitude".split())
junction={}
for i in range(len(data['features'])):
    id,lon,lat=int(data['features'][i]['attributes']['FID']),data['features'][i]['geometry']['x'],data['features'][i]['geometry']['y']
    junction[i]=Location(id,lon,lat)
	

#get junction coordination
@app.route('/get-junction/', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getjunction():
	data = request.get_json()
	output = getjunction(data['ID'])
	return jsonify(output)
	
#damaged places add end point
@app.route('/get-nearest-location/', methods=['POST'])
@cross_origin(origin='*')
def nearestLocation():
  print("Request")
  data = request.get_json()
  print(data)
  output = getNearestLocation(data['start_Longitude'],data['start_Latitude'])
  return jsonify(output)
	
#safe rote find end point
@app.route('/safe-route/', methods=['POST'])
@cross_origin(origin='*')
def simpleGet():
    data = request.get_json()
    output = evacuationRoute(junction,data['src'],data['dst'])
    return jsonify(output)

#damaged places add end point
@app.route('/add-damaged-place/', methods=['GET'])
@cross_origin(origin='*')
def getAdminRecords():
  records = mongo.db.damaged_places
  output = []
  for s in records.find():
    output.append({'status':s['status'],'Latitude':s['Latitude'],'Longitude' : s['Longitude']})
  return jsonify(output)

#damaged places find end point
@app.route('/damaged-place/', methods=['POST'])
@cross_origin(origin='*')
def addArimaModelPost():
    if request.method=='POST':  
        data = request.get_json()
        print(data)
        mongo.db.damaged_places.insert_one(data)
        return jsonify({'ok': True, 'message': 'damaged-place saved successfully!'})
    else:
        return jsonify({'error': True, 'message': 'error'})
		

# Load the model
model = pickle.load(open('fakemodelLSTM2.pkl','rb'))
graph = tf.get_default_graph()

@app.route('/api',methods=['GET','POST'])
def predict():
    global graph
    with graph.as_default():
        # Get the data from the POST request.
        #data = {'id': 0.8}#request.get_json(force=True)
        r = requests.get('https://environment.data.gov.uk/flood-monitoring/id/stations/1491TH/readings?_sorted&_limit=10')
        dataj=r.json()
        levels = [item['value'] for item in dataj['items']]
        data={"value":levels[0]}
        arr=np.array( tuple(data.values()))
        darray=arr.reshape((1, len(arr), 1))

        # Make prediction using model loaded from disk as per the data.
        prediction = model.predict(darray)

        # Take the first value of prediction
        output =prediction.reshape(4,1)
        mydict=[{"hour1":round(output.item(0)),"hour2":round(output.item(1)),"hour3":round(output.item(2)),"hour4":round(output.item(3))}]
        

    return jsonify(mydict)
    #return data

if __name__ == '__main__':
    #pp.debug=True
    app.run(port=5000, debug=False)