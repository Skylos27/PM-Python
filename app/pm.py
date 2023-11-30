# -*- coding: utf-8 -*-
from cryptography.fernet import Fernet

class PasswordManager:
    def __init__(self):
        self.key = "2K3lubeoYVHOWNh5SJdqekKeAf40OA-mevTFIKATD7k=%"
        self.password_file = "./entries.txt"
        self.password_dict = {}
        self.login_dict = {}
    
    def check_site(self, site1):
        existing = False
        with open("./entries.txt",'r') as f:
            for line in f:
                site,login,enc = line.split(":")
                if site1 == site:
                    existing = True
        return existing
                

    def create_key(self,path):
        self.key = Fernet.generate_key()
        with open(path,'wb') as f:
            f.write(self.key)
        print(self.key)

    def load_key(self, path):
        with open(path,'rb') as f:
            self.key = f.read()


    def list_sites(self, path = "./entries.txt"):
        with open(path,'r') as f:
            for line in f:
                site,login, encrypted = line.split(":")
                print("- " + site + "\n")

    def load_pass(self,path):
        self.password_file = path
        with open(path,'r') as f:
            for line in f:
                site,login, encrypted = line.split(":")
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()
                self.login_dict[site] = login

    def add_password(self, site, login, password):
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
        if self.check_site(site) == False:
            print("Ce site n'existe pas")
            return
        return self.password_dict[site]
    
    def get_login(self,site):
        if self.check_site(site) == False:
            print("Ce site n'existe pas")
            return
        return self.login_dict[site]
    
    def delete_pass(self,site):
        pass
