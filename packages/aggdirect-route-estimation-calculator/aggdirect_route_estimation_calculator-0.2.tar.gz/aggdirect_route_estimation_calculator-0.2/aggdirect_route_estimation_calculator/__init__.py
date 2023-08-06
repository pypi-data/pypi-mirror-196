import polyline

class CoolmapRoutePath:
    
    def __init__(self, response):
        self.__response = response
    
    
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