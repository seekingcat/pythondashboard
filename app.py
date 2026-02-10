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

stocks_res = requests.get(stock_url)
stocks = stocks_res.json()
# stock_data = stocks['Meta Data']['3. Last Refreshed']

def load_habits():
    with open('habits.json', 'r') as f:
        return json.load(f)

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
            # 'stock_date':stocks['Meta Data']['3. Last Refreshed'],
            # 'stock_name': stocks['Meta Data']['2. Symbol'],
            # 'open': stocks['Time Series (Daily)'][stock_date]['1. open'],
            # 'close': stocks['Time Series (Daily)'][stock_date]['4. close'],
            'habits': habits_data['habits']
        }

    return render_template('dashboard.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)