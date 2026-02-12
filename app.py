import config
import json

from flask import Flask, render_template
from datetime import datetime, timedelta
import requests

app = Flask(__name__)


url = config.weather_api
quote_url = 'https://zenquotes.io/api/quotes/random'
stock_url = config.stocks_api

res = requests.get(url)
weather = res.json()

quote_res = requests.get(quote_url)
quotes = quote_res.json()


def load_habits():
    with open('habits.json', 'r') as f:
        return json.load(f)
    
# def write_habits(new_data, filename='habits.json'):
#     with open('habits.json', 'r+') as f:
#         f_data = json.load(f)
#         f_data['date_completed'].append(new_data)
#         f.seek(0)
#         json.dump(f_data, f)

def calculate_streak(dates_completed):
    if not dates_completed:
        return 0
    
    sorted_dates = sorted(dates_completed, reverse=True)
    today = datetime.now().date().isoformat()

    return 0



@app.route('/')
def dashboard():
    habits_data = load_habits()

    data = {
            'current_time': datetime.now().strftime('%I:%M %p'),
            'current_date': datetime.now().strftime('%A, %B, %d, %Y'),
            'description': weather['weather'][0]['description'],
            'temp': weather['main']['temp'],
            'feels': weather['main']['feels_like'],
            'quote':quotes[0]['q'],
            'author': quotes[0]['a'],
            'habits': habits_data['habits']
        }

    return render_template('dashboard.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)