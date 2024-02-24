# Experimento MOORA
# Doctorado en Tecnología
# Universidad Autónoma de ciudad Juárez
# Actualización Feb 2024


import asyncio
import datetime
import math
import random
from decimal import Decimal
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xlsxwriter
from flask import Flask
from openpyxl import load_workbook


async def ejecutar_moorav(w, n):

    hora_inicio = datetime.datetime.now()
    fecha_inicio = hora_inicio.date()
    print()
    print("-------------------------------------------")
    print("Construcción de la matriz de decisión")
    attributes = ["C1", "C2", "C3", "C4", "C5"]
    candidates = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9"]
    n = n
    a = 9
    raw_data = [
        [0.048, 0.047, 0.070, 0.087, 0.190],
        [0.053, 0.052, 0.066, 0.081, 0.058],
        [0.057, 0.057, 0.066, 0.076, 0.022],
        [0.062, 0.062, 0.063, 0.058, 0.007],
        [0.066, 0.066, 0.070, 0.085, 0.004],
        [0.070, 0.071, 0.066, 0.058, 0.003],
        [0.075, 0.075, 0.066, 0.047, 0.002],
        [0.079, 0.079, 0.066, 0.035, 0.002],
        [0.083, 0.083, 0.066, 0.051, 0.000],
    ]

    # Mostrar los datos sin procesar que tenemos
    x = pd.DataFrame(data=raw_data, index=candidates, columns=attributes)
    print(x)

    #############################################################################################
    print("\n-------------------------------------------")
    print("Controles iniciales")
    # Contien las evaluaciones cardinales de cada alternativa respecto a cada criterio
    EV = ["Min", "Min", "Min", "Min", "Min"]
    print("Evaluaciones cardinales de cada alternativa respecto a cada criterio:")
    print(EV,"\n")

    ### -- Pesos por cada criterio
    w = [0.400, 0.200, 0.030, 0.070, 0.300]
    #w = [0.300, 0.200, 0.200, 0.150, 0.150] 
    #w = [0.200, 0.200, 0.200, 0.200, 0.200]
    #w = [0.123, 0.099, 0.043, 0.343, 0.392]
    weights = pd.Series(w, index=attributes)
    print(weights,"\n")

    ### -- Normalizamos con distancia euclidiana
    # Calcular la suma de los cuadrados de cada fila
    squared_sum = (x ** 2).sum(axis=1)
    print("squared_sum",squared_sum)

    # Calcular la raíz cuadrada de la suma de cuadrados
    norm_factor = np.sqrt(squared_sum)
    print("norm_factor",norm_factor)

    # Normalizar dividiendo cada valor por la raíz cuadrada correspondiente
    normalized_data = x.div(norm_factor, axis=0)
    print("\n Matriz de datos normalizados (distancia euclidiana):")
    print(normalized_data)

    ### -- Ponderamos la matriz normalizada por los pesos de los criterios
    weighted_data = normalized_data * weights
    print("\nMatriz de datos ponderados:")
    print(weighted_data)

    ### -- Cálculo de la puntuación de cada alternativa:
    if "Min" in EV:
        global_scores = weighted_data.min(axis=1)  # Evaluación mínima
    else:
        global_scores = weighted_data.max(axis=1)  # Evaluación máxima
        
    print("\nEvaluación de cada alternativa:")
    print(global_scores)

    ### -- Clasificación de alternativas
    ranked_alternatives = global_scores.sort_values(ascending=False)
    print("\nClasificación de alternativas:")
    print(ranked_alternatives)


    #####################################################################################
    ### -- Crear DataFrame para clasificación final
    RankFin = pd.DataFrame(ranked_alternatives, columns=['Puntuación Global'])
    RankFin['Alternativa'] = ranked_alternatives.index
    RankFin.reset_index(drop=True, inplace=True)

    print("\nClasificación Final:")
    print(RankFin)

    print("\nLa mejor solución es la alternativa:", RankFin.iloc[0]['Alternativa'], "con una puntuación global de:", RankFin.iloc[0]['Puntuación Global'])


    #####################################################################################
    # Para almacenar tiempo de ejecución
    hora_fin = datetime.datetime.now()
    ejecut = hora_fin - hora_inicio
    arreglo = ranked_alternatives.index[-10:]
    arregloInvertido = tuple((arreglo))
    alternativas = arregloInvertido

    # Para guardar información en archivo de EXCEl
    dT = {"Método": ["MOORA"],
        "Hora de inicio": [hora_inicio.time()],
        "Fecha de inicio": [fecha_inicio],
        "Hora de finalización": [hora_fin.time()],
        "Tiempo de ejecución": [ejecut]}

    dataT = pd.DataFrame(dT)
    dataAlt = pd.DataFrame(RankFin)
    dataw = pd.DataFrame(w)
    dataND = pd.DataFrame(normalized_data)
    datawd= pd.DataFrame(weighted_data)
    datags= pd.DataFrame(global_scores)


    with pd.ExcelWriter('Experimentos2/MOORA.xlsx', engine='xlsxwriter') as writer:
        dataT.to_excel(writer, sheet_name='Tiempos')
        dataw.to_excel(writer, sheet_name='w')
        x.to_excel(writer, sheet_name='Matriz_decisión')
        dataND.to_excel(writer, sheet_name='Matriz_normaliza')
        datawd.to_excel(writer, sheet_name='Matriz_ponderadss')
        datags.to_excel(writer, sheet_name='Evaluación_cada_alternativa')
        dataAlt.to_excel(writer, sheet_name='Ranking_alternativas')


    print('\n Datos guardados el archivo:MOORA.xlsx')
    print()

    # Imprimimos los resultados de tiempo
    print("Método MOORA")
    print("Hora de inicio:", hora_inicio.time())
    print("Fecha de inicio:", fecha_inicio)
    print("Hora de finalización:", hora_fin.time())
    print("Tiempo de ejecución:", ejecut)
    print()

    await asyncio.sleep(0.1)

    datosMoorav = {
        "mejor_alternativa": alternativas,
        "iteraciones": n,
        "hora_inicio": hora_inicio.time().strftime('%H:%M:%S'),
        "fecha_inicio": fecha_inicio.isoformat(),
        "hora_finalizacion": hora_fin.time().strftime('%H:%M:%S'),
        "tiempo_ejecucion": str(hora_fin - hora_inicio)
    }

    return datosMoorav