from flask import Flask, render_template, session, redirect, request, url_for, logging, flash, abort

from models import User

app = Flask(__name__)
app.config.from_pyfile("settings.py")

users = {
    "cjvborges@gmail.com":
    User(name="Carlos", email="cjvborges@gmail.com", password="12345"),
    "nelsonmestevao@gmail.com":
    User(name="Nelson", email="nelsonmestevao@gmail.com", password="12345")
}


@app.route("/logout", methods=['GET'])
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route("/")
def index():
    if not "user" in session:
        return redirect(url_for('login'))

    return render_template("pages/index.html", user=session["user"])


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if email in users:
            # TODO: create error page <https://stackoverflow.com/a/21301229/8222710>
            abort(400)

        # TODO: verify if password is strong

        new_user = User(name, email, password)

        # TODO: add email validation
        users.update({email: new_user})

        session["user"] = new_user.__dict__

        return redirect(url_for('index'))

    return render_template("pages/register.html")


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if not email in users:
            # TODO: create error page <https://stackoverflow.com/a/21301229/8222710>
            abort(404)
        user = users[email]
        if password == user.password:
            session["user"] = user.__dict__
        return redirect(url_for('index'))

    return render_template("pages/login.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
