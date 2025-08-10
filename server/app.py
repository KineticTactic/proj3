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

def reset_users_table():
    db = get_db()
    # Check if 'users' table exists and has correct columns
    try:
        cur = db.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cur.fetchall()]
        required = {'username', 'password', 'email', 'role'}
        if not required.issubset(set(columns)):
            db.execute('DROP TABLE IF EXISTS users')
    except sqlite3.OperationalError:
        db.execute('DROP TABLE IF EXISTS users')
    db.commit()

def init_db():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT
        )
    ''')
    db.commit()

@app.cli.command('init-db')
def init_db_command():
    """Initializes the database."""
    reset_users_table()
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    success = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        role = request.form['role']  # "student" or "club"
        db = get_db()
        try:
            db.execute(
                'INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)',
                (username, password, email, role)
            )
            db.commit()
            success = "Registration successful! You can now log in."
        except sqlite3.IntegrityError:
            error = "Username already exists. Please choose another."
    return render_template('register.html', error=error, success=success)

@app.route('/feed')
def user_feed():
    return render_template('user_feed.html')

@app.route('/add-event')
def add_event():
    return render_template('add_event.html')

@app.route('/club-dashboard')
def club_dashboard():
    # Dummy data for demonstration
    events = [
        {
            "id": "tech1",
            "title": "Robotics Tech Talk",
            "date": "August 15, 2025",
            "time": "6:00 PM",
        },
        {
            "id": "cultural1",
            "title": "Music Jam Session",
            "date": "August 18, 2025",
            "time": "8:00 PM",
        },
    ]
    return render_template('club_dashboard.html', events=events)

@app.route('/edit-event/<event_id>')
def edit_event(event_id):
    # Dummy data for demonstration
    events = {
        "tech1": {
            "id": "tech1",
            "title": "Robotics Tech Talk",
            "date": "2025-08-15",
            "time": "18:00",
            "description": "Join us for an insightful talk on the future of robotics and automation. This session will cover the latest advancements, ethical considerations, and career opportunities in the field. Hosted by the University Robotics Club.",
            "eligibility": "Open to all students and faculty. No prior knowledge of robotics is required.",
        },
        "cultural1": {
            "id": "cultural1",
            "title": "Music Jam Session",
            "date": "2025-08-18",
            "time": "20:00",
            "description": "An open stage for all music lovers. Bring your instruments and voice!",
            "eligibility": "Open to all students.",
        },
    }
    event = events.get(event_id)
    return render_template('edit_event.html', event=event)

@app.route('/view-registrations/<event_id>')
def view_registrations(event_id):
    # Dummy data for demonstration
    event = {
        "tech1": {"title": "Robotics Tech Talk"},
        "cultural1": {"title": "Music Jam Session"},
    }.get(event_id)

    registrations = [
        {"id": "101", "name": "Alice Johnson", "email": "alice@example.com"},
        {"id": "102", "name": "Bob Williams", "email": "bob@example.com"},
        {"id": "103", "name": "Charlie Brown", "email": "charlie@example.com"},
    ]
    return render_template('view_registrations.html', event=event, registrations=registrations)

@app.route('/event/<int:event_id>')
def event_details(event_id):
    # Dummy data for demonstration
    events = {
        1: {
            "id": "tech1",
            "title": "Robotics Tech Talk",
            "date": "August 15, 2025",
            "time": "6:00 PM",
            "description": "Join us for an insightful talk on the future of robotics and automation. This session will cover the latest advancements, ethical considerations, and career opportunities in the field. Hosted by the University Robotics Club.",
            "eligibility": "Open to all students and faculty. No prior knowledge of robotics is required.",
            "google_calendar_link": "https://calendar.google.com/calendar/render?action=TEMPLATE&text=Robotics+Tech+Talk&dates=20250815T180000/20250815T190000&details=Join+us+for+an+insightful+talk+on+the+future+of+robotics+and+automation.&location=Online"
        },
        # Add other events here
    }
    event = events.get(event_id, {
        "id": "default",
        "title": "Event Not Found",
        "date": "N/A",
        "time": "N/A",
        "description": "The event you are looking for does not exist.",
        "eligibility": "N/A",
        "google_calendar_link": "#"
    })
    return render_template('event_details.html', event=event)


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
            return redirect("/feed")
        else:
            error = 'Invalid credentials'
    return render_template('student_login.html', error=error)

if __name__ == "__main__":
    app.run(debug=True)