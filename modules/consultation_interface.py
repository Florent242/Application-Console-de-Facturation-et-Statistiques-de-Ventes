import pandas as pd
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data')

def lire_fichier_excel(nom_fichier):
    chemin_complet = os.path.join(DATA_PATH, nom_fichier)
    try:
        df = pd.read_excel(chemin_complet)
        return df
    except FileNotFoundError:
        return pd.DataFrame()

def afficher_clients():
    return lire_fichier_excel('Clients.xlsx')

def afficher_produits():
    return lire_fichier_excel('Produits.xlsx')

def afficher_cartes():
    return lire_fichier_excel('CartesReduction.xlsx')