
import asyncio
from ipaddress import v4_int_to_packed
from flask import Flask, render_template, request
from openpyxl import load_workbook
import random
from decimal import Decimal
import pandas as pd
import numpy as np
import xlsxwriter
from cProfile import label
from matplotlib.transforms import Bbox
import matplotlib.pyplot as plt
import datetime


async def ejecutar_da(w, n):

    hora_inicio = datetime.datetime.now()
    fecha_inicio = hora_inicio.date()

    print()
    print("-------------------------------------------")
    print("Construcción de la matriz de decisión" )
    candidates = np.array(["A1", "A2", "A3", "A4", "A5", "A6","A7","A8","A9"])
    n=5 #Criterios
    a=9 # Alternativas
    Resultados=[]
    A1t={'C1':[0.048,0.053,0.057,0.062,0.066,0.070,0.075,0.079,0.083],
        'C2':[0.047,0.052,0.057,0.062,0.066,0.071,0.075,0.079,0.083],
        'C3':[0.070,0.066,0.066,0.063,0.070,0.066,0.066,0.066,0.066],
        'C4':[0.087,0.081,0.076,0.058,0.085,0.058,0.047,0.035,0.051],
        'C5':[0.190,0.058,0.022,0.007,0.004,0.003,0.002,0.002,0.000]}
    A1=pd.DataFrame(data=A1t,index=candidates)
    #CP=pd.DataFrame(A1t) # Esta es la primera posición del enjambre
    #V=pd.DataFrame(A1t) # Solo para pruebas
    #PBEST=pd.DataFrame(A1t) #Es la primera mejor posición
    print(A1,"\n")

    print("\n -------------------------------------------")
    print("Controles iniciales" )

    print("-------------------------------------------")
    print("Grado de preferencia para cada alternativa")
    # Los pesos son por cada criterio
    #w=[float(0.200),float(0.200),float(0.200),float(0.200),float(0.200)]
    w=[float(0.400),float(0.200),float(0.030),float(0.070),float(0.300)]
    #w=[float(0.123),float(0.099),float(0.043),float(0.343),float(0.392)]
    print(w,"\n")

    wwi=0.3 # Tener un rango menor ayuda a
    c1=2.5    # Este influye en la pobabilidad hacia
    c2=1.5    # Este influye en la pobabilidad hacia
    dim=n*a #dimensión del enjambre
    T=300     #número de iteraciones para PSO
    rangoMin=0 #este rango de valores
    rangoMax=1  

    print("w(inertia) = ",wwi)
    print("c1 = ",c1)
    print("c2 = ",c2)
    print("No. de iteraciones = ",T,"\n")
    #print("r1 = ")
    print("Función Objetivo: IS(a_{1}^i, a_{2}^i, ...a_{m}^i) = PI_{j=1}^m(a^i / S_{l})^w_{j}")
    print("Rango de valores: (",rangoMin,",",rangoMax,") \n")

    #a)Solución ideal
    St=[]
    print("-------------------------------------------")
    print("Establecer la solución ideal")
    # Mejor solución del conjunto de los datos.
    # 1) promedio de cada criterio

    for j in range(n):
        P1=0
        for i in range(a):
            P1 = float(P1)+float(A1.iat[i,j])
        P1=round((float(P1)/float(a)),3)
        St.append(round((float(P1)),3))
    S = pd.Series(St)
    r1 = pd.Series(St)
    print(S,"\n")

    print("-------------------------------------------")
    print("Determinar el índice de similitud")
    #a) normalizamos (a/S)
    #b) elevar lo normalizado al peso(w)
    #c) Producto sucesivo
    CFt=[]
    SI1=[]
    PST=[]

    ISSFO = pd.DataFrame(columns=['C1','C2','C3','C4','C5'])
    for j in range(a):
        SI1=[]
        ISSFOm1=[]
        for i in range(n):
            dat1= float(A1.iat[j,i])
            dat2 = float(S[i])
            wn2=float(w[i]) 
            dat3 = round((dat1/dat2),3)
            #print("normalizado",dat3)

            #print(dat1,"/",dat2, "=",dat3)
            dat4 = round((abs(dat3)**abs(wn2)),3)
            #print("Elevado",dat4)
            #print("                         ",dat3,"^",wn2,"=",dat4)
            #SI1.append(float(dat4))
            ISSFOm1.append(round((float(dat4)),3))
            #print()
        #print("SI1")
        #print(SI1)
        ISSFOVr1 = pd.DataFrame({'C1':[ISSFOm1[0]],'C2':[ISSFOm1[1]],'C3':[ISSFOm1[2]],'C4':[ISSFOm1[3]],'C5':[ISSFOm1[4]]})
        ISSFO = pd.concat([ISSFO,ISSFOVr1], ignore_index=True)
    #print("ISSFO(1)=")
    #print(ISSFO,"\n")

    for j in range(a):
        Sqq1=float(1)   
        for z in range(n):
            dat5= float(ISSFO.iat[j,z])
            #print("valor",dat5)
            #Sqq1=(float(Sqq1)*float(SI1[z]))
            Sqq1=(Sqq1*dat5)
            #print("              Sqq1",Sqq1)
            #print("              dat5",dat5)
        #print("-----------")
        Sqq1=round(Sqq1,3)
        #print("producto",Sqq1)
        #print()
        CFt.append(float(Sqq1))
        PST.append(float(Sqq1))
    PSS = pd.Series(CFt)
    r2 = pd.Series(CFt)
    #print(r2)
    print("-- Índice de similitud =")
    print(PSS)

    print("\n -------------------------------------------")
    print("Establecer el ranking de las alternativas, en orden descendente.")
    Alt=[]
    PST.sort(reverse=True)
    print("reversa",PST)

    qqtemp=0
    indxx=0
    for i in range(a):
        au=0
        for j in range(a):
            compar1= round((float(PST[i])),3)
            compar2= round((float(PSS[au])),3)
            #print(compar1,"=", compar2)
            if(compar1==compar2):
                if indxx==0:
                    qqtemp=j
                    Alt.append(qqtemp+1)
                else:
                    qqtemp=j
                    if (qqtemp+1) in Alt:
                        aalt=0
                    else:
                        Alt.append(qqtemp+1)               
                indxx=indxx+1
            au=au+1
            #print("Alt",Alt)
    print("   Producto sucesivo=   ", PST)
    print("   Ranking_alternativas=",Alt,"\n")


    # PAra almacenar tiempo de ejecución
    hora_fin = datetime.datetime.now()
    alternativas = Alt[-10:]
   

    print('Datos guardados el archivo:DA.xlsx')
    print()


    # Imprimimos los resultados de tiempo
    print("Algoritmo DA")
    print("Cantidad de Iteraciones:", T)
    print("Hora de inicio:", hora_inicio.time())
    print("Fecha de inicio:", fecha_inicio)
    print("Hora de finalización:", hora_fin.time())
    print("Tiempo de ejecución:",hora_fin-hora_inicio)
    print()

    await asyncio.sleep(0.1)

    datosDa = {
        "mejor_alternativa": alternativas,
        "iteraciones": n,
        "hora_inicio": hora_inicio.time().strftime('%H:%M:%S'),
        "fecha_inicio": fecha_inicio.isoformat(),
        "hora_finalizacion": hora_fin.time().strftime('%H:%M:%S'),
        "tiempo_ejecucion": str(hora_fin - hora_inicio)
    }

    return datosDa