from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

app.secret_key = 'Sova Sona Da Phish'

StarRez = "housing.db"

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

@app.route("/employee/view", endpoint='employee_view')
def employee_view():
    return render_template("employeeView.html")

@app.route('/studentView/form')
def studentView():
    return render_template('housingForm.html')

@app.route("/messages", methods=['GET'])
def messages():
    return render_template('messages.html')

@app.route("/applications", methods=['GET'])
def applications():
    return render_template('applications.html')

@app.route("/employee/create", methods=['GET', 'POST'])
def new_employee():
    # Your code for rendering the employee creation form or handling POST request
    return render_template('employee_creation_form.html')
    
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('home'))


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
                session['student_id'] = user[0]  # Assuming the first column is student ID
                session['student_name'] = user[1]
                session['student_email'] = user[4]  # Assuming the email is in the fifth column
                print(f'Login successful')

                # Redirect to the student dashboard view after successful login
                return redirect(url_for('student_dash'))  # Use redirect to go to the student dashboard
            else:
                flash("Invalid email or password", "error")  # Flash error message if login fails
        else:
            flash("Error connecting to database", "error")

    return render_template('studentLogin.html')  # Render login template on GET request


@app.route('/studentView')
def student_dash():
    # Retrieve session data
    student_email = session.get("student_email")
    student_ID = session.get("student_id")

    # Debugging: Check if session variables are correctly set
    print(f"Student Email: {student_email}, Student ID: {student_ID}")

    if not student_email or not student_ID:
        flash("You need to be logged in to access this page", "error")
        return redirect(url_for('student_login'))

    # Open database connection
    conn = open_connection()
    if conn:
        cursor = conn.cursor()

        # Check if the student has already submitted the housing form
        sql_check = """
            SELECT * FROM housingForm
            WHERE f_studentID = ?
        """
        cursor.execute(sql_check, (student_ID,))
        existing_form = cursor.fetchone()
        
        if existing_form:
            # Query to fetch the f_status for the given student
            sql_housing_check = """
                SELECT f_status FROM housingForm
                WHERE f_studentID = ?
            """
            cursor.execute(sql_housing_check, (student_ID,))
            status = cursor.fetchone()
            stat = status[0]
            if stat == 'F':
                housing_status = "You have submitted your housing form, and it is still being processed."
            else:
                housing_status = "You have submitted your housing form and it has been approved."
        else:
            housing_status = "You have not yet submitted your housing form."

        conn.close()

        # Render the student view template with the housing status
        return render_template('studentView.html', housing_status=housing_status)

    else:
        flash("Error connecting to the database", "error")
        return redirect(url_for('student_login'))


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

@app.route("/studentView/form", methods=['GET', 'POST'])
def submitForm():
    # Retrieve session data
    student_email = session.get("student_email")
    student_ID = session.get("student_id")  # Assuming 'student_id' is used in the session

    # If the session does not have the student email or ID, handle the error (redirect to login or show message)
    if not student_email or not student_ID:
        flash("You need to be logged in to access this page", "error")
        return redirect(url_for('studentView'))  # Redirect to the login page if no session data found

    # Retrieve form data
    roomType = request.form.get("roomType")
    cleanliness = request.form.get("cleanliness")
    roomGender = request.form.get("roomGender")
    accommodations = request.form.get("accommodations")

    # Debugging: Print form data
    print(f"Form Attempt: {student_email} and {roomType} and {cleanliness} and {roomGender} and {accommodations}")

    # Open database connection
    conn = open_connection()
    if conn:
        cursor = conn.cursor()

        # Check if the student has already submitted the form
        sql_check = """
            SELECT * FROM housingForm f
            WHERE f.f_studentID = ?
        """
        cursor.execute(sql_check, (student_ID,))
        existing_form = cursor.fetchone()

        if existing_form:
            # If form already exists, show an error message
            flash("You've already completed the Housing Form", "error")
            return redirect('/login/student')  # Redirect to student view or another appropriate page

        # Get the current maximum f_formID
        cursor.execute("SELECT MAX(f_formID) FROM housingForm")
        max_formID = cursor.fetchone()[0]

        # Generate the new f_formID
        f_formID = max_formID + 1 if max_formID is not None else 1  # Default to 1 if no forms exist

        print(f"Generated f_formID: {f_formID}")

        # If no existing form, proceed with inserting the new form data into housingForm
        sql_insert_housingForm = """
            INSERT INTO housingForm (f_formID, f_studentID, f_status, f_accomodations, f_surveyID)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(sql_insert_housingForm, (f_formID, student_ID, 'F', accommodations, f_formID))
        conn.commit()

        # Now insert the data into the profileSurvey table using the f_formID as s_surveyID
        sql_insert_profileSurvey = """
            INSERT INTO profileSurvey (s_surveyID, s_prefRoomType, s_cleanliness, s_prefRoomGen)
            VALUES (?, ?, ?, ?)
        """
        cursor.execute(sql_insert_profileSurvey, (f_formID, roomType, cleanliness, roomGender))
        conn.commit()

        # Close connection
        conn.close()

        # Show a success message after submitting the form
        flash("Housing form submitted successfully!", "success")
        return redirect(url_for('studentView'))  # Redirect to a page after form submission

    else:
        flash("Error connecting to the database", "error")
        return redirect(url_for('studentView'))

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
                session['employee_name'] = user[1]
                session['employee_email'] = user[2]  # Assuming the email is in the third column
                print(f'Login successful')

                # Redirect to the employee view page
                return redirect(url_for('employee_view'))  # This should match the route function name 'employee_view'
            else:
                flash("Invalid email or password", "error")  # Flash error message if login fails
        else:
            flash("Error connecting to database", "error")
    
    return render_template("employeeLogin.html")

@app.route("/employee/creation", methods=['GET', 'POST'])
def employee_create():
    # Debugging print to check if the route is hit
    print("Employee create route hit!")
    
    if request.method == 'POST':
        # Debugging print to check if the POST method is received
        print("POST method received")
        
        # Get the form data
        employee_name = request.form.get('employee_name')
        employee_email = request.form.get('employee_email')
        employee_password = request.form.get('employee_password')

        # Debug: Print the received data
        print(f"Received data: Name: {employee_name}, Email: {employee_email}, Password: {employee_password}")

        # Assuming you have a function to open the database connection and insert data
        conn = open_connection()  # Make sure this function works
        if conn:
            try:
                cursor = conn.cursor()

                # Generate a new employee ID (this assumes auto-incrementing IDs in the DB)
                cursor.execute("SELECT MAX(e_employeeID) FROM employee")
                max_id = cursor.fetchone()[0]
                new_employee_id = max_id + 1 if max_id is not None else 1  # Default to 1 if no employees exist

                # Insert new employee into the database
                sql_insert = """
                    INSERT INTO employee (e_employeeID, e_name, e_email, e_password)
                    VALUES (?, ?, ?, ?)
                """
                cursor.execute(sql_insert, (new_employee_id, employee_name, employee_email, employee_password))
                conn.commit()

                # Success message
                flash(f"Employee {employee_name} created successfully!", "success")
                return redirect(url_for('employee_view'))  # Redirect to employee view or another page

            except Exception as e:
                print(f"Error occurred: {e}")
                flash("An error occurred while creating the employee. Please try again.", "error")
            finally:
                conn.close()
        else:
            flash("Error connecting to the database", "error")
        
    return render_template('employee_creation_form.html')

@app.route("/employee/application-approval", methods=['GET', 'POST'])
def application_approval():
    # Open a connection to the database
    conn = open_connection()
    if conn:
        cursor = conn.cursor()

        if request.method == 'POST':
            # Handle form submission for approving or rejecting applications
            action = request.form.get('action')  # 'approve' or 'reject'
            form_id = request.form.get('form_id')  # The form ID to update

            if action == 'approve':
                # Update the f_status to 'A' for approved
                sql_update = "UPDATE housingForm SET f_status = 'A' WHERE f_formID = ?"
                cursor.execute(sql_update, (form_id,))
                conn.commit()
                flash(f"Application {form_id} approved!", "success")

            elif action == 'reject':
                # Update the f_status to 'R' for rejected
                sql_update = "UPDATE housingForm SET f_status = 'R' WHERE f_formID = ?"
                cursor.execute(sql_update, (form_id,))
                conn.commit()
                flash(f"Application {form_id} rejected.", "error")

            # Redirect to the same page after updating the status
            return redirect(url_for('application_approval'))

        else:
            # Query for all housing forms with f_status 'F' and join with student table to get the student name
            sql_query = """
                SELECT hf.*, s.s_name
                FROM housingForm hf
                JOIN student s ON hf.f_studentID = s.s_studentID
                WHERE hf.f_status = 'F'
            """
            cursor.execute(sql_query)
            applications = cursor.fetchall()  # Fetch all records

            # Debugging: Print applications to check the result
            print(f"Applications with f_status = 'F': {applications}")

            conn.close()  # Close the connection

            # Pass the applications data to the template
            return render_template("applications.html", applications=applications)
    else:
        flash("Error connecting to the database", "error")
        return redirect(url_for('employee_view'))



if __name__ == "__main__":
    app.run(debug=True)
