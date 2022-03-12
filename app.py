import database
from flask import Flask, render_template, session, redirect, request, url_for, logging, flash, abort


from models import User

import re
import sqlite3
import smtplib
import ssl
import email_verificacao

#! conn = sqlite3.connect('healthberry.db')
#! c = conn.cursor()
#! c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")


app = Flask(__name__)
app.config.from_pyfile("settings.py")


@app.errorhandler(404)
def erro(error):
    return render_template('pages/error.html'), 404


@app.errorhandler(400)
def error(error):
    return render_template('pages/error.html'), 400
    # TODO: replace number


@app.route("/logout", methods=['GET'])
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route("/")
def index():
    if not "user" in session:
        return redirect(url_for('login'))

    return render_template("pages/index.html")


@app.route("/dashboard")
def dashboard():

    return render_template("pages/dashboard.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    conn = sqlite3.connect('healthberry.db')
    c = conn.cursor()
    c.execute('SELECT * FROM USERS')
    users = c.fetchall()
    for u in users:
        print(u)
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if email in users:
            # TODO: create error page <https://stackoverflow.com/a/21301229/8222710> - feito
            abort(400)
        conn.commit()
        # TODO: verify if password is strong
        c.close()
        new_user = User(name, email, password)
        conn = sqlite3.connect('healthberry.db')
        c = conn.cursor()

        # TODO: add email validation

        c.execute('INSERT INTO users(name, email, password) VALUES (?,?, ?)',
                  (name, email, password))
        conn.commit()
        c.close()

        return redirect(url_for('index'))

    return render_template("pages/register.html")


@app.route("/login", methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        conn = sqlite3.connect('healthberry.db')
        c = conn.cursor()
        email = request.form['email']
        password = request.form['password']
        c.execute("SELECT * FROM users WHERE email=?", (email,))
        # TODO: create error page <https://stackoverflow.com/a/21301229/8222710> - feito
        user = c.fetchone()
        c.close()
        print(user)
        if password == user[3]:
            session["user"] = {"email": user[2], "name": user[1]}
            return redirect(url_for('index'))
        else:
            # TODO: Alterar para chamar notificação
            print('''<script> alert(Password Errada  %s ')
                   </script> ''' % ())
            return redirect(url_for('login'))

    return render_template("pages/login.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
