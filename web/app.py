from flask import Flask, render_template, request, session, redirect, url_for, flash
import json


app = Flask(__name__)
app.secret_key = 'afd13e8123fcde30295536363838dcd6'


@app.route("/")
def index():
    if 'username' not in session:
        return render_template('index.html')
    else:
        return render_template('auth_index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'username' not in request.form or 'password' not in request.form:
            return 'Неверный запрос', 400

        username = request.form['username']
        password = request.form['password']

        with open('discord-bot/registered_users.json', 'r') as f:
            users = json.load(f)

        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))

        flash('Неверное имя пользователя или пароль')
    
    return render_template('login.html')

@app.route("/registration")
def registration():
    return render_template('registration.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/profile")
def profile():
    with open('discord-bot/transportations.json', 'r') as f:
        data = json.load(f)

    user_data = [item for item in data if item['user_id'] == session['username']]

    return render_template('profile.html', data=user_data)


if __name__ == "__main__":
    app.run(debug=True)
    