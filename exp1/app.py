from flask import Flask, render_template, redirect, url_for, session, request
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os

app = Flask(__name__)
app.secret_key = 'devops_lab_2026'

# MySQL Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sahasra@24'
app.config['MYSQL_DB'] = 'mydb'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM user WHERE email=%s AND password=%s",
            (email, password)
        )

        user = cursor.fetchone()

        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']

            message = "Login Successful"
            return render_template('user.html', message=message, user=user)

        else:
            message = "Invalid Email or Password"

    return render_template('login.html', message=message)


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM user WHERE email=%s", (email,))
        account = cursor.fetchone()

        if account:
            message = "Account Already Exists"

        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = "Invalid Email Address"

        elif not name or not email or not password:
            message = "Please fill all details"

        else:
            cursor.execute(
                "INSERT INTO user(name,email,password) VALUES(%s,%s,%s)",
                (name, email, password)
            )
            mysql.connection.commit()

            message = "Registration Successful"
            return redirect(url_for('login'))

    return render_template('register.html', message=message)


@app.route('/user')
def user():
    if 'loggedin' in session:
        return render_template(
            'user.html',
            name=session['name'],
            email=session['email']
        )

    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


print("Current Working Directory:", os.getcwd())
print("App Root Path:", app.root_path)
print("Templates Folder:", app.template_folder)


if __name__ == '__main__':
    app.run(debug=True)

