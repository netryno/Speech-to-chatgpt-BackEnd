from array import array
from fastapi import FastAPI, HTTPException
from datetime import datetime
#from starlette.responses import Response
from typing import Optional
from pydantic import BaseModel
from app.api import api

class Item(BaseModel):
    point: str='-19.891017337524648, -65.088969087838'
    polygon: Optional['str'] ='[[-65.249813,-21.482379],[-65.2118,-21.29097],[-65.222802,-21.253301]]'



app = FastAPI(
    title='SkyGIS',
    description='Microservicio para trabajar confirmación geografica',
    version="0.0.1",   
)


@app.get("/")
def root():
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

@app.post("/boolean-point-in-polygon")
async def point_polygon(item: Item):
    return api.point_polygon(item)
