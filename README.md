Proyecto base en Fast API y Python.

## Condiciones:

- Python 3

## Clonar proyecto

```
git clone https://git.fiscalia.gob.bo/desarrollo/skyperson
```

## Run local
### Install dependencies

```
pip install -r requirements.txt
```

### Run server

```
uvicorn app.main:app --reload
```

### Run test

```
pytest app/test.py
```

## Run with docker

### Run server

```
docker-compose up -d --build
```

### Run test

```
docker-compose exec skyperson pytest test/test.py
```

## API documentation (provided by Swagger UI)

```
http://127.0.0.1:8002/docs
```

