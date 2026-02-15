from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Create database
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS topics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT,
        topic TEXT,
        exam_date TEXT,
        difficulty INTEGER,
        completed INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()

init_db()

# AI Priority Calculation
def calculate_priority(exam_date, difficulty, completed):
    today = datetime.today()
    exam = datetime.strptime(exam_date, "%Y-%m-%d")

    days_left = (exam - today).days
    if days_left <= 0:
        urgency = 10
    else:
        urgency = 10 / days_left

    priority = (urgency * 0.4) + (difficulty * 0.3) + ((1-completed) * 10 * 0.3)

    return round(priority, 2)

# Home page
@app.route("/")
def index():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT * FROM topics")
    rows = c.fetchall()

    topics = []
    for row in rows:
        priority = calculate_priority(row[3], row[4], row[5])
        topics.append({
            "id": row[0],
            "subject": row[1],
            "topic": row[2],
            "exam_date": row[3],
            "difficulty": row[4],
            "completed": row[5],
            "priority": priority
        })

    topics.sort(key=lambda x: x["priority"], reverse=True)

    return render_template("index.html", topics=topics)

# Add topic
@app.route("/add", methods=["POST"])
def add():
    subject = request.form["subject"]
    topic = request.form["topic"]
    exam_date = request.form["exam_date"]
    difficulty = request.form["difficulty"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO topics (subject, topic, exam_date, difficulty) VALUES (?, ?, ?, ?)",
        (subject, topic, exam_date, difficulty)
    )

    conn.commit()
    conn.close()

    return jsonify({"status": "success"})

# Mark complete
@app.route("/complete/<int:id>")
def complete(id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("UPDATE topics SET completed = 1 WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return jsonify({"status": "done"})

if __name__ == "__main__":
    app.run(debug=True)
