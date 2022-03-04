from fastapi import FastAPI
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.api import api

class Item(BaseModel):
    latitud: float = -19.033843983071566
    longitud: float = -65.2579481489859
    json_borde: Optional['str'] ='[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","id":"cochabamba","coordinates":[[[ -65.25818020105362,-19.033169241181586 ],[-65.25822848081589,-19.034094722562475],[-65.25756865739822,-19.034115007028145],[-65.25752305984497,-19.033184454615835],[-65.25818020105362,-19.033169241181586]] ] }}]'


class Punto(BaseModel):
    latitud: float = 25.761095379325667
    longitud: float = -80.19431586662844


app = FastAPI(
    title='SkyGIS',
    description='Microservicio para trabajar confirmación geografica',
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