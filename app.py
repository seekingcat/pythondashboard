import os
import json
from dotenv import load_dotenv

from flask import Flask, render_template, redirect, url_for
from datetime import datetime, timedelta
from database import get_all_habits, mark_habit_complete, init_db
import requests
load_dotenv()
init_db()

app = Flask(__name__)

weather_url = os.getenv('WEATHER_API')
quote_url = 'https://zenquotes.io/api/quotes/random'

res = requests.get(weather_url)
weather = res.json()

quote_res = requests.get(quote_url)
quotes = quote_res.json()


# def load_habits():
#     with open('habits.json', 'r') as f:
#         return json.load(f)
    
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
    habits = get_all_habits()

    for habit in habits:
        habit['streak'] = calculate_streak(habit['dates_completed'])

    data = {
            'current_time': datetime.now().strftime('%I:%M %p'),
            'current_date': datetime.now().strftime('%A, %B, %d, %Y'),
            'description': weather['weather'][0]['description'],
            'temp': weather['main']['temp'],
            'feels': weather['main']['feels_like'],
            'quote':quotes[0]['q'],
            'author': quotes[0]['a'],
            'habits': habits
        }

    return render_template('dashboard.html', data=data)

@app.route('/complete/<int:habit_id>', methods=['POST'])
def mark_complete(habit_id):
    # Get today's date as a string
    today = datetime.now().date().isoformat()
    
    mark_habit_complete(habit_id, today)
    
    # Redirect back to dashboard
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))