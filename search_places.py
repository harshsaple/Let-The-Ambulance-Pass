from flask import Flask, request, jsonify
import requests


@app.route('/search_places')
def search_places(api_key, query, location=None, radius=5000):
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

 

if __name__ == "__main__":

    query = "coffee shops in New York"
    location = "40.7128,-74.0060"  # Optional: Latitude and Longitude
    api_key = os.environ.get('GOOGLE_API_KEY')
    results = search_places(api_key, query, location)

    print(results)