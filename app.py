from flask import Flask
import csv
import json
from fetch_data import fetch_data, check_bboxes, check_bboxes_secret
from flask_cors import CORS, cross_origin
from country_bboxes import bbox


app = Flask(__name__)
cors = CORS(app)


csv_path = '/home/gothic459/mysite/flights.csv'


data = []
with open(csv_path, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data.append(row)

def parse(has_fetched):
    if has_fetched:
        print("Successfully fetched data")
        data.clear()
        with open(csv_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
    else:
        print("Failed to fetch data")

@app.route('/api/flights')
@cross_origin()
def index():
    has_fetched = fetch_data()
    parse(has_fetched[0])
    return json.dumps(data), 200, {'Content-Type': 'application/json'}

@app.route('/api/flights/<int:id>')
@cross_origin()
def flight(id):
    try:
        has_fetched = fetch_data()
        parse(has_fetched)
        return json.dumps(data[id], indent=4), 200, {'Content-Type': 'application/json'}
    except:
        return "Error"

@app.route('/api/flights/airspaces')
@cross_origin()
def airspaces():
    has_fetched = fetch_data()
    parse(has_fetched[0])
    airspaces = check_bboxes(data)
    return json.dumps(airspaces, indent=4), 200, {'Content-Type': 'application/json'}

@app.route('/api/flights/airspaces/details')
@cross_origin()
def secret_airspaces():
    has_fetched = fetch_data()
    parse(has_fetched[0])
    airspaces = check_bboxes_secret(data)
    return json.dumps(airspaces, indent=4), 200, {'Content-Type': 'application/json'}


@app.route('/api/flights/bbox')
@cross_origin()
def bboxes():
    return json.dumps(bbox, indent=4), 200, {'Content-Type': 'application/json'}

