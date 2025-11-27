# core/intervals.py
import pandas as pd
import numpy as np

def crear_intervalos(serie_valores: pd.Series,criterio_intervalos:str):
    '''
    Crea intervalos para datos continuos basados en el criterio seleccionado.
    
    :param serie_valores: Serie de Pandas con los valores numéricos.
    :param criterio_intervalos: Criterio para definir los intervalos
    :return: DataFrame con los intervalos y sus frecuencias.
    '''
    n = len(serie_valores)
    valor_min = serie_valores.min()
    valor_max = serie_valores.max()
    rango = valor_max - valor_min

    if criterio_intervalos == "Regla de Sturges":
        k = int(np.ceil(1 + np.log2(n)))
    elif criterio_intervalos == "Raíz cuadrada":
        k = int(np.ceil(np.sqrt(n)))
    elif criterio_intervalos == "Regla de Scott":
        h = 3.5 * serie_valores.std() / (n ** (1/3))
        k = int(np.ceil(rango / h))
    else:
        try:
            k = int(criterio_intervalos)
            if k <= 0:
                raise ValueError("El número de intervalos debe ser mayor a cero.")
        except ValueError:
            raise ValueError("Criterio de intervalos no reconocido.")
    
    ancho_intervalo = round(rango / k)
    limites_inferiores = [valor_min + i * ancho_intervalo for i in range(k)]
    limites_superiores= [limites_inferiores[i] + ancho_intervalo for i in range(k)]
    marcas_de_clase = [(limites_inferiores[i] + limites_superiores[i]) / 2 for i in range(k)]
    frecuencias, _ = np.histogram(serie_valores, bins=k, range=(valor_min, valor_max))
    tabla_frecuencias = pd.DataFrame({
        'Límite Inferior': limites_inferiores,
        'Límite Superior': limites_superiores,
        'Marca de Clase': marcas_de_clase,
        'Frecuencia Absoluta (fi)': frecuencias
    })
    return tabla_frecuencias


# Ejemplo de uso:
# datos = pd.Series([1.5, 2.3, 2.9, 3.1, 4.0, 5.2, 5.5, 6.3, 7.8, 6.6 ])
# tabla_intervalos = crear_intervalos(datos, 'Regla de Scott')
# print(tabla_intervalos)
