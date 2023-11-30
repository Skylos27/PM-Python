# -*- coding: utf-8 -*-
from cryptography.fernet import Fernet

class PasswordManager:
    def __init__(self):
        self.key = "2K3lubeoYVHOWNh5SJdqekKeAf40OA-mevTFIKATD7k=%"
        self.password_file = "./entries.txt"
        self.password_dict = {}
        self.login_dict = {}
    
    def check_site(self, site1):
        """
        Vérifie si le site existe déjà dans le fichier

        :param site1: site à vérifier
        :type site1: str
        :return: True si le site existe déjà, False sinon
        :rtype: bool
        """
        existing = False
        with open("./entries.txt",'r') as f:
            for line in f:
                site,login,enc = line.split(":")
                if site1 == site:
                    existing = True
        return existing
                
    def create_key(self,path):
        """
        Crée une clé et l'écrit dans un fichier
        
        :param path: chemin du fichier où écrire la clé
        :type path: str
        :return: None
        """
        self.key = Fernet.generate_key()
        with open(path,'wb') as f:
            f.write(self.key)
        print(self.key)

    def load_key(self, path):
        """
        Charge une clé depuis un fichier

        :param path: chemin du fichier où lire la clé
        :type path: str
        :return: None
        """
        with open(path,'rb') as f:
            self.key = f.read()

    def decrypt_password(self, encrypted_password):
        """
        Déchiffre un mot de passe

        :param encrypted_password: mot de passe chiffré
        :type encrypted_password: str
        :return: mot de passe déchiffré
        :rtype: str
        """
        key = "2K3lubeoYVHOWNh5SJdqekKeAf40OA-mevTFIKATD7k=%"
        decrypted_password = Fernet(key).decrypt(encrypted_password.encode()).decode()
        return decrypted_password

    def encrypt_password(self, encrypted_password):
        """
        Chiffre un mot de passe
        
        :param encrypted_password: mot de passe à chiffrer
        :type encrypted_password: str
        :return: mot de passe chiffré
        :rtype: str
        """
        encrypted = Fernet(self.key).encrypt(encrypted_password.encode())
        return encrypted


    def list_sites(self, path = "./entries.txt"):
        """
        Affiche la liste des sites enregistrés

        :param path: chemin du fichier où lire les sites
        :type path: str
        :return: None
        """
        with open(path,'r') as f:
            for line in f:
                site,login, encrypted = line.split(":")
                print(site + "\n")

    def load_pass(self,path):
        """
        Charge les mots de passe depuis un fichier

        :param path: chemin du fichier où lire les mots de passe
        :type path: str
        :return: None
        """
        self.password_file = path
        with open(path,'r') as f:
            for line in f:
                site,login, encrypted = line.split(":")
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()
                self.login_dict[site] = login

    def add_password(self, site, login, password):
        """
        Ajoute un mot de passe à la liste
        
        :param site: site du mot de passe
        :type site: str
        :param login: login du site
        :type login: str
        :param password: mot de passe du site
        :type password: str
        :return: None
        """
        self.password_dict[site] = password
        self.login_dict[site] = login
        if self.check_site(site):
            print("Ce compte existe déjà")
            return
        if self.password_file != None:
            with open(self.password_file,"a+") as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + login + ":" + encrypted.decode() + "\n")

    def get_pass(self,site):
        """
        Retourne le mot de passe d'un site
        
        :param site: site dont on veut le mot de passe
        :type site: str
        :return: mot de passe du site
        :rtype: str
        """
        if self.check_site(site) == False:
            print("Ce site n'existe pas")
            return
        return self.password_dict[site]
    
    def get_login(self,site):
        """
        Retourne le login d'un site

        :param site: site dont on veut le login
        :type site: str
        :return: login du site
        :rtype: str
        """
        if self.check_site(site) == False:
            print("Ce site n'existe pas")
            return
        return self.login_dict[site]
    
    def delete_pass(self,site):
        """
        Supprime un mot de passe

        :param site: site dont on veut supprimer le mot de passe
        :type site: str
        :return: None
        """
        # Ouvre le fichier en mode lecture seule et récupère toutes les lignes
        with open('./entries.txt', 'r') as file:
            lines = file.readlines()
        # Ouvre le fichier en mode écriture et supprime le contenu
        with open('./entries.txt', 'w') as file:
            # Parcours toutes les lignes du fichier et supprime la ligne si le site est présent
            for line in lines:
                if site not in line:
                    file.write(line)
