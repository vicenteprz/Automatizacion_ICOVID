import pymongo
from pymongo import MongoClient
import pandas as pd
import json
import datetime
from datetime import date, time, datetime
from matplotlib import pyplot as plt

def insert_totalesNacionales():
    #conexion a la base de datos 
    totalesNacionales="https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv"
    cluster=MongoClient("mongodb://127.0.0.1:27017/") # se conecta con mongo
    db=cluster["icovid"] #entra en la base de datos
    collection=db["totalesNacionales"] # entra en la coleccion
    collection.drop() #codigo para eliminar la coleccion en caso de que exista una , asi no se repiten los elementos
    df = pd.read_csv(totalesNacionales) #lee el csv
    df = df.set_index("Fecha") # define el indice como Fecha
    df = df.sort_index()
    data={}#se inicia el diccionario donde irán los datos
    count=0#se inicia un contador
    for e in df.head():#se recorren las cabezas osea las fechas de df
        data={} # se inicia un arreglo en el diccionario donde estará conformada por e= la fecha de la pasada del for
        var={}#se inicia la variable donde iran los datos
        var={"Fecha":e,
            "Casos inactivos confirmados":(df.iloc[:,count][0]), #se van agregando los datos correspondientes de la columna en la que esté la pasada del for
            "Casos activos":(df.iloc[:,count][1]), 
            "Casos activos confirmados":(df.iloc[:,count][2]),
            "Casos activos por FD":(df.iloc[:,count][3]),
            "Casos activos por FIS":(df.iloc[:,count][4]),
            "Casos activos probables":(df.iloc[:,count][5]),
            "Confirmados recuperados":(df.iloc[:,count][6]),
            "Casos nuevos con sintomas":(df.iloc[:,count][7]),
            "Casos nuevos sin notificar":(df.iloc[:,count][8]),
            "Casos nuevos sin sintomas":(df.iloc[:,count][9]),
            "Casos nuevos totales":(df.iloc[:,count][10]),
            "Casos probables acumulados":(df.iloc[:,count][11]),
            "Casos recuperados":(df.iloc[:,count][12]),
            "Casos recuperados por FD":(df.iloc[:,count][13]),
            "Casos recuperados por FIS":(df.iloc[:,count][14]),
            "Casos totales":(df.iloc[:,count][15]),
            "Fallecidos":(df.iloc[:,count])[16]}
            
        data.update(var)#a la variable data se le ingresa todo el diccionario generado
    
        collection.insert_one(data)    # esta funcion de pymongo va a insertar toda la coleccion por pasada 
        count+=1 #el contado aumenta en 1
        data={} # se reinicia la variable data 
def getFECHA_CASOS():
    cluster=MongoClient("mongodb://127.0.0.1:27017/") # se conecta con mongo
    db=cluster["icovid"] #entra en la base de datos
    collection=db["totalesNacionales"]
    arrayDatos=[]
    arrayFechas=[]
    arrayNumeros=[]
    for i in collection.find({},{"_id":0,"Fecha":1,"Casos activos":1}):
        splitter= str(i)
        splited= splitter.split("'")
        fecha=splited[3]
        valor1=splited[6].split("}")
        valor2=valor1[0].split(":")  
        valor3=valor2[1].split(" ")
        if valor3[1] =='nan':
            valor3[1]=0   
        ValorFinal=int(float(valor3[1]))
        arrayFechas.append(fecha)
        arrayNumeros.append(ValorFinal)
    arrayDatos.append(arrayFechas)
    arrayDatos.append(arrayNumeros)
    return arrayDatos
def getGRAPH():
    fechas=getFECHA_CASOS()[0]
    numeros=getFECHA_CASOS()[1]
    plot1=plt.figure(1) # para mostrar el grafico de rojo en pantalla
    plt.title('Casos Activos chile')
    plt.plot(fechas,numeros)
    plt.show()
  


        
            
