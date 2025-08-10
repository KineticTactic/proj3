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
    db = get_db()
    db.execute('CREATE TABLE IF NOT EXISTS visits (count INTEGER)')
    cur = db.execute('SELECT count FROM visits')
    row = cur.fetchone()
    if row:
        count = row[0] + 1
        db.execute('UPDATE visits SET count = ?', (count,))
    else:
        count = 1
        db.execute('INSERT INTO visits (count) VALUES (1)')
    db.commit()
    return render_template('index.html', count=count)

if __name__ == "__main__":
    app.run(debug=True)