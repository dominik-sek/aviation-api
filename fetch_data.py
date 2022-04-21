import csv
from opensky_api import OpenSkyApi
from country_bboxes import bbox

api = OpenSkyApi()
def fetch_data():
    try:
        s = api.get_states()
        with open('/home/gothic459/mysite/flights.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['origin_country', 'time_position', 'last_contact', 'longitude', 'latitude', 'geo_altitude', 'on_ground', 'velocity', 'true_track', 'vertical_rate', 'baro_altitude', 'position_source','timestamp'])
            for i in range(len(s.states)):
                writer.writerow([
                    s.states[i].origin_country,
                    s.states[i].time_position,
                    s.states[i].last_contact,
                    s.states[i].longitude,
                    s.states[i].latitude,
                    s.states[i].geo_altitude,
                    s.states[i].on_ground,
                    s.states[i].velocity,
                    s.states[i].true_track,
                    s.states[i].vertical_rate,
                    s.states[i].baro_altitude,
                    s.states[i].position_source,
                    s.time])
        return True, "Success"
    except:
        return False, "Failed to fetch data"

#lat_min, lat_max, lon_min, lon_max
def check_bboxes(flight_data):
    airspaces = {}
    for i in range(len(flight_data)):
        if flight_data[i]['latitude'] != '' and flight_data[i]['longitude'] != '' and flight_data[i]['on_ground'] == 'False':
            lat = float(flight_data[i]['latitude'])
            lon = float(flight_data[i]['longitude'])
            for key, value in bbox.items():
                lat_min = value[1][0]
                lat_max = value[1][1]
                lon_min = value[1][2]
                lon_max = value[1][3]
                if(lat >= lat_min and lat <= lat_max and lon >= lon_min and lon <= lon_max):
                    if value[0] in airspaces:
                        airspaces[value[0]] += 1
                    else:
                        airspaces[value[0]] = 1
    return airspaces

def check_bboxes_secret(flight_data):
    airspaces = []
    for i in range(len(flight_data)):
        if flight_data[i]['latitude'] != '' and flight_data[i]['longitude'] != '' and flight_data[i]['on_ground'] == 'False':
            lat = float(flight_data[i]['latitude'])
            lon = float(flight_data[i]['longitude'])
            for key, value in bbox.items():
                lat_min = value[1][0]
                lat_max = value[1][1]
                lon_min = value[1][2]
                lon_max = value[1][3]
                if(lat >= lat_min and lat <= lat_max and lon >= lon_min and lon <= lon_max):
                    airspaces.append(
                        {
                            "airspace": value[0],
                            "latitude": lat,
                            "longitude": lon
                        })
    return airspaces

