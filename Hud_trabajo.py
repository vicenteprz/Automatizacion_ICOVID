#Import
import streamlit as st
import altair as alt
from vega_datasets import data
import pymongo
import datetime
from pymongo import MongoClient

#From
from sklearn import datasets

#Titulo
st.title ("Bases de datos Covid-19 en Chile")
#SubHeader
st.write    ("A continuación se mostraran bases de datos creadas gracias a la información recolectada a través de la pagina del Gobierno de Chile: https://www.minciencia.gob.cl/COVID19")
st.write ("    ")
st.write ("    ")
st.write ("    ")


#Multiselect
location = st.multiselect("Regiones de Chile: ",("Arica y Parinacota","Tarapacá","Antofagaste","Coquimbo","Valparaíso","Metropolitana","O’Higgins","Maule"))

#datasets_name = st.slider.selectbox("Regiones de Chile: ",("Arica y Parinacota","Tarapacá","Antofagaste","Coquimbo","Valparaíso","Metropolitana","O’Higgins","Maule"))



#selectbox

#occupation = st.selectbox("Elige una opción que te interese observar",["Casos de Covid-19","Fallecidos","Exámenes-PCR","", ])


cluster = MongoClient("mongodb://127.0.0.1:27017/")  # se conecta con mongo
db = cluster["icovid"]  # entra en la base de datos
collection = db["totalesNacionales"]  # entra en la coleccion
Jsonmongo = collection.find()

for i in Jsonmongo:
    print(i)

#Grafico

source = data.movies.url

alt.Chart(Jsonmongo).transform_window(
    cumulative_count="count()",
    sort=[{"field": "IMDB_Rating"}],
).mark_area().encode(
    x="IMDB_Rating:Q",
    y="cumulative_count:Q"
)



