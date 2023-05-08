from pymongo import MongoClient
from querys import get_avg_temperature, get_best_country_in_sport, get_best_sport_for_country
import os
from dotenv import load_dotenv

load_dotenv()

# Read the Mongo connection string from the environment variables and create the client
client = MongoClient(os.environ['MONGO_CLIENT'])

print('---------')
#result = get_avg_temperature(client, 'Bilbao','07/02/2014','23/02/2014')
#result = get_best_country_in_sport(client, 'Basketball')
result = get_best_sport_for_country(client, 'China')
for r in result:
    print(r)
# print(result)
print('---------')