import os
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


@app.get("/")
def read_root():
    return {'spbhack': 'Сервис по устранению и изменению некорректных адресов из городских баз данных'}