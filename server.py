from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

app.secret_key = 'Sova Sona Da Phish'

# Database configuration
StarRez = "housing.db"

# Function to open database connection
def open_connection():
    conn = None
    try:
        conn = sqlite3.connect(StarRez)
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn

# Home route
@app.route("/")
def home():
    return render_template('welcome.html')

# Student login route
@app.route("/login/student", methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        student_email = request.form.get('student_email')
        student_password = request.form.get('student_password')
        print(f"Login Attempt: With {student_email} and {student_password}")

        conn = open_connection()
        if conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM student WHERE s_email = ? AND s_password = ?"
            cursor.execute(sql, (student_email, student_password))
            user = cursor.fetchone()
            conn.close()

            if user:
                # Set session variables upon successful login
                session['customer_id'] = user[0]  # Assuming the first column is customer ID
                session['email'] = user[2]  # Assuming the email is in the third column
                print(f'Login successful')
                return redirect(url_for('studentView'))  # Redirect to student view page
            else:
                flash("Invalid email or password", "error")  # Flash error message if login fails
        else:
            flash("Error connecting to database", "error")

    return render_template('studentLogin.html')  # Render login template on GET request

# Employee login route
@app.route("/login/employee")
def employee_login():
    return render_template('employeeLogin.html')

# You can add other routes here if necessary

if __name__ == "__main__":
    app.run(debug=True)
