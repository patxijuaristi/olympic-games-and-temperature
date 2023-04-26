import sys
sys.path.append('.')
import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime

from querys.querys import get_avg_temperature

load_dotenv()

# Leer la información de conexión con Mongo de las variables de entorno y crear el cliente
client = MongoClient(os.environ['MONGO_CLIENT'])

# Leer el archivo CSV
df = pd.read_csv('data/fechas_olimpiadas_test.csv')

# Convertir las fechas a objetos de tipo datetime
df['Opening ceremony'] = pd.to_datetime(df['Opening ceremony'], dayfirst=True, errors='coerce')
df['Closing ceremony'] = pd.to_datetime(df['Closing ceremony'], dayfirst=True, errors='coerce')

# Eliminar filas sin fecha en ambas columnas
df.dropna(subset=['Opening ceremony', 'Closing ceremony'], how='all', inplace=True)

# Eliminar filas de juegos olímpicos futuros
current_date = datetime.now().date()
df = df[df['Opening ceremony'].dt.date <= current_date]

# Convertir las fechas a strings especificando el formato
df['Opening ceremony'] = df['Opening ceremony'].dt.strftime('%d/%m/%Y')
df['Closing ceremony'] = df['Closing ceremony'].dt.strftime('%d/%m/%Y')

# Añadir una nueva columna con latemporada de los juegos olímpicos (summer or winter)
df['Season'] = df.apply(lambda row: 'Summer' if pd.to_datetime(row['Opening ceremony'], format='%d/%m/%Y').month > 4 else 'Winter', axis=1)


# Inicializar lista para almacenar las temperaturas medias
avg_temps = []
# Iterar sobre las filas en el data frame y llamar a get_avg_temperature para cada fila
for i, row in df.iterrows():
    city = row['City']
    start_date = row['Opening ceremony']
    end_date = row['Closing ceremony']
    avg_temp = get_avg_temperature(client, city, start_date, end_date)
    avg_temps.append(avg_temp)

# Añadir la lista de temperaturas medias como una nueva columna en el data frame
df['Avg temperature'] = avg_temps

# Guardar el DataFrame en un nuevo archivo CSV que será luego importando a MongoDB como una colección nueva
df.to_csv('data/fechas_olimpiadas_limpias_test.csv', index=False)
