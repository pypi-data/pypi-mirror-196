import requests
import polyline
import json
import urllib.parse

class CoolmapRoutePath():
    
    def __init__(self, from_lat_log,to_lat_log, mapbox_api_key ):
        self.from_lat_log = from_lat_log
        self.to_lat_log = to_lat_log
        self.mapbox_api_key = mapbox_api_key
        #defining as private instance variable
        self.__response = self.__get_response
    
    #defineing a private method
    @property
    def __get_response(self):
        headers = {'Content-Type': 'application/json', 'Authorization': ''}
        url = "https://api.mapbox.com/valhalla/v1/route/?"
        from_lat_log = self.from_lat_log.split(",")
        to_lat_log = self.to_lat_log.split(",")
        from_lat = from_lat_log[0]
        from_lon = from_lat_log[1]
        to_lat = to_lat_log[0]
        to_lon = to_lat_log[1]
        param = {"locations":[{"lat": float(from_lat),"lon": float(from_lon)},{"lat": to_lat,"lon": to_lon,}],"costing": "truck","costing_options": {"truck": {"height": 3.66,"width": "2.6","length": "21.64","axle_load": "18.07","hazmat": False}}}
        request_params = {'json': json.dumps(param), 'access_token': self.mapbox_api_key}
        request_url = url + urllib.parse.urlencode(request_params)
        return requests.get(request_url, headers=headers).json() 

    
    def estimated_time(self, required_unit="M"):
        required_unit =  required_unit.upper()
        unit = {"M":[0.0166667, "Minutes"], "H":[0.000277778,"Hours"], "S":[1,"Seconds"]}
        return f"{str(round((self.__response['trip']['summary']['time'] * unit.get(required_unit)[0]), 2))} {unit.get(required_unit)[1]}"


    def estimated_distance(self, required_unit="M"):
        required_unit = required_unit.upper()
        unit = {"M":[0.621371, "Miles"], "K":[1,"Kilometer"], "T":[1000, "Meter"]}
        return f"{str(round(self.__response['trip']['summary']['length'] * unit.get(required_unit)[0], 2))} {unit.get(required_unit)[1]}"
    
    
    def get_path(self):
        return ";".join([f'{l[0] * 0.1},{l[1] * 0.1}' for l in polyline.decode(self.__response['trip']['legs'][0]["shape"])])
    