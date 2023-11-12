# import http.client
# import json
# token = 0
# conn = http.client.HTTPConnection("api.iq.inrix.com")
# payload = ''
# headers = {}
import http.client
import json
conn = http.client.HTTPSConnection("api.iq.inrix.com")
payload = ''
headers = {}
req = ''
def accessToken():
    conn.request("GET", "/auth/v1/appToken?appId=t0cmg5z6u2&hashToken=dDBjbWc1ejZ1MnxXVExmZGU4ZFliN3FzUzlGYmZkazgzWUFnRlRNMTRkRG53azJYVHhp", payload, headers)
    res = conn.getresponse()
    data = res.read()
    token = json.loads(data.decode('utf-8'))['result']['token']
    return token

#Finds the route
def find_route(headers,req):
    conn.request("GET",req,payload,headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode('utf-8'))

#Get Routes from the find Route
def get_route(headers,req):
    conn.request("GET",req,payload,headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode('utf-8'))['result']['trip']['routes'][0]['points']['coordinates']

if __name__ == "__main__":
    accessToken()