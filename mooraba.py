


async def ejecutar_Mooraba():



    await asyncio.run(0.1)
    datosMooraba = {
                "mejor_alternativa": alternativas,
                "iteraciones": t,
                "hora_inicio": hora_inicio.time().strftime('%H:%M:%S'),
                "fecha_inicio": fecha_inicio.isoformat(),
                "hora_finalizacion": hora_fin.time().strftime('%H:%M:%S'),
                "tiempo_ejecucion": str(hora_fin - hora_inicio)
            }

    return datosMooraba