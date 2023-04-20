from pymongo import MongoClient
from querys import get_avg_temperature
import os
from dotenv import load_dotenv

load_dotenv()

# Read the Mongo connection string from the environment variables and create the client
client = MongoClient(os.environ['MONGO_CLIENT'])

print('---------')
result = get_avg_temperature(client, 'Madrid','23/03/1999','20/07/1999')
print(result['AvgTemperature'])
print('---------')