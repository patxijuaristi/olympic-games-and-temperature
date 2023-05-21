from pymongo import MongoClient
import querys
import os
from dotenv import load_dotenv

def find_indexes_used(data):
    if isinstance(data, dict):
        if 'indexesUsed' in data:
            return data['indexesUsed']
        for value in data.values():
            result = find_indexes_used(value)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_indexes_used(item)
            if result is not None:
                return result
    return None

def get_results(result, with_indexes):
    miliseconds = 0
    stages = result['stages']
    for s in stages:
        miliseconds += s['executionTimeMillisEstimate']

    miliseconds += result['operationTime'].as_datetime().second

    execution_stats = stages[0]['$cursor']['executionStats']
    n_returned = execution_stats['nReturned']
    keys_examined = execution_stats['totalKeysExamined']
    docs_examined = execution_stats['totalDocsExamined']

    if with_indexes:
        execution_stages = execution_stats.get('executionStages', {})
        indexes_used = find_indexes_used(execution_stages)
    else:
        indexes_used = None
    
    return {
        'miliseconds': miliseconds,
        'n_returned': n_returned,
        'keys_examined': keys_examined,
        'docs_examined': docs_examined,
        'indexes_used': indexes_used
    }
    

load_dotenv()

# Read the Mongo connection string from the environment variables and create the client
client = MongoClient(os.environ['MONGO_CLIENT'])
collection = client['olympics']['athlete_events']

print('---------')

# 1. Crear índices
collection.create_index([("Team", 1)], background=True)
collection.create_index([("Sport", 1), ("Medal", 1)], background=True)
collection.create_index([("_id.Sport", 1)], background=True)
collection.create_index([("total_medals", -1)], background=True)

print('Índices creados')
print('---------')

# 2. Ejecutar la agregación con índices activados
result_with_indexes = querys.get_best_sport_for_country(client, country='China', explain=True)

# 3. Desactivar los índices
collection.drop_indexes()

# 4. Ejecutar la agregación sin índices
result_without_indexes = querys.get_best_sport_for_country(client, country='China', explain=True)

# 5. Mostrar los resultados
print(get_results(result_with_indexes, True))
print('\n')
print(get_results(result_without_indexes, False))