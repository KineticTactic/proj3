import sqlite3
from flask import Flask, render_template, g

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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/student-login')
def student_login():
    return render_template('student_login.html')

@app.route('/club-login')
def club_login():
    return render_template('club_login.html')

if __name__ == "__main__":
    app.run(debug=True)