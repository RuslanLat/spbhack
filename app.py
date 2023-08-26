import streamlit as st
import requests
import json
import pandas as pd
from fuzzywuzzy import fuzz

st.set_page_config(page_title='Комитет по информатизации и связи',
                    page_icon='images/logo.jpg') #layout = "wide"


col1, col2 = st.columns([1,5])
col1.markdown("""<p><img src='data:image/png;base64,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' width='80' height='90' align='middle' /> </p>""", unsafe_allow_html=True)    
col2.markdown("<p style='text-align: center; font-size:20px; color: blac;'><STRONG> Правительство Санкт-Петербурга<br>Комитет по информатизации и связи</STRONG></p>", unsafe_allow_html=True)
col2.markdown("<p style='text-align: center; font-size:20px; color: blac;'> Сервис по устранению и изменению некорректных адресов из городских баз данных  </p>", unsafe_allow_html=True)

input_text = st.text_input('Введите адрес для поиска', 'г.Санкт-Петербург, Петровский проспект, дом 18')

@st.cache_data
def data_upload_predict():
    
    df = pd.read_csv('row_data/building_20230808.csv').set_index('id').drop_duplicates()

    return df

def fuzz_partial_ratio(full_address_lower, input_text):
    return fuzz.partial_ratio(full_address_lower, input_text)

if input_text:
    st.write('Введенный адрес', input_text)

    df = data_upload_predict()
    df['fuzz_partial_ratio'] = df['full_address'].apply(lambda x: fuzz_partial_ratio(x, input_text))
    df = df.sort_values(by='fuzz_partial_ratio', ascending=False)[:10]
    st.subheader('Результаты поиска')
    st.write(df)



st.write("##")
st.markdown("<h6 style='text-align: center; color: blac;'> ©️ Команда Ленинград </h6>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center; color: blac;'> Цифровой прорыв Санкт-Петербург 2023 </h6>", unsafe_allow_html=True)