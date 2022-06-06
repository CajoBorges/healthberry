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

# servidor com raspberry

app = Flask(__name__)
app.config.from_pyfile("settings.py")


@app.errorhandler(404)
def erro(error):
    return render_template('pages/error.html'), 404


@app.errorhandler(400)
def error(error):
    return render_template('pages/error.html'), 400


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
    if not "user" in session:
        return redirect(url_for('login'))
    return render_template("pages/dashboard/dashboard.html")


@app.route("/ritmo-cardiaco")
def ritmoCardiaco():
    if not "user" in session:
        return redirect(url_for('login'))
    return render_template("pages/dashboard/rcardiaco.html")


@app.route("/tensao-arterial")
def tensaoArterial():
    if not "user" in session:
        return redirect(url_for('login'))
    return render_template("pages/dashboard/tensao_arterial.html")


@app.route("/km-passos")
def kmPassos():
    if not "user" in session:
        return redirect(url_for('login'))
    return render_template("pages/dashboard/km_passos.html")


@app.route("/sono")
def sono():
    if not "user" in session:
        return redirect(url_for('login'))
    return render_template("pages/dashboard/sono.html")


@app.route("/altura-peso")
def alturaPeso():
    if not "user" in session:
        return redirect(url_for('login'))
    return render_template("pages/dashboard/altura_peso.html")


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
        print(password)
        if re.match("^\S*(?=\S{8,})(?=\S*\d)(?=\S*[A-Z])(?=\S*[a-z])(?=\S*[!@#$%^&*? ])\S*$", password) != None:
            if re.match("(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*)@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])", email) != None:
                if email in users:
                    abort(400)
                conn.commit()
                c.close()
                new_user = User(name, email, password)
                conn = sqlite3.connect('healthberry.db')
                c = conn.cursor()

                c.execute('INSERT INTO users(name, email, password) VALUES (?,?, ?)',
                          (name, email, password))
                conn.commit()
                c.close()

                return redirect(url_for('dashboard'))
            else:
                flash('Email inválido.')
                return redirect(url_for('register'))
        else:
            flash('Password Fraca. Utilize pelo menos 8 carateres de letras maiúsculas, minúsculas, números e carateres especiais.')
            return redirect(url_for('register'))

    return render_template("pages/register.html")


@app.route("/login", methods=['POST', 'GET'])
def login():
    error = ''
    if request.method == 'POST':
        conn = sqlite3.connect('healthberry.db')
        c = conn.cursor()
        email = request.form['email']
        password = request.form['password']
        c.execute("SELECT * FROM users WHERE email=?", (email,))
        user = c.fetchone()
        c.close()
        print(user)
        if password == user[3]:
            session["user"] = {"email": user[2], "name": user[1]}
            return redirect(url_for('dashboard'))

        else:
            flash('Password errada')
            return redirect(url_for('login'))

    return render_template("pages/login.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
