"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""


import pandas as pd
import os

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Leer el archivo original
datos_originales = pd.read_csv(r'files/input/solicitudes_de_credito.csv', sep=';', index_col=0)

def pregunta_01():
    """
    Limpia el archivo 'solicitudes_de_credito.csv' y guarda el resultado
    en 'files/output/solicitudes_de_credito.csv'.
    """
    # Crear copia de trabajo
    datos_limpios = datos_originales.copy()

    # Normalizar columna 'sexo'
    datos_limpios['sexo'] = datos_limpios['sexo'].astype('category')
    datos_limpios['sexo'] = datos_limpios['sexo'].str.lower()

    # Convertir fechas a datetime
    datos_limpios['fecha_de_beneficio'] = pd.to_datetime(
        datos_limpios['fecha_de_beneficio'], format="%d/%m/%Y", errors='coerce'
    ).combine_first(
        pd.to_datetime(datos_limpios['fecha_de_beneficio'], format="%Y/%m/%d", errors='coerce')
    )

    # Limpiar columna 'monto_del_credito'
    datos_limpios['monto_del_credito'] = datos_limpios['monto_del_credito']\
        .str.strip().str.replace("$", "", regex=False)\
        .str.replace(",", "", regex=False).str.replace(".00", "", regex=False)
    datos_limpios['monto_del_credito'] = datos_limpios['monto_del_credito'].astype(int)

    # Normalizar texto en otras columnas
    columnas_texto = ['barrio', 'idea_negocio', 'línea_credito', 'tipo_de_emprendimiento']
    for col in columnas_texto:
        datos_limpios[col] = datos_limpios[col].str.lower().str.replace("_", " ", regex=False).str.replace("-", " ", regex=False).str.strip()

    # Eliminar duplicados y filas vacías
    datos_limpios = datos_limpios.drop_duplicates()
    datos_limpios = datos_limpios.dropna()

    # Guardar archivo limpio
    os.makedirs('files/output', exist_ok=True)
    datos_limpios.to_csv(r'files/output/solicitudes_de_credito.csv', sep=';', index=False)

    return datos_limpios

# Ejecutar limpieza
pregunta_01()
