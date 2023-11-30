# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, jsonify
from pm import PasswordManager


app = Flask(__name__)

password_manager = PasswordManager()

# Liste pour stocker temporairement les informations de connexion
users = [{'username': 'admin', 'password': 'admin', 'entries': []}]
# Liste pour stocker les données du fichier entries.txt
db = []
def update_db():
    with open('entries.txt', 'r') as file:
        for line in file:
            site, username, password = line.strip().split(':')
            db.append({'site': site, 'username': username, 'password': password_manager.decrypt_password(password)})
        print(db)

update_db()


# Définition des différentes routes de l'application

@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Route pour la page d'accueil
    
    :return: page d'accueil
    :rtype: template
    """
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
    """
    Route pour la page d'édition d'une entrée
    
    :param site: site de l'entrée à éditer
    :type site: str
    :return: page d'édition d'une entrée
    :rtype: template
    """
    return redirect(url_for('dashboard', username='admin'))

@app.route('/delete_entry/<string:site>')
def delete_entry(site):
    """
    Route pour la suppression d'une entrée
    
    :param site: site de l'entrée à supprimer
    :type site: str
    :return: page de dashboard
    :rtype: template
    """
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
    """
    Route pour la page de dashboard
    
    :param username: nom d'utilisateur
    :type username: str
    :return: page de dashboard
    :rtype: template
    """
    update_db()
    user = get_user_by_username(username)
    if user:
        return render_template('dashboard.html', entries=db)
    else:
        error = 'Utilisateur introuvable'
        return render_template('login.html', error=error)

@app.route('/add_entry', methods=['GET', 'POST'])
def add_entry():
    """
    Route pour la page d'ajout d'une entrée
    
    :return: page d'ajout d'une entrée
    :rtype: template
    """
    if request.method == 'POST':
        site = request.form['site']
        username = request.form['username']
        password = request.form['password']

        password_manager.add_password(site, username, password)
        db.append({'site': site, 'username': username, 'password': password})
        return redirect(url_for('dashboard', username='admin'))
    return render_template('add_entry.html')

# Getter pour récupérer un utilisateur par son username et son mot de passe
def get_user(username, password):
    """
    Récupère un utilisateur par son nom d'utilisateur et son mot de passe
    
    :param username: nom d'utilisateur
    :type username: str
    :param password: mot de passe
    :type password: str
    :return: utilisateur
    :rtype: dict
    """
    for user in users:
        if user['username'] == username and user['password'] == password:
            return user
    return None

# Getter pour récupérer un utilisateur par son username et son mot de passe
def get_user_by_username(username):
    """
    Récupère un utilisateur par son nom d'utilisateur
    
    :param username: nom d'utilisateur
    :type username: str
    :return: utilisateur
    :rtype: dict
    """
    for user in users:
        if user['username'] == username:
            return user
    return None

if __name__ == '__main__':
    app.run(debug=True)
