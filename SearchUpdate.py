from bs4 import BeautifulSoup as bs
import requests
from datetime import date, time, datetime
import pymongo
from pymongo import MongoClient
import mongopy
import time

def detectar(url):
    page=requests.get(url)
    soup = bs(page.content,'html.parser')
    
    #horas
    eq = soup.find_all("time-ago")#obtiene las fechas
    while eq == []:
        print ("Buscando actualizacion..  " , eq)
        time.sleep(2)
        eq = soup.find_all("time-ago")
        
    hora_pag= eq[1].text.split(" ")#se guarda en variable la segunda fecha , es segundo para evitar tomar el readme
    hora_pag[0]=cambiarfecha(hora_pag[0]) ###se cambia el nov por la fecha en numero HAY QUE CREAR FUNCION PARA TODAS LAS FECHAS
    hora_pag[1]=hora_pag[1].replace(',','')#se quita la coma del dia
    ano=int(hora_pag[2])#se guardan en variables
    mes=int(hora_pag[0])
    dia=int(hora_pag[1])
    fechaPag=date(ano,mes,dia)#en una variable se guarda em formato datetime
    if fechaPag == getFecha():#se compara retorna true o false
        
        print('fecha de actualizacion de la pagina: '+str(fechaPag))
        print('fecha de actualizacion de la Base de datos: '+str(getFecha()))
        print("-------------------------------------------------------")
        
        return True
    else:
        
        print('fecha de actualizacion de la pagina: '+str(fechaPag))
        print('fecha de actualizacion de la Base de datos: '+str(getFecha()))
        print("-------------------------------------------------------")
        return False
def cambiarfecha(mes): #en esta funcion hay que ir agregando los meses y que retornen su respectivo numero como string para utilizar en la funcion detectar
  if mes=='Oct':
    return '10'
  elif mes=='Nov':
    return '11'
  elif mes=='Dic':
    return '12'
def getFecha():
    cluster=MongoClient("mongodb://127.0.0.1:27017/") # se conecta con mongo
    db=cluster["icovid"] #entra en la base de datos
    collection=db["totalesNacionales"]
    query=""#se inicia variable donde quedará almacenada la consulta
    fechaProcesada="" # variable en la que quedara guardada la fecha al procesarla despues del query
    for t in collection.find({},{"_id":0,"Fecha":1}).sort([('$natural',-1)]).limit(1): #esta funcion permite retornar una consulta , en este caso pide la tabla de abajo hacia arriba , mostrando el primer valor
        query=str(t)
    proceso1=query.split(" ")
    proceso2=proceso1[1].split("'")
    proceso3=proceso2[1].split("-")
    ano=int(proceso3[0])# se guardará en variables los numeros de la fecha como interger
    mes=int(proceso3[1])
    dia=int(proceso3[2])
    fechaBD=date(ano,mes,dia)#se guarda en variable un datetime con la fecha ya formada
    return fechaBD

def automata():
    fechaHoy=date.today()    
    ahora=datetime.now()#horario actual
    horario1=datetime(year=ahora.year ,month=ahora.month,day=ahora.day,hour=9,minute=0,second=0)#el dia a las 9
    horario2=datetime(year=ahora.year ,month=ahora.month,day=ahora.day,hour=13,minute=0,second=0)#el dia a las 13 
    if getFecha()!=fechaHoy:
            print("base de datos no corresponde al dia de hoy")
        
            print("Se está buscando actualizacion en horario de actualizacion")
            while horario1< ahora and ahora<horario2:
                print("buscando actualizacion")
                if detectar("https://github.com/MinCiencia/Datos-COVID19/tree/master/output/producto5") == False:
                    
                        print("HORA DE ACTUALIZAR BASE DE DATOS")
                        mongopy.insert_totalesNacionales()
                        print("se acaba de actualizar base de datos")
                        break
                elif ahora>horario2:
                    print("fuera de horario de actualizacion , actualizando")
                    print("HORA DE ACTUALIZAR BASE DE DATOS")
                    mongopy.insert_totalesNacionales()
                    print("se acaba de actualizar base de datos")
                    break
                    
                        
                else:
                    print("No se encontró actualizacion")
                    time.sleep(120)
            print("no se encuentra en horario de actualizacion")
            
    elif getFecha()==fechaHoy:
        print("base de datos ya está actualizada")
    else :
        print("ocurrío algo extraño")
def ActualizacionManual():            
        print("HORA DE ACTUALIZAR BASE DE DATOS")
        mongopy.insert_totalesNacionales()
        print("se acaba de actualizar base de datos")
        
        
def Main():
    print("Que desea:")
    print("0 = automatizar")
    print("1= actualizacion manual")
    scanner=int(input("escriba su comando= \n"))
    if scanner == 0:
        automata()
    elif scanner == 1:
        ActualizacionManual()
    else:
        print("no eligio como proceder , cancelando ejecucíon")
Main()
    

