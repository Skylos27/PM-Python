# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for
from pm import PasswordManager

app = Flask(__name__)

password_manager = PasswordManager()

# Utilisez une liste pour stocker temporairement les informations de connexion (à des fins de démonstration)
users = [{'username': 'admin', 'password': 'admin', 'entries': []}]

# Utilisez une autre liste pour stocker les données du fichier entries.txt
db = []

with open('entries.txt', 'r') as file:
    for line in file:
        site, username, password = line.strip().split(':')
        db.append({'site': site, 'username': username, 'password': password_manager.decrypt_password(password)})

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username, password)
        if user:
            return redirect(url_for('dashboard', username=username, entries=db))
        else:
            error = 'Identifiants invalides. Veuillez réessayer.'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/dashboard/<username>')
def dashboard(username):
    user = get_user_by_username(username)
    if user:
        return render_template('dashboard.html', entries=db)
    else:
        error = 'Utilisateur introuvable'
        return render_template('login.html', error=error)

@app.route('/add_entry', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        site = request.form['site']
        username = request.form['username']
        password = request.form['password']

        password_manager.add_password(site, username, password)
        db.append({'site': site, 'username': username, 'password': password})
        return redirect(url_for('dashboard', username='admin'))
    return render_template('add_entry.html')


def get_user(username, password):
    for user in users:
        if user['username'] == username and user['password'] == password:
            return user
    return None

def get_user_by_username(username):
    for user in users:
        if user['username'] == username:
            return user
    return None

if __name__ == '__main__':
    app.run(debug=True)
