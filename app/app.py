import sys
sys.path.append('..')

from flask import Flask, render_template, request
from pymongo import MongoClient
from querys.querys import get_best_sport_for_country, get_best_country_in_sport, country_better_winter_or_summer
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.environ['MONGO_CLIENT'])

app = Flask(__name__)
app.config['STATIC_URL_PATH'] = '/static'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/querys')
def querys():
    return render_template('querys.html')

@app.route('/sports-by-country', methods=['GET', 'POST'])
def sports_by_country():
    if request.method == 'POST':
        country = request.form.get('country')
        results = get_best_sport_for_country(client, country)

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
        results = get_best_country_in_sport(client, sport)

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

if __name__ == '__main__':
    app.run(debug=True, port=8000)
