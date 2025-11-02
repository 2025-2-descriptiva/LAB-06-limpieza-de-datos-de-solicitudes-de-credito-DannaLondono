"""
Código para limpiar el archivo de solicitudes de crédito.
Se eliminan duplicados, se convierten tipos de datos y se normalizan columnas de texto.
"""


import pandas as pd
import os

# Mostrar todas las filas y columnas al imprimir DataFrames
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Cargar archivo de solicitudes de crédito
archivo_entrada = r'files/input/solicitudes_de_credito.csv'
solicitudes = pd.read_csv(archivo_entrada, sep=';', index_col=0)


def pregunta_01():
    """
    Limpia el archivo de solicitudes de crédito:
    - Normaliza texto en columnas de categoría y string
    - Convierte montos a enteros
    - Convierte fechas a formato datetime
    - Elimina duplicados y filas vacías

    El archivo limpio se guarda en 'files/output/solicitudes_de_credito.csv'.
    """

    # Crear copia de trabajo para no modificar el DataFrame original
    datos_limpios = solicitudes.copy()

    # Normalizar columna 'sexo'
    datos_limpios['sexo'] = datos_limpios['sexo'].astype('category')
    datos_limpios['sexo'] = datos_limpios['sexo'].str.lower()

    # Convertir columna 'fecha_de_beneficio' a datetime
    datos_limpios['fecha_de_beneficio'] = pd.to_datetime(
        datos_limpios['fecha_de_beneficio'], format="%d/%m/%Y", errors="coerce"
    ).combine_first(
        pd.to_datetime(datos_limpios['fecha_de_beneficio'], format="%Y/%m/%d", errors="coerce")
    )

    # Limpiar columna 'monto_del_credito' y convertir a entero
    datos_limpios['monto_del_credito'] = (
        datos_limpios['monto_del_credito']
        .str.strip()
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace(".00", "", regex=False)
    )
    datos_limpios['monto_del_credito'] = datos_limpios['monto_del_credito'].astype(int)

    # Normalizar texto en columnas relevantes
    datos_limpios['barrio'] = datos_limpios['barrio'].str.lower().str.replace("_", " ").str.replace("-", " ")
    datos_limpios['idea_negocio'] = datos_limpios['idea_negocio'].str.lower().str.replace("_", " ").str.replace("-", " ").str.strip()
    datos_limpios['línea_credito'] = datos_limpios['línea_credito'].str.lower().str.replace("_", " ").str.replace("-", " ").str.strip()
    datos_limpios['tipo_de_emprendimiento'] = datos_limpios['tipo_de_emprendimiento'].str.lower().str.replace("_", " ").str.replace("-", " ").str.strip()

    # Eliminar registros duplicados y filas con datos faltantes
    datos_limpios = datos_limpios.drop_duplicates()
    datos_limpios = datos_limpios.dropna()

    # Crear carpeta de salida si no existe
    os.makedirs('files/output/', exist_ok=True)

    # Guardar archivo limpio
    archivo_salida = r'files/output/solicitudes_de_credito.csv'
    datos_limpios.to_csv(archivo_salida, sep=';', index=True)

    return datos_limpios


# Ejecutar limpieza
resultado_limpio = pregunta_01()
