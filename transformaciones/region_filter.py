import pandas as pd

# Leer el fichero CSV como un dataframe de pandas
df = pd.read_csv('city_temperature.csv', encoding='utf-8')

# Filtrar las regiones para sin los valores de África
# porque nunca se han celebrado los juegos olimpicos en África
df = df[df['Region'] != 'Africa']

# Como hay muchos datos de Estados Unidos, y solo se han celebrado los juegos olímpicos en 6 ciudades americanas,
# se han filtrado dichas ciudades del dataset y borrar el resto de valores.
# Las ciudades en los que se han celebrado son los siguientes: Atlanta, Los Angeles, Lake Placid (New York City), 
# Salt Lake City, St Louis y Squaw Valley (Reno)

us_cities_to_keep = ['Atlanta', 'Los Angeles', 'New York City', 'Salt Lake City', 'St Louis', 'Reno']
df = df[~((df['Country'] == 'US') & (~df['City'].isin(us_cities_to_keep)))]

# En sudamérica solo se han celebrado los juegos olímpicos en Rio de Jainero.
# Por tanto, eliminamos el resto de filas
df = df[~((df['Region'] == 'South/Central America & Carribean') & (df['City'] != 'Rio de Janeiro'))]

# Borramos la columna 'State' porque solo se usa para ciudades de EEUU
df.drop('State', axis=1, inplace=True)

# Escribit el nuevo dataset filtrado
df.to_csv('filtered_file.csv', index=False, encoding='utf-8')
