import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g

app = Flask(__name__)
DATABASE = 'database.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    db.commit()

@app.cli.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    print('Initialized the database.')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/student-login')
def student_login():
    return render_template('student_login.html')

@app.route('/club-login')
def club_login():
    return render_template('club_login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/feed')
def user_feed():
    return render_template('user_feed.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cur = db.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cur.fetchone()
        if user:
            return redirect(url_for('home'))
        else:
            error = 'Invalid credentials'
    return render_template('student_login.html', error=error)

if __name__ == "__main__":
    app.run(debug=True)