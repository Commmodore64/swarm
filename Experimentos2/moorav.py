# Experimento MOORA
# Doctorado en Tecnología
# Universidad Autónoma de ciudad Juárez
# Actualización Feb 2024


from flask import Flask
import random
from decimal import Decimal
import pandas as pd
from openpyxl import load_workbook
import xlsxwriter
import matplotlib.pyplot as plt
import math
import datetime
import asyncio


hora_inicio = datetime.datetime.now()
fecha_inicio = hora_inicio.date()

print()
print("-------------------------------------------")
print("Construcción de la matriz de decisión")
attributes = ["C1", "C2", "C3", "C4", "C5"]
candidates = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9"]
n = 5
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
A1 = pd.DataFrame(data=raw_data, index=candidates, columns=attributes)
print(A1)

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
normalized_data = A1.div(A1.sum(axis=0), axis=1)
print("Matriz de datos normalizados:")
print(normalized_data)

### -- Ponderamos la matriz normalizada por los pesos de los criterios
weighted_data = normalized_data * weights
print("\nMatriz de datos ponderados:")
print(weighted_data)

### -- Obtenemos la evaluación de cada alternativa 
global_scores = weighted_data.sum(axis=1) #Puntuación Global
print("\nPuntuación global para cada alternativa:")
print(global_scores)

### -- Clasificación de alternativas
ranked_alternatives = global_scores.sort_values(ascending=False)
print("\nClasificación de alternativas:")
print(ranked_alternatives.iloc[3])

#####################################################################################
### -- Crear DataFrame para clasificación final
RankFin = pd.DataFrame(ranked_alternatives, columns=['Puntuación Global'])
RankFin['Alternativa'] = ranked_alternatives.index
print (ranked_alternatives.index[-5:])
RankFin.reset_index(drop=True, inplace=True)
arreglo = ranked_alternatives.index[-5:]
arregloInvertido = tuple(reversed(arreglo))
print(arregloInvertido)

print("\nClasificación Final:")
print(RankFin)

print("La mejor solución es la alternativa:", RankFin.iloc[0]['Alternativa'], "con una puntuación global de:", RankFin.iloc[0]['Puntuación Global'])


#####################################################################################
# Para almacenar tiempo de ejecución
hora_fin = datetime.datetime.now()
ejecut = hora_fin - hora_inicio
alternativas = RankFin[-5:]

# Para guardar información en archivo de EXCEl
dT = {"Algoritmo": ["TOPSIS"],
    "Hora de inicio": [hora_inicio.time()],
    "Fecha de inicio": [fecha_inicio],
    "Hora de finalización": [hora_fin.time()],
    "Tiempo de ejecución": [ejecut]}

dataT = pd.DataFrame(dT)
dataAlt = pd.DataFrame(RankFin)
dataw = pd.DataFrame(w)

with pd.ExcelWriter('Experimentos/MOORA.xlsx', engine='xlsxwriter') as writer:
    dataT.to_excel(writer, sheet_name='Tiempos')
    dataw.to_excel(writer, sheet_name='w')
    A1.to_excel(writer, sheet_name='Matriz')
    dataAlt.to_excel(writer, sheet_name='Ranking_alternativas')

print('Datos guardados el archivo:MOORA.xlsx')
print()

# Imprimimos los resultados de tiempo
print("Algoritmo MOORA")
print("Hora de inicio:", hora_inicio.time())
print("Fecha de inicio:", fecha_inicio)
print("Hora de finalización:", hora_fin.time())
print("Tiempo de ejecución:", ejecut)

    