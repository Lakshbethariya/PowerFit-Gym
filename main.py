from flask import Flask, render_template, request, redirect, session, flash, url_for
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- DATABASE ----------------
def create_db():
    conn = sqlite3.connect("gym.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS members(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        plan TEXT,
        joining_date TEXT,
        expiry_date TEXT,
        status TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_name TEXT,
        date TEXT
    )
    """)

    # Default admin
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users VALUES (NULL,'admin','1234','admin')")

    conn.commit()
    conn.close()

create_db()

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template("index.html")

# ---------------- LOGIN ----------------
@app.route('/login')
def login():
    return redirect('/?page=login')

@app.route('/login_check', methods=['POST'])
def login_check():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()

    if not username or not password:
        return redirect('/?page=login&error=1')

    conn = sqlite3.connect("gym.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['user'] = username
        session['role'] = user[3]

        if user[3] == 'admin':
            return redirect('/admin')
        else:
            return redirect('/dashboard')
    else:
        return redirect('/?page=login&error=1')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ---------------- ADD MEMBER ----------------
@app.route('/add_member', methods=['POST'])
def add_member():
    name         = request.form['name']
    age          = request.form['age']
    plan         = request.form['plan']
    joining_date = request.form['joining_date']

    join_date_obj = datetime.strptime(joining_date, "%Y-%m-%d")

    if plan == "1 Month":
        expiry = join_date_obj + timedelta(days=30)
    elif plan == "3 Months":
        expiry = join_date_obj + timedelta(days=90)
    elif plan == "6 Months":
        expiry = join_date_obj + timedelta(days=180)
    else:
        expiry = join_date_obj + timedelta(days=365)

    expiry_date = expiry.strftime("%Y-%m-%d")

    conn = sqlite3.connect("gym.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO members(name, age, plan, joining_date, expiry_date, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, age, plan, joining_date, expiry_date, "pending"))

    # Create member login (username = full name, default password = 1234)
    cursor.execute("SELECT * FROM users WHERE username=?", (name,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users(username, password, role) VALUES (?,?,?)", (name, "1234", "member"))

    conn.commit()
    conn.close()

    # Redirect back: if admin added, go to admin; else go to home
    if session.get('role') == 'admin':
        return redirect('/admin')
    return redirect('/?msg=member_added')

# ---------------- ADMIN ----------------
@app.route('/admin')
def admin():
    if 'role' not in session or session['role'] != 'admin':
        return redirect('/?page=login&error=1')

    conn = sqlite3.connect("gym.db")
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("UPDATE members SET status='expired' WHERE expiry_date < ? AND status='active'", (today,))
    conn.commit()

    cursor.execute("SELECT * FROM members")
    rows = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM members WHERE status='active'")
    active_count = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM members WHERE status='expired'")
    expired_members = cursor.fetchall()

    cursor.execute("SELECT * FROM members WHERE status='deleted'")
    deleted_members = cursor.fetchall()

    cursor.execute("SELECT * FROM members WHERE status='active'")
    active_members = cursor.fetchall()

    conn.close()

    return render_template("admin.html",
        rows=rows,
        active_count=active_count,
        expired_members=expired_members,
        deleted_members=deleted_members,
        active_members=active_members
    )

# ---------------- APPROVE ----------------
@app.route('/approve/<int:id>')
def approve(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect('/?page=login')
    conn = sqlite3.connect("gym.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE members SET status='active' WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/admin')

# ---------------- DELETE ----------------
@app.route('/delete/<int:id>')
def delete(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect('/?page=login')
    conn = sqlite3.connect("gym.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE members SET status='deleted' WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/admin')

# ---------------- MARK ATTENDANCE ----------------
@app.route('/mark_attendance/<int:id>')
def mark_attendance(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect('/?page=login')
    today = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect("gym.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, status FROM members WHERE id=?", (id,))
    result = cursor.fetchone()
    if result:
        name, status = result
        if status == "active":
            cursor.execute("SELECT * FROM attendance WHERE member_name=? AND date=?", (name, today))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO attendance(member_name,date) VALUES (?,?)", (name, today))
    conn.commit()
    conn.close()
    return redirect('/admin')

# ---------------- MEMBER DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/?page=login')

    conn = sqlite3.connect("gym.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE name=?", (session['user'],))
    member = cursor.fetchone()
    cursor.execute("SELECT date FROM attendance WHERE member_name=?", (session['user'],))
    attendance = cursor.fetchall()
    conn.close()

    if not member:
        session.clear()
        return redirect('/?page=login&error=1')

    return render_template("dashboard.html", member=member, attendance=attendance)

# ---------------- ADMIN ATTENDANCE ----------------
@app.route('/attendance')
def attendance_page():
    if 'role' not in session or session['role'] != 'admin':
        return redirect('/?page=login')
    conn = sqlite3.connect("gym.db")
    cursor = conn.cursor()
    cursor.execute("SELECT member_name, date FROM attendance")
    data = cursor.fetchall()
    conn.close()
    return render_template("attendance.html", data=data)

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)
