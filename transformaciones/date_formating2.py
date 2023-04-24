import pandas as pd

# Leer el archivo CSV
df = pd.read_csv('../data/fechas_olimpiadas.csv')

# Convertir las fechas a objetos de tipo datetime
df['Opening ceremony'] = pd.to_datetime(df['Opening ceremony'], dayfirst=True, errors='coerce')
df['Closing ceremony'] = pd.to_datetime(df['Closing ceremony'], dayfirst=True, errors='coerce')

# Eliminar filas sin fecha en ambas columnas
df.dropna(subset=['Opening ceremony', 'Closing ceremony'], how='all', inplace=True)

# Convertir las fechas a strings con el formato deseado
df['Opening ceremony'] = df['Opening ceremony'].dt.strftime('%d/%m/%Y')
df['Closing ceremony'] = df['Closing ceremony'].dt.strftime('%d/%m/%Y')

# Guardar el DataFrame en un nuevo archivo CSV
df.to_csv('../data/fechas_olimpiadas_limpias.csv', index=False)
