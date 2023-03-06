## MICROSERVICE
ChatGPT + OpenAI Whisper (audio a texto) + Pyttsx3 (texto a audio) => Docker-compose

-Servicio recibe un archivo audio en base64, (audio con consulta verbal a chatgpt).
-Convierte el audio en texto usando herramienta: openai-whisper.
-Consume servicio de api.openai.com/v1/completions, pasandole el prompt extraido del audio.
-Convierte el texto (respuesta) de chatgpt en audio (mp3), y retorna como respuesta en base64



## Condiciones:

- Python 3

## Install
## Clonar proyecto

```
git clone https://git.....
```
Copiar docker-compose.example.yml
Configurar los variables de entorno

```
      - OPENAI_TOKEN=YOURTOKEN
      - OPENAI_TEMPERATURE=0.5
      - OPENAI_MAX_TOKENS=100
      - FRONT_URL_CORS=https://localhost:8084
      - WHISPER_MODEL=tiny
```

WHISPER_MODEL : tiny, base, small, medium, large, large-v2
OPENAI_TEMPERATURE: valores de 0.0 a 1.0
OPENAI_MAX_TOKENS: Cantidad de palabras maxima en la respuesta de chatgpt

## Run with docker

### Run server

```
docker-compose up -d --build
```

## API documentation (provided by Swagger UI)

```
http://127.0.0.1:8003/docs
```


## Usage
### Consumir servicio

```
POST {{urlBase}}/process_audio
content-type: application/json

{
  "audio_b64": "SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU5L... stringb64 del audio .wav"
}
```

### Respuesta servicio
```
{
    "prompt": "¿Explica cómo desaparecieron los mayas?",
    "chatgpt_respuesta" : "\n\nLos mayas desaparecieron aproximadamente en el año 1000 d.C. La razón es desconocida, pero hay varias teorías. Algunos...",
    "chatgpt_respuesta_audiob64": "SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjIwLjEwMAAAA... stringb64"
}
```





## Librerias:
fastapi
uvicorn
pydantic
requests
SpeechRecognition
pyttsx3
openai-whisper


### FrontEnd para este servicio



```
git clone https://git.....
```