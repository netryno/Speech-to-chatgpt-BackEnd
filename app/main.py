from fastapi import FastAPI
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.api import api

class Item(BaseModel):
    latitud: float = -19.891017337524648
    longitud: float = -65.088969087838
    json_borde: Optional['str'] ='[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","id":"cochabamba","coordinates":[[[-66.785232,-18.135654],[-66.676444,-18.109284],[-66.785232,-18.135654]] ] }}]'

class Punto(BaseModel):
    latitud: float = -19.891017337524648
    longitud: float = -65.088969087838


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

@app.post("/punto-en-area", status_code=200)
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


@app.post("/punto-en-mundo", status_code=200)
async def buscar(punto: Punto):
    res = {
            "error"   : False,
            "message" : "Ubicación de un punto en el mundo",
            "response": {
                "latitud":punto.latitud,
                "longitud":punto.longitud,
                "ubicacion": api.buscar(punto.latitud,punto.longitud),
                "ubicacion2": api.buscar2(punto.latitud,punto.longitud)
            },
            "status"  : 200
    }
    return res    