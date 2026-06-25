from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create database table
def init_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        roll_number TEXT UNIQUE NOT NULL,
        math REAL,
        science REAL,
        english REAL
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():

    if request.method == 'POST':

        name = request.form['name']
        roll = request.form['roll']

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        try:

            cursor.execute(
                "INSERT INTO students(name, roll_number) VALUES (?, ?)",
                (name, roll)
            )

            conn.commit()

        except sqlite3.IntegrityError:

            conn.close()

            return render_template(
                "update_confirm.html",
                name=name,
                roll=roll
            )

        conn.close()

        return redirect('/students')

    return render_template('add_student.html')

@app.route('/add_grade', methods=['GET', 'POST'])
def add_grade():

    if request.method == 'POST':

        roll = request.form['roll']
        math = request.form['math']
        science = request.form['science']
        english = request.form['english']

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE students
        SET math=?, science=?, english=?
        WHERE roll_number=?
        """, (math, science, english, roll))

        conn.commit()
        conn.close()

        return redirect('/students')

    return render_template('add_grade.html')


@app.route('/students')
def students():

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    data = cursor.fetchall()

    conn.close()

    return render_template('students.html', students=data)

@app.route('/update_student', methods=['POST'])
def update_student():

    name = request.form['name']
    roll = request.form['roll']

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE students SET name=? WHERE roll_number=?",
        (name, roll)
    )

    conn.commit()
    conn.close()

    return redirect('/students')

if __name__ == '__main__':
    app.run(debug=True)