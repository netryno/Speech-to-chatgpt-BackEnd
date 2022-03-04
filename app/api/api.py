import json
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import reverse_geocode

from staticmap import StaticMap, Line, Polygon as poligono
from io import BytesIO
import base64
import os

def point_polygon(latitud,longitud,stringJson):
    bordes = abstraer(stringJson,1)       #saneamos desde la BD de MP
    point = Point(latitud, longitud)    #Covertimos en un punto las coordenadas del punto
    polygon = Polygon(bordes)           #Convertimos en poligono
    resultado = polygon.contains(point)  #libreria que verifica si un punto pertenece a una area
    return resultado
    #retorna falso verdadero

#string stringJson: formato de la BD
#revertir: 1 o 0: invierte o no las coordenadas 
#retorna [( x,y),(xx,yy),...]
#
def abstraer(stringJson,revertir=1):
    x = json.loads(stringJson)
    #obtenemos lo que nos interesa
    #T ODO validar / u obtener de diferentes formatos
    poligono = x[0]['geometry']['coordinates'][0]
    polygon_saneado = []
    for val in poligono:                #iteramos array
        if(revertir==1):
            pol = val[::-1]                 #revertimos
            t = tuple(e for e in pol)       #convertimos a tuplas
        else:
            t = tuple(e for e in val)
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


def plotear(stringJson):
    #saneamos info de la BD
    poli = abstraer(stringJson,0)
    m = StaticMap(500, 400, 10,5) #ancho, alto,  padding x, padding y, url template
    polygon = poligono(poli,'#f47521ab', '#000', 22)
    m.add_polygon(polygon)
    image = m.render()

    #escribimos en la memoria ram
    letter_data = BytesIO()
    image.save(letter_data,'png')
    letter_data.seek(0)
    #convertimos a b64
    data = base64.b64encode(letter_data.read()) 
    return data

    #image.save('tmp/map.png')
    #return 'ok'
    #print(m) 
    #return m  
