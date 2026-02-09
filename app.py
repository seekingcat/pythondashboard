import config

from flask import Flask, render_template
from datetime import datetime
import requests

app = Flask(__name__)


url = config.weather_api
quote_url = 'https://zenquotes.io/api/quotes/random'

@app.route('/')
def dashboard():
    quote_res = requests.get(quote_url)
    quotes = quote_res.json()
    res = requests.get(url)
    weather = res.json()
    data = {
        'current_time': datetime.now().strftime('%I:%M %p'),
        'current_date': datetime.now().strftime('%A, %B, %d, %Y'),
        'description': weather['weather'][0]['description'],
        'temp': weather['main']['temp'],
        'feels': weather['main']['feels_like'],
        'quote':quotes[0]['q'],
        'author': quotes[0]['a']
    }

    return render_template('dashboard.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)