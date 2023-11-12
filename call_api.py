from accessToken import accessToken,find_route
from flask import jsonify
d = accessToken()
#print(d)
headers = {'Authorization' : 'Bearer '}
headers['Authorization'] = headers['Authorization'] + d
#print(headers)
wp_1 = [37.770581,-122.442550]
wp_2 = [37.765297,-122.442527]
useTraffic = "true"
req = f"/findRoute?wp_1={wp_1[0]}%2C{wp_1[1]}&wp_2={wp_2[0]}%2C{wp_2[1]}&maxAlternates=1&useTraffic={useTraffic}&routeOutputFields=D%2CS%2CW%2CB%2CI%2CU%2CP&format=json"
e = find_route(headers,req)
print(e)