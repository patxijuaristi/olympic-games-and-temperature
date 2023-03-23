import pandas as pd

# Read in the CSV file as a pandas dataframe
df = pd.read_csv('fechas_olimpiadas.csv', encoding='utf-8')

# Convert the date columns to datetime format with the specified format string
'''df['Opening ceremony'] = pd.to_datetime(df['Opening ceremony'], format='%d %B %Y').dt.strftime('%d/%m/%Y')
df['Closing ceremony'] = pd.to_datetime(df['Closing ceremony'], format='%d %B %Y').dt.strftime('%d/%m/%Y')'''

for col in ['Opening ceremony', 'Closing ceremony']:
    try:
        df[col] = pd.to_datetime(df[col], format='%d %B %Y').dt.strftime('%d/%m/%Y')
    except ValueError:
        df[col] = df[col]

# Write the modified dataframe to a new CSV file
df.to_csv('modified_olympic_ceremonies.csv', index=False, encoding='utf-8')
