from pymongo import MongoClient
#from querys import get_avg_temperature, get_best_country_in_sport, get_best_sport_for_country, country_better_winter_or_summer, get_olimpics_avg_temperature_by_year
import querys
import os
from dotenv import load_dotenv

load_dotenv()

# Read the Mongo connection string from the environment variables and create the client
client = MongoClient(os.environ['MONGO_CLIENT'])

print('---------')
#result = get_avg_temperature(client, 'Bilbao','07/02/2014','23/02/2014')
#result = get_best_country_in_sport(client, 'Basketball')
#result = get_best_sport_for_country(client, 'China')
#result = country_better_winter_or_summer(client, 'China')
#result = querys.get_olimpics_avg_temperature_by_year(client, '2016')
#result = querys.country_most_medals_by_temperature(client, 'Spain')
result = querys.compare_two_country_results_by_temperature(client, 'Spain', 'Norway')
for r in result:
    print(r)
print(result)
print('---------')