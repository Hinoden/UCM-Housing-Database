from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import random
from sqlite3 import Error
from datetime import datetime

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

@app.route("/")
def home():
    return render_template('welcome.html')

@app.route("/employee_view", endpoint='employee_view')
def employee_view():
    return render_template("employeeView.html")

@app.route('/studentView/form')
def studentView():
    return render_template('housingForm.html')

@app.route("/applications", methods=['GET'])
def applications():
    return render_template('applications.html')

@app.route("/employee/create", methods=['GET', 'POST'])
def new_employee():
    return render_template('employee_creation_form.html')

@app.route("/employee/delete_message", methods = ['GET', 'POST'])
def delMessage():
    return render_template('deleteMessage.html')
    
@app.route("/logout")
def logout():
    session.clear()
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
                session['student_id'] = user[0] 
                session['student_name'] = user[1]
                session['student_email'] = user[4] 
                print(f'Login successful')

                return redirect(url_for('student_dash')) 
            else:
                flash("Invalid email or password", "error")  
        else:
            flash("Error connecting to database", "error")

    return render_template('studentLogin.html') 


@app.route('/studentView')
def student_dash():
    student_email = session.get("student_email")
    student_ID = session.get("student_id")

    print(f"Student Email: {student_email}, Student ID: {student_ID}")

    if not student_email or not student_ID:
        flash("You need to be logged in to access this page", "error")
        return redirect(url_for('student_login'))

    conn = open_connection()
    if conn:
        cursor = conn.cursor()

        sql_check = """
            SELECT f_status FROM housingForm WHERE f_studentID = ?
        """
        cursor.execute(sql_check, (student_ID,))
        status = cursor.fetchone()
        
        if status:
            stat = status[0]
            if stat == 'F':
                housing_status = "You have submitted your housing form, and it is still being processed."
            elif stat == 'A':
                housing_status = "You have submitted your housing form and it has been approved."
            elif stat == 'R':
                housing_status = "You have submitted your housing form and it has been rejected."
            else:
                housing_status = "Unknown status."
        else:
            housing_status = "You have not yet submitted your housing form."

        conn.close()

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
                    sql_max_id = "SELECT MAX(s_studentID) FROM student"
                    cursor.execute(sql_max_id)
                    max_id = cursor.fetchone()[0]
                    new_student_id = max_id + 1 if max_id is not None else 1

                    sql_insert = """
                        INSERT INTO student (s_studentID, s_name, s_gender, s_year, s_email, s_password, s_buildingID, s_roomID)
                        VALUES (?, ?, ?, ?, ?, ?, 0, 0)
                    """
                    cursor.execute(sql_insert, (new_student_id, student_name, student_gender, student_year, student_email, student_password))
                    conn.commit()
                    flash("Sign-up successful! You can now log in.", "success")
                    return redirect(url_for('student_login')) 

            except sqlite3.OperationalError as e:
                print(f"Database error: {e}")
                flash("There was an issue with the database. Please try again later.", "error")

            finally:
                conn.close()

    return render_template('studentSignup.html')

@app.route("/studentView/form", methods=['GET', 'POST'])
def submitForm():
    student_email = session.get("student_email")
    student_ID = session.get("student_id") 

    if not student_email or not student_ID:
        flash("You need to be logged in to access this page", "error")
        return redirect(url_for('studentView'))

    roomType = request.form.get("roomType")
    cleanliness = request.form.get("cleanliness")
    roomGender = request.form.get("roomGender")
    accommodations = request.form.get("accommodations")

    print(f"Form Attempt: {student_email} and {roomType} and {cleanliness} and {roomGender} and {accommodations}")

    conn = open_connection()
    if conn:
        cursor = conn.cursor()

        sql_check = """
            SELECT * FROM housingForm f
            WHERE f.f_studentID = ?
        """
        cursor.execute(sql_check, (student_ID,))
        existing_form = cursor.fetchone()

        if existing_form:
            flash("You've already completed the Housing Form", "error")
            return redirect('/login/student') 

        cursor.execute("SELECT MAX(f_formID) FROM housingForm")
        max_formID = cursor.fetchone()[0]

        f_formID = max_formID + 1 if max_formID is not None else 1

        print(f"Generated f_formID: {f_formID}")

        sql_insert_housingForm = """
            INSERT INTO housingForm (f_formID, f_studentID, f_status, f_accomodations, f_surveyID)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(sql_insert_housingForm, (f_formID, student_ID, 'F', accommodations, f_formID))
        conn.commit()

        sql_insert_profileSurvey = """
            INSERT INTO profileSurvey (s_surveyID, s_prefRoomType, s_cleanliness, s_prefRoomGen)
            VALUES (?, ?, ?, ?)
        """
        cursor.execute(sql_insert_profileSurvey, (f_formID, roomType, cleanliness, roomGender))
        conn.commit()

        conn.close()

        flash("Housing form submitted successfully!", "success")
        return redirect(url_for('studentView'))

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
                session['employee_id'] = user[0]
                session['employee_name'] = user[1]
                session['employee_email'] = user[2]
                print(f'Login successful')

                return redirect(url_for('employee_view'))
            else:
                flash("Invalid email or password", "error")
        else:
            flash("Error connecting to database", "error")
    
    return render_template("employeeLogin.html")

@app.route("/employee/creation", methods=['GET', 'POST'])
def employee_create():
    if request.method == 'POST':
        print("POST method received")
        employee_name = request.form.get('employee_name')
        employee_email = request.form.get('employee_email')
        employee_password = request.form.get('employee_password')

        print(f"Received data: Name: {employee_name}, Email: {employee_email}, Password: {employee_password}")
        conn = open_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT MAX(e_employeeID) FROM employee")
                max_id = cursor.fetchone()[0]
                new_employee_id = max_id + 1 if max_id is not None else 1
                sql_insert = """
                    INSERT INTO employee (e_employeeID, e_name, e_email, e_password)
                    VALUES (?, ?, ?, ?)
                """
                cursor.execute(sql_insert, (new_employee_id, employee_name, employee_email, employee_password))
                conn.commit()
                flash(f"Employee {employee_name} created successfully!", "success")
                return redirect(url_for('employee_view'))

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
    conn = open_connection()
    if conn:
        cursor = conn.cursor()

        if request.method == 'POST':
            action = request.form.get('action')  # 'approve' or 'reject'
            form_id = request.form.get('form_id')

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
            return redirect(url_for('application_approval'))

        else:
            sql_query = """
                SELECT hf.*, s.s_name
                FROM housingForm hf
                JOIN student s ON hf.f_studentID = s.s_studentID
                WHERE hf.f_status = 'F'
            """
            cursor.execute(sql_query)
            applications = cursor.fetchall()
            print(f"Applications with f_status = 'F': {applications}")

            conn.close()
            return render_template("applications.html", applications=applications)
    else:
        flash("Error connecting to the database", "error")
        return redirect(url_for('employee_view'))
    
@app.route('/select-room', methods=['GET', 'POST'])
def select_room():
    student_id = session['student_id']
    available_rooms = get_available_rooms()

    if request.method == 'POST':
        room_info = request.form.get('room_id')
        
        if room_info:
            room_id, building_id = room_info.split(':')
            assign_room_to_student(room_id)
            update_housing_status(student_id, room_id, building_id)
            return render_template('select_room.html')

    return render_template('select_room.html', rooms=available_rooms)


def assign_room_to_student(room_id):
    conn = open_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE room SET r_occupied = 'T' WHERE r_roomID = ?
    """, (room_id,))
    conn.commit()
    conn.close()

def update_housing_status(student_id, room_id, building_id):
    conn = open_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE student 
        SET s_buildingID = ?, s_roomID = ? 
        WHERE s_studentID = ?
    """, (building_id, room_id, student_id))
    conn.commit()
    conn.close()

def get_available_rooms():
    conn = open_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT r_roomID, r_buildingID FROM room WHERE r_occupied = 'F'") #F means unoccupied
    available_rooms = cursor.fetchall()
    conn.close()
    return available_rooms

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        message = request.form.get('message')
        employee_id = request.form.get('employee')
        
        if not message or not employee_id:
            flash("Please provide both a message and select an employee.", "error")
            return redirect(url_for('contact'))
        
        conn = open_connection()
        if conn:
            try:
                cursor = conn.cursor()
                sql_insert_contact = """
                    INSERT INTO contact (c_contactDateTime, c_reason, c_studentID, c_employeeID)
                    VALUES (?, ?, ?, ?)
                """
                contact_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute(sql_insert_contact, (contact_datetime, message, session.get('student_id'), employee_id))
                conn.commit()

                flash("Your contact has been submitted successfully!", "success")
                return redirect(url_for('contact'))

            except sqlite3.OperationalError as e:
                print(f"Database error: {e}")
                flash("There was an issue with the database. Please try again later.", "error")
                return redirect(url_for('contact'))
            finally:
                conn.close()

        else:
            flash("Error connecting to the database", "error")
            return redirect(url_for('contact'))

    else:
        conn = open_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT e_employeeID, e_name FROM employee")
                employees = cursor.fetchall()
                return render_template('contact.html', employees=employees)

            except sqlite3.OperationalError as e:
                print(f"Database error: {e}")
                flash("There was an issue fetching employee data. Please try again later.", "error")
                return render_template('contact.html', employees=[])
            finally:
                conn.close()

        else:
            flash("Error connecting to the database", "error")
            return render_template('contact.html', employees=[]) 
        
@app.route('/messages', methods=['GET', 'POST'])
def employee_messages():
    employee_id = session.get('employee_id')

    if not employee_id:
        flash("You must be logged in as an employee to view messages.", "error")
        return redirect(url_for('employee_login'))

    conn = open_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c_contactDateTime, c_reason, c_studentID, s.s_name
                FROM contact c
                JOIN student s ON c.c_studentID = s.s_studentID
                WHERE c.c_employeeID = ?
            """, (employee_id,))
            messages = cursor.fetchall()

            return render_template('empMessages.html', messages=messages)

        except sqlite3.OperationalError as e:
            print(f"Database error: {e}")
            flash("There was an issue fetching your messages. Please try again later.", "error")
            return render_template('empMessages.html', messages=[])
        finally:
            conn.close()

    else:
        flash("Error connecting to the database", "error")
        return render_template('empMessages.html', messages=[])

@app.route('/delete_message/<int:student_id>', methods=['POST'])
def delete_message(student_id):
    employee_id = session.get('employee_id')
    print(f"Deleting message for student with ID: {student_id}") 

    if not employee_id:
        flash("You must be logged in as an employee to delete messages.", "error")
        return redirect(url_for('employee_login'))

    conn = open_connection()
    if conn:
        try:
            cursor = conn.cursor()
            print(f"Executing SELECT query for student_id: {student_id}")
            cursor.execute("SELECT c_employeeID FROM contact WHERE c_studentID = ?", (student_id,))
            result = cursor.fetchone()
            
            if result:
                print(f"Message result: {result}")
                if result[0] == employee_id: 
                    print("Employee authorized. Deleting message.") 
                    cursor.execute("DELETE FROM contact WHERE c_studentID = ?", (student_id,))
                    conn.commit()
                    flash("Message deleted successfully.", "success")
                else:
                    flash("You are not authorized to delete this message.", "error")
            else:
                flash("Message not found.", "error")  

            return redirect(url_for('employee_messages'))  

        except sqlite3.OperationalError as e:
            print(f"Database error: {e}")
            flash("There was an issue deleting the message. Please try again later.", "error")
            return redirect(url_for('employee_messages'))

        except Exception as e:
            print(f"Unexpected error: {e}") 
            flash("Unexpected error occurred while deleting the message.", "error")
            return redirect(url_for('employee_messages'))

        finally:
            conn.close()

    else:
        flash("Error connecting to the database", "error")
        return redirect(url_for('employee_messages'))


if __name__ == "__main__":
    app.run(debug=True)
