# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for
from pm import PasswordManager
from flask import jsonify


app = Flask(__name__)

password_manager = PasswordManager()

# Utilisez une liste pour stocker temporairement les informations de connexion (à des fins de démonstration)
users = [{'username': 'admin', 'password': 'admin', 'entries': []}]

# Utilisez une autre liste pour stocker les données du fichier entries.txt
db = []
def update_db():
    with open('entries.txt', 'r') as file:
        for line in file:
            site, username, password = line.strip().split(':')
            db.append({'site': site, 'username': username, 'password': password_manager.decrypt_password(password)})
        print(db)

update_db()


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

@app.route('/edit/<site>', methods=['GET', 'POST'])
def edit_entry(site):

    return redirect(url_for('dashboard', username='admin'))

@app.route('/delete_entry/<string:site>')
def delete_entry(site):
    password_manager.delete_pass(site)
    index_to_remove = None
    for i, entry in enumerate(db):
        if entry['site'] == site:
            index_to_remove = i
            break

    # Supprimez l'entrée de db si elle a été trouvée
    if index_to_remove is not None:
        db.pop(index_to_remove)
    update_db()
    return redirect(url_for('dashboard', username='admin'))



@app.route('/dashboard/<username>')
def dashboard(username):
    update_db()
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
