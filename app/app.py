import sys
sys.path.append('..')

from flask import Flask, render_template, request
from pymongo import MongoClient
from querys.querys import get_best_sport_for_country
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

@app.route('/sports_by_country', methods=['GET', 'POST'])
def search():
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

if __name__ == '__main__':
    app.run(debug=True, port=8000)
