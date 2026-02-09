from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def dashboard():
    data = {
        'current_time': datetime.now().strftime('%I:%M %p'),
        'current_date': datetime.now().strftime('%A, %B, %d, %Y')
    }

    return render_template('dashboard.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)