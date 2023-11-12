from flask import Flask, render_template, request, jsonify
import requests
import os
from geocoding import get_lat_long
from models import Place
from set_api_key import read_api_key

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

@app.route('/search_places', methods=["GET", "POST"])
def search_places(location=None, radius=5000):
    # pincode = input("Enter pin code : ")
    api_key = read_api_key(3141)
    query = request.args.get('query')
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    params = {
        "query": query,
        "key": api_key
    }

    if location:
        params["location"] = location
        params["radius"] = radius

    response = requests.get(url, params=params)
    if response.status_code == 200:
        places = response.json().get('results', [])
        simplified_results = [{'name': place['name'], 'place_id': place['place_id']} for place in places]
        return jsonify(simplified_results)
    else:
        return jsonify([])

@app.route('/select_place', methods=['POST'])
def select_place():
    data = request.json
    place_name = data.get('place_name')
    lat, long = get_lat_long(place_name)
    print(f'{place_name} : {lat}, {long}')
    
@app.route('/place-names', methods=['POST'])
def get_place_names():
    data = request.get_json()
    try:
        start_place, end_place = data['start_place'], datap['end_place']
        print(start_place, end_place)
        response_data = {'message': 'Route found successfully'}
        
        start_lat, start_long = get_lat_long(start_place)
        end_lat, end_long = get_lat_long(end_place)
        
        start_place = Place(name=start_place, latitiude=start_lat, longitude=start_long)
        end_place = Place(name=end_place, latitude=end_lat, longitude=end_long)
        find_routes(start_place, end_place)
        return jsonify(response_data), 200

    except Exception as e:
        # Handle exceptions appropriately
        error_message = str(e)
        print("Error:", error_message)
        return jsonify({'error': error_message}), 500

@app.route('/find-routes', methods=['GET', 'POST'])
def find_routes(start_place : Place, end_place : Place):
    pass

if __name__ == '__main__':
    app.run(debug=True, port=4000)