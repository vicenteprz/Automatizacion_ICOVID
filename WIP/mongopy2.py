import pymongo
from pymongo import MongoClient
import pandas as pd
import json
import datetime
from datetime import date, time, datetime
from matplotlib import pyplot as plt

def insert_totalesNacionales():
    URL="https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv"
    cluster=MongoClient("mongodb://127.0.0.1:27017/") # se conecta con mongo
    db=cluster["test"] #entra en la base de datos
    collection=db["totalesNacionales5"] # entra en la coleccion
    collection.drop() #codigo para eliminar la coleccion en caso de que exista una , asi no se repiten los elementos
    df = pd.read_csv(URL) #lee el csv
    df = df.set_index("Fecha") # define el indice como Fecha
    df = df.sort_index()
    data={}#se inicia el diccionario donde irán los datos
    count=0#se inicia un contador
    for e in df.head():#se recorren las cabezas osea las fechas de df
        data={} 
        var={"Fecha":e}   
        var.update(df.iloc[:,count]) 
        data.update(var)
        collection.insert_one(data) 
        count+=1
        data={}
def insert_casosComuna():
    URL="https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto1/Covid-19.csv"
    cluster=MongoClient("mongodb://127.0.0.1:27017/") # se conecta con mongo
    db=cluster["test"] #entra en la base de datos
    collection=db["casosComuna"] # entra en la coleccion
    collection.drop() #codigo para eliminar la coleccion en caso de que exista una , asi no se repiten los elementos
    df = pd.read_csv(URL) #lee el csv
    columns=df.head(0)
    
    data={}#se inicia el diccionario donde irán los datos
    count=0#se inicia un contador
    #print(df.keys()[0])
    #print(df.values[0])
    for i in range(len(df.values)):
        dData={}
        var={}
        
        for e in range(len(df.values[i])):
            
            dData[df.keys()[e]]= df.values[i][e]
            
        #print(dData)
        #print("NEXT----NEXT----NEXT----NEXT----NEXT----NEXT----NEXT----NEXT----")
        
        #var.update(dData)
        collection.insert_one(dData)
        dData={}
        
        
            
            
           
            
            
               
                
                
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
#nsert_totalesNacionales()
insert_casosComuna() 


        
            
