import json
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import reverse_geocode




def point_polygon(latitud,longitud,stringJson):
    bordes = abstraer(stringJson)       #saneamos desde la BD de MP
    point = Point(latitud, longitud)    #Covertimos en un punto las coordenadas del punto
    polygon = Polygon(bordes)           #Convertimos en poligono
    resultado = polygon.contains(point)  #libreria que verifica si un punto pertenece a una area
    return resultado
    #retorna falso verdadero

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

def buscar(latitud,longitud):
    coordinates =[(latitud, longitud)]      #armamos tupla
    result = reverse_geocode.search(coordinates) #aplicamos a libreria
    return result
    '''
    {
        "country_code": "BO",
        "city": "Betanzos",
        "country": "Bolivia"
    }
    '''
