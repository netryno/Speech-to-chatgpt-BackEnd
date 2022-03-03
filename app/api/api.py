import json
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

def point_polygon(latitud,longitud,stringJson):
    bordes = abstraer(stringJson)
    point = Point(latitud, longitud)
    polygon = Polygon(bordes)
    resultado = polygon.contains(point)
    return resultado


def abstraer(stringJson):
    x = json.loads(stringJson)
    #obtenemos lo que nos interesa
    #T ODO validar / u obtener de diferentes formatos
    poligono = x[0]['geometry']['coordinates'][0]
    polygon_saneado = []
    for val in poligono:                #iteramos array
        pol = val[::-1]                 #revertimos
        t = tuple(e for e in pol)       #convertimos a tuplas
        polygon_saneado.append(t)       #agregamos al array

    return polygon_saneado