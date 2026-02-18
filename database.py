import _sqlite3
from datetime import datetime

def get_db():
    conn = _sqlite3.connect('habits.db')
    conn.row_factory = _sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL
        )
    ''')
    
    # Create completions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            date_completed TEXT NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits (id),
            UNIQUE(habit_id, date_completed)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_all_habits():
    conn = get_db()
    cursor = conn.cursor()

    habits = cursor.execute('SELECT * FROM habits').fetchall()

    result = []
    for habit in habits:
        completions = cursor.execute(
            'SELECT date_completed FROM completions WHERE habit_id = ?',
            (habit['id'],)
        ).fetchall()

        dates = [c['date_completed'] for c in completions]

        result.append({
            'id': habit['id'],
            'name': habit['name'],
            'dates_completed': dates
        })

    conn.close()
    return result

def add_habit(name):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO habits (name, created_at) VALUES (?, ?)',
        (name, datetime.now().date().isoformat())
    )

    conn.commit()
    conn.close()

def mark_habit_complete(habit_id, date):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        'INSERT OR IGNORE INTO completions (habit_id, date_completed) VALUES (?, ?)',
        (habit_id, date)
    )
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print('Database created!')