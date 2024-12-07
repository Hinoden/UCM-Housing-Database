from flask import Flask, render_template

app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return render_template('welcome.html')

# Student login route
@app.route("/login/student")
def student_login():
    return render_template('studentLogin.html')

# Employee login route
@app.route("/login/employee")
def employee_login():
    return render_template('employeeLogin.html')

if __name__ == "__main__":
    app.run(debug=True)
