import os
import pandas as pd
import psycopg2
from fastapi import FastAPI
from dotenv import load_dotenv
from fuzzywuzzy import fuzz



load_dotenv()

app = FastAPI()


DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')


connect = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)

cursor = connect.cursor()


def fuzz_ratio(full_address_lower, input_text):
    return fuzz.ratio(full_address_lower, input_text)


@app.get('/')
def read_root():
    return {'spbhack': 'Сервис по устранению и изменению некорректных адресов из городских баз данных'}


@app.post('/predict')
def addrese_predict(addrese: str):

    # cursor.execute("""INSERT INTO train_building( 
    #                     full_address) 
    #                     VALUES (%s);""", addrese)
    # connect.commit()

    cursor.execute("""SELECT *
                    FROM train_building;""")
    rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns=[_.name for _ in cursor.description])
    df['fuzz_ratio'] = df['full_address'].apply(lambda x: fuzz_ratio(x.lower(), addrese.lower()))
    df_new = df.sort_values(by='fuzz_ratio', ascending=False)[:10]

    return df_new.to_dict()