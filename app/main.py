from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import io
import os
from pydantic import BaseModel
from typing import List
import requests
import base64
import speech_recognition as sr
import pyttsx3
import random
import string
import whisper
import time

#envs
token_openai = os.getenv("OPENAI_TOKEN")
openai_temperature = os.getenv("OPENAI_TEMPERATURE",0.7)
openai_max_tokens = os.getenv("OPENAI_MAX_TOKENS",50)
whisper_model = os.getenv("WHISPER_MODEL",'tiny')
front_url_cors = os.getenv("FRONT_URL_CORS",'https://localhost:8084')

app = FastAPI(
    title='SkyChatGPT',
    description='Microservicio bot-chatgpt',
    version="0.0.1",   
)

print(front_url_cors)

#cors
origins = [
    front_url_cors,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AudioFile(BaseModel):
    audio_b64: str

@app.get("/")
async def home():
    home = {
            "error"   : False,
            "message" : "SkyChatGPT",
            "response": {
                "microservicio":"SkyChatGPT",
                "version"       : "0.0.1",
                "dateTime": (datetime.now()).strftime('%Y-%m-%d %H:%M:%S'),
                "descripcion": f'SkyChatGPT: ',
                "autor": "Copyright © Paul Caihuara",
            },
            "status"  : 200
    }
    return home

#Servicio
@app.post("/process_audio/", status_code=200,  tags=["Boot"])
async def convert_audio_to_text(audio: AudioFile):
    texto = audiob64_a_texto(audio.audio_b64)
    print('Pregunta: '+texto)
    respuesta_txt=chatgpt(texto)
    print('Respuesta:  '+respuesta_txt)
    return {
        "prompt": texto,
        "chatgpt_respuesta":respuesta_txt,
        "chatgpt_respuesta_audiob64": texto_a_audio(respuesta_txt)
    }

#Funciones necesarias
def chatgpt(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer "+token_openai
    }

    #models: es-davinci, text-davinci-002
    data = {
        "model": "text-davinci-002",
        "prompt": prompt,
        "temperature": float(openai_temperature),
        "max_tokens": int(openai_max_tokens)
    }  
    response = requests.post("https://api.openai.com/v1/completions", headers=headers, json=data)
    print(response)
    response_text = response.json()["choices"][0]["text"]

    return response_text

def audiob64_a_texto(audiob64):
    path = './tmp/'+ strRandom(15) + '.wav'
    # Crear un objeto de archivo a partir de la cadena de texto Base64
    audio_file = io.BytesIO(base64.b64decode(audiob64))

    with open(path, 'wb') as f:
       f.write(audio_file.getbuffer())

    model = whisper.load_model(whisper_model)

    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(path) ##  "hola.mp3"
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")
    # decode the audio
    #options = whisper.DecodingOptions()
    options = whisper.DecodingOptions(fp16 = False)
    result = whisper.decode(model, mel, options)
    os.remove(path)
    return result.text

def texto_a_audio(texto):
    path = './tmp/'+ strRandom(10) + '.mp3'
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.save_to_file(texto, path)
    engine.runAndWait()
    time.sleep(2)
    with io.open(path, 'rb') as f:
        audio_bytes = f.read()

    base64_audio = base64.b64encode(audio_bytes).decode('utf-8')
    os.remove(path)
    return base64_audio


def strRandom(longitud = 8):
    caracteres = string.ascii_lowercase + string.digits # Caracteres alfanuméricos en minúscula
    resultado = ''.join(random.choice(caracteres) for i in range(longitud)) # Generar string aleatorio
    return resultado