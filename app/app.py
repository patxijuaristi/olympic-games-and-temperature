import sys
sys.path.append('..')

from flask import Flask, render_template, request
from pymongo import MongoClient
from querys.querys import get_best_sport_for_country, get_best_country_in_sport, country_better_winter_or_summer, country_most_medals_by_temperature, compare_two_country_results_by_temperature, get_best_country_by_year, get_avg_temperature
from querys.indexes import get_results, remove_indexes, indexes_sports_by_country, indexes_get_avg_temperature, indexes_get_best_country_in_sport
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.environ['MONGO_CLIENT'])

app = Flask(__name__)
app.config['STATIC_URL_PATH'] = '/static'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/queries')
def querys():
    return render_template('querys.html')

@app.route('/visualization-temperature')
def visualization_temperature():
    return render_template('visualization_temperature.html')

@app.route('/visualization-olympics')
def visualization_olympics():
    return render_template('visualization_olympics.html')

@app.route('/indexes', methods=['GET', 'POST'])
def indexes():
    if request.method == 'POST':
        index = request.form.get('index')
        if index == '':
            return render_template('indexes.html')
        
        remove_indexes(client)
        if index == 'sports_by_country':
            country = request.form.get('country')
            without_indexes = get_best_sport_for_country(client, country=country, explain=True)
            indexes_str = indexes_sports_by_country(client)
            with_indexes = get_best_sport_for_country(client, country=country, explain=True)
        elif index == 'get_avg_temperature':
            city = request.form.get('city')
            without_indexes = get_avg_temperature(client, city=city, start_date='01/01/2000', end_date='01/01/2001', explain=True)
            indexes_str = indexes_get_avg_temperature(client)
            with_indexes = get_avg_temperature(client, city=city, start_date='01/01/2000', end_date='01/01/2001', explain=True)
        elif index == 'get_best_country_in_sport':
            sport = request.form.get('sport')
            without_indexes = get_best_country_in_sport(client, sport=sport, explain=True)
            indexes_str = indexes_get_best_country_in_sport(client)
            with_indexes = get_best_country_in_sport(client, sport=sport, explain=True)
        else:
            return render_template('indexes.html')
        result_with = get_results(with_indexes, True)
        result_without = get_results(without_indexes, False)
            
        return render_template('indexes.html', result_with=result_with, result_without=result_without, indexes_str=indexes_str)
    else:
        return render_template('indexes.html')

@app.route('/sports-by-country', methods=['GET', 'POST'])
def sports_by_country():
    if request.method == 'POST':
        country = request.form.get('country')
        results = get_best_sport_for_country(client, country=country, explain=False)

        formatted_results = []
        for r in results:
            fr = {
                'sport': r['sport'],
                'gold': 0,
                'silver': 0,
                'bronze': 0,
                'total': r['total_medals']
            }

            for medal in r['medals']:
                medal_type = medal['medal'].lower()
                fr[medal_type] = medal['count']

            formatted_results.append(fr)
    else:
        country = ''
        formatted_results = []

    return render_template('sports_by_country.html', country=country, results=formatted_results)

@app.route('/best-country-in-sport', methods=['GET', 'POST'])
def best_country_in_sport():
    if request.method == 'POST':
        sport = request.form.get('sport')
        results = get_best_country_in_sport(client, sport, False)

        formatted_results = []
        for r in results:
            fr = {
                'country': r['country'],
                'gold': 0,
                'silver': 0,
                'bronze': 0,
                'total': r['total_medals']
            }

            for medal in r['medals']:
                medal_type = medal['medal'].lower()
                fr[medal_type] = medal['count']

            formatted_results.append(fr)
    else:
        sport = ''
        formatted_results = []
    
    return render_template('best_country_in_sport.html', sport=sport, results=formatted_results)

@app.route('/country-results-by-season', methods=['GET', 'POST'])
def country_results_by_season():
    if request.method == 'POST':
        country = request.form.get('country')
        result = country_better_winter_or_summer(client, country)
    else:
        country = ''
        result = []
    
    return render_template('country_results_by_season.html', country=country, result=result)

@app.route('/medals-temperature', methods=['GET', 'POST'])
def medals_and_temperature():
    if request.method == 'POST':
        country = request.form.get('country')
        results = list(country_most_medals_by_temperature(client, country))
    else:
        country = ''
        results = []

    return render_template('medals_and_temperature.html', country=country, results=results)

@app.route('/compare-countries-results', methods=['GET', 'POST'])
def compare_countries_results_by_temperature():
    if request.method == 'POST':
        country1 = request.form.get('country1')
        country2 = request.form.get('country2')
        results = list(compare_two_country_results_by_temperature(client, country1, country2))
    else:
        country1 = ''
        country2 = ''
        results = []
    
    return render_template('compare_countries_results.html', country1=country1, country2=country2, results=results)

@app.route('/best-country-per-games', methods=['GET'])
def best_country_per_games():
    results = list(get_best_country_by_year(client))
    
    return render_template('best_country_per_games.html', results=results)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
