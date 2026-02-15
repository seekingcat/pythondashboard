import config
import json

from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
import requests

app = Flask(__name__)


url = config.weather_api
quote_url = 'https://zenquotes.io/api/quotes/random'
# stock_url = config.stocks_api

res = requests.get(url)
weather = res.json()

quote_res = requests.get(quote_url)
quotes = quote_res.json()


def load_habits():
    with open('habits.json', 'r') as f:
        return json.load(f)
    
def calculate_streak(dates_completed):
    if not dates_completed:
        return 0
    
    # Convert string dates to date objects and sort newest first
    dates = sorted([datetime.fromisoformat(d).date() for d in dates_completed], reverse=True)
    
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    # If the most recent completion isn't today or yesterday, streak is dead
    if dates[0] != today and dates[0] != yesterday:
        return 0
    
    # Count consecutive days working backwards
    streak = 0
    expected_date = dates[0]
    
    for date in dates:
        if date == expected_date:
            streak += 1
            expected_date = date - timedelta(days=1)
        else:
            break  # Found a gap, stop counting
    
    return streak


@app.route('/')
def dashboard():
    habits_data = load_habits()

    for habit in habits_data['habits']:
        habit['streak'] = calculate_streak(habit['dates_completed'])

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

@app.route('/complete/<habit_name>', methods=['POST'])
def mark_complete(habit_name):
    # Load current habits
    habits_data = load_habits()
    
    # Get today's date as a string
    today = datetime.now().date().isoformat()
    
    # Find the habit and add today's date if not already there
    for habit in habits_data['habits']:
        if habit['name'] == habit_name:
            if today not in habit['dates_completed']:
                habit['dates_completed'].append(today)
            break
    
    # Save back to file
    with open('habits.json', 'w') as f:
        json.dump(habits_data, f, indent=2)
    
    # Redirect back to dashboard
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)