from flask import Flask, render_template, request, jsonify
import requests
import os
from geocoding import get_lat_long
from models import Place
from set_api_key import read_api_key
from googleplaces import GooglePlaces, types, lang
# import http.client
# import json
# conn = http.client.HTTPSConnection("api.iq.inrix.com")
import json
from accessToken import accessToken,find_route,get_route

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    start = request.form.get('start_point')
    end = request.form.get('end_point')
    print(start,end)
    return render_template("home.html")

@app.route('/json_string', methods=["GET","POST"])
def json_demo():
    d = {
        "data":"this is some data",
        "start Point" : "-122345678",
        "end Point" :"+0987654"
    }
    return d

# @app.route('/search_places', methods=["GET", "POST"])
# def search_places(location=None, radius=5000):
#     # pincode = input("Enter pin code : ")
#     api_key = read_api_key(3141)
#     query = request.args.get('query')
#     url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"

#     params = {
#         "query": query,
#         "key": api_key
#     }

#     if location:
#         params["location"] = location
#         params["radius"] = radius

#     response = requests.get(url, params=params)
#     print(response)
#     if response.status_code == 200:
#         places = response.json().get('results', [])
#         print(places)
#         simplified_results = [{'name': place['name'], 'place_id': place['place_id']} for place in places]
#         return jsonify(simplified_results)
#     else:
#         return jsonify([])

@app.route('/search_places')
def search_places():
    query = request.args.get('query')
    api_key = read_api_key(3141)
    google_places = GooglePlaces(api_key)
    # Search for places
    try:
        # Search for places
        query_result = google_places.text_search(query=query)

        results = []
        for place in query_result.places:
            # Getting details of each place
            place.get_details()
            results.append({
                "name": place.name,
                "formatted_address": place.formatted_address,
                "place_id": place.place_id
            })

        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/select_place', methods=['POST'])
def select_place():
    data = request.json
    place_name = data.get('place_name')
    lat, long = get_lat_long(place_name)
    print(f'{place_name} : {lat}, {long}')
    
@app.route('/place-names', methods=['POST', 'GET'])
def get_place_names():
    data = request.get_json()
    try:
        start_place, end_place = data['start_place'], data['end_place']
        print(start_place, end_place)
        response_data = {'message': 'Route found successfully'}
        
        start_lat, start_long = get_lat_long(start_place)
        end_lat, end_long = get_lat_long(end_place)
        
        start_place = Place(name=start_place, latitude=start_lat, longitude=start_long)
        end_place = Place(name=end_place, latitude=end_lat, longitude=end_long)
        coord_data = {
            'start_lat' : start_lat,
            'end_lat' : end_lat,
            'start_long' : start_long,
            'end_long' : end_long
        }
        print(coord_data)

        d = accessToken()
        print(d)
        #breakpoint()
        headers = {'Authorization' : 'Bearer '}
        headers['Authorization'] = headers['Authorization'] + d
        #print(headers)
        print(coord_data)
        wp_1 = [start_lat, start_long]
        wp_2 = [end_lat, end_long]
        # {'start_lat': 37.354611, 'end_lat': 37.3496835, 'start_long': -121.918866, 'end_long': -121.9451335}
        # wp_1 = [37.354611,-121.918866]
        # wp_2 = [37.349683,-121.945133]
        useTraffic = "true"
        routeOutputFields = "D%2CS%2CW%2CB%2CI%2CU%2CP"
        seperator = "%2C"

        req = f"/findRoute?wp_1={wp_1[0]}{seperator}{wp_1[1]}&wp_2={wp_2[0]}{seperator}{wp_2[1]}&maxAlternates=1&useTraffic={useTraffic}&routeOutputFields={routeOutputFields}&format=json"
        #breakpoint()
        find_routes = find_route(headers,req)
        print(find_routes)
        # find_routes_dict = json.loads(find_routes)
        
        route_id = find_routes['result']['trip']['tripId']
        print("Trip ID:", route_id)

        req = f"/route?routeId={route_id}&useTraffic={useTraffic}&routeType=0&routeOutputFields={routeOutputFields}&format=json"
        get_routes_result = get_route(headers,req)
        json_obj = json.dumps(get_routes_result)


        #find_routes(start_place, end_place)
        return json_obj, 200

    except Exception as e:
        # Handle exceptions appropriately
        error_message = str(e)
        print("Error:", error_message)
        #breakpoint()
        return jsonify({'error': error_message}), 500
    


# def find_routes(coord_data):
    
    
# @app.route('/find-routes', methods=['GET', 'POST'])
# def find_routes(start_place : Place, end_place : Place):
#     start_
#     data = {'start_coord' : {start_place.latitude, start_place.longitude},
#             'end_coord' : {end_place.latitude, end_place.longitude}
#             }
#     return jsonify(data), 200

if __name__ == '__main__':
    app.run(debug=True, port=4000)