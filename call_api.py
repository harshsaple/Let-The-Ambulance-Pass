from accessToken import accessToken,find_route,get_route
from flask import jsonify
d = accessToken()
#print(d)
headers = {'Authorization' : 'Bearer '}
headers['Authorization'] = headers['Authorization'] + d
#print(headers)
wp_1 = [37.770581,-122.442550]
wp_2 = [37.765297,-122.442527]

useTraffic = "true"
routeOutputFields = "D%2CS%2CW%2CB%2CI%2CU%2CP"
seperator = "%2C"

req = f"/findRoute?wp_1={wp_1[0]}{seperator}{wp_1[1]}&wp_2={wp_2[0]}{seperator}{wp_2[1]}&maxAlternates=1&useTraffic={useTraffic}&routeOutputFields={routeOutputFields}&format=json"
find_routes = find_route(headers,req)

route_id = find_routes['result']['trip']['tripId']
print("Trip ID:", route_id)

req = f"/route?routeId={route_id}&useTraffic={useTraffic}&routeType=0&routeOutputFields={routeOutputFields}&format=json"
get_routes_result = get_route(headers,req)
print(get_routes_result)

