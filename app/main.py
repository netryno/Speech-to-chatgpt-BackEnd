from fastapi import FastAPI
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.api import api
import array
from typing import List

area_default= '[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","id":"cochabamba","coordinates":[[[ -65.25818020105362,-19.033169241181586 ],[-65.25822848081589,-19.034094722562475],[-65.25756865739822,-19.034115007028145],[-65.25752305984497,-19.033184454615835],[-65.25818020105362,-19.033169241181586]] ] }}]'
area_default2= '[[[-65.2580326795578,-19.046039308364062],[-65.25892317295…04707880924646],[-65.2580326795578,-19.046039308364062]]]'
cordinates =  [[-65.2580326795578,-19.046039308364062],[-65.25892317295074,-19.04696725336608],[-65.25743186473846,-19.048087879484772],[-65.25656819343567,-19.04707880924646],[-65.2580326795578,-19.046039308364062]]

class Item(BaseModel):
    latitud: float = -19.033843983071566
    longitud: float = -65.2579481489859
    json_borde: Optional['str'] =area_default


class Punto(BaseModel):
    latitud: float = 25.761095379325667
    longitud: float = -80.19431586662844

class Area(BaseModel):
    json_borde: Optional['str'] =area_default

class Point(BaseModel):
     point: List[25.761095379325667,-80.19431586662844]


class Item2(BaseModel):
    latitud: float = -19.033843983071566
    longitud: float = -65.2579481489859
    json_borde: List[Point] = cordinates


app = FastAPI(
    title='SkyGIS - Ministerio Público',
    description='Microservicio para trabajar con confirmación geografica',
    version="0.0.1",   
)

@app.get("/")
def home():
    home = {
            "error"   : False,
            "message" : "ok",
            "response": {
                "microservicio":"SkyGis",
                "version"       : "0.0.1",
                "dateTime": (datetime.now()).strftime('%Y-%m-%d %H:%M:%S'),
                "descripcion":"Información geográfica",
                "autor": "Copyright © Ministerio Público",
            },
            "status"  : 200
    }
    return home

@app.post("/punto-en-area", status_code=200,  tags=["Geolocalización"])
async def verificar(item: Item):
    res = {
            "error"   : False,
            "message" : "Punto geográfico pertenece a una área determinada?",
            "response": {
                "latitud":item.latitud,
                "longitud":item.longitud,
                "pertenece": api.point_polygon(item.latitud,item.longitud,item.json_borde)
            },
            "status"  : 200
    }
    return res  

@app.post("/punto-en-area2", status_code=200,  tags=["Geolocalización"])
async def verificar(item2: Item2):
    res = {
            "error"   : False,
            "message" : "Punto geográfico pertenece a una área determinada (coordinates)?",
            "response": {
                "latitud":item2.latitud,
                "longitud":item2.longitud,
                "pertenece": api.point_polygon2(item2.latitud,item2.longitud,item2.json_borde)
            },
            "status"  : 200
    }
    return res    


@app.post("/punto-en-mundo", status_code=200, tags=["Geolocalización"])
async def buscar(punto: Punto):
    res = {
            "error"   : False,
            "message" : "Ubicación de un punto en el mundo",
            "response": {
                "latitud":punto.latitud,
                "longitud":punto.longitud,
                "ubicacion": api.buscar(punto.latitud,punto.longitud),
            },
            "status"  : 200
    }
    return res    


@app.post("/plotear", status_code=200, tags=["Geolocalización"])
async def area(area:Area):
    res = {
            "error"   : False,
            "message" : "Area renderizado en un imagen png",
            "response": {
                "png_base64": api.plotear(area.json_borde),
            },
            "status"  : 200
    }
    return res  