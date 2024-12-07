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
                session['student_id'] = user[0]  # Assuming the first column is customer ID
                session['student_email'] = user[2]  # Assuming the email is in the third column
                print(f'Login successful')
                return redirect(url_for('studentView'))  # Redirect to student view page
            else:
                flash("Invalid email or password", "error")  # Flash error message if login fails
        else:
            flash("Error connecting to database", "error")

    return render_template('studentLogin.html')  # Render login template on GET request

@app.route("/signup/student", methods=['GET', 'POST'])
def student_signup():
    if request.method == 'POST':
        student_name = request.form.get('student_name')
        student_gender = request.form.get('gender')
        student_email = request.form.get('student_email')
        student_password = request.form.get('student_password')
        student_year = request.form.get('student_year')

        print(f"Sign Up Attempt: {student_name}, {student_gender}, {student_email}, {student_password}, {student_year}")

        # Open connection to the database
        conn = open_connection()
        if conn:
            try:
                cursor = conn.cursor()

                # Check if the student already exists (based on email)
                sql_check = "SELECT * FROM student WHERE s_email = ?"
                cursor.execute(sql_check, (student_email,))
                existing_user = cursor.fetchone()

                if existing_user:
                    flash("This email is already registered. Please login.", "error")
                else:
                    # Fetch the current max s_studentID and increment it
                    sql_max_id = "SELECT MAX(s_studentID) FROM student"
                    cursor.execute(sql_max_id)
                    max_id = cursor.fetchone()[0]
                    new_student_id = max_id + 1 if max_id is not None else 1  # Default to 1 if no student exists

                    # Insert new student with manually incremented s_studentID
                    sql_insert = """
                        INSERT INTO student (s_studentID, s_name, s_gender, s_year, s_email, s_password, s_buildingID, s_roomID)
                        VALUES (?, ?, ?, ?, ?, ?, 0, 0)
                    """
                    cursor.execute(sql_insert, (new_student_id, student_name, student_gender, student_year, student_email, student_password))
                    conn.commit()
                    flash("Sign-up successful! You can now log in.", "success")
                    return redirect(url_for('student_login'))  # Redirect back to the student login page

            except sqlite3.OperationalError as e:
                print(f"Database error: {e}")
                flash("There was an issue with the database. Please try again later.", "error")

            finally:
                # Ensure the connection is closed after the operation
                conn.close()

    return render_template('studentSignup.html')  # Render signup page on GET request


    return render_template('studentSignup.html')  # Render signup page on GET request



# Employee login route
@app.route("/login/employee", methods=['GET', 'POST'])
def employee_login():
    if request.method == 'POST':
        employee_email = request.form.get('employee_email')
        employee_password = request.form.get('employee_password')
        print(f"Login Attempt: With {employee_email} and {employee_password}")

        conn = open_connection()
        if conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM employee WHERE e_email = ? AND e_password = ?"
            cursor.execute(sql, (employee_email, employee_password))
            user = cursor.fetchone()
            conn.close()

            if user:
                # Set session variables upon successful login
                session['employee_id'] = user[0]  # Assuming the first column is employee ID
                session['employee_email'] = user[2]  # Assuming the email is in the third column
                print(f'Login successful')
                return redirect(url_for('employeeView'))  # Redirect to the employee view page
            else:
                flash("Invalid email or password", "error")  # Flash error message if login fails
        else:
            flash("Error connecting to database", "error")

    return render_template('employeeLogin.html')  # Render login template on GET request


if __name__ == "__main__":
    app.run(debug=True)
