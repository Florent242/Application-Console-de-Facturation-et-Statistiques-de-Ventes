import pandas as pd
import os
from colorama import Fore, Style
from modules.consultation import lire_fichier_excel, afficher_produits

def valider_code_produit(code):
    return len(code) == 6 and code.isalnum()

def code_produit_existe(code, df_produits):
    return code in df_produits['code_produit'].values

def saisir_prix_unitaire():
    while True:
        try:
            prix = float(input(Fore.CYAN + "Prix unitaire [FCFA]: " + Style.RESET_ALL))
            if prix <= 0:
                print(Fore.RED + "Le prix doit être positif.")
            else:
                return round(prix, 2)
        except ValueError:
            print(Fore.RED + "Veuillez entrer un nombre valide.")

def ajouter_produit():
    print(Fore.YELLOW + "\n=== AJOUT D'UN NOUVEAU PRODUIT ===")
    
    df_produits = lire_fichier_excel('Produits.xlsx')
    if df_produits is None:
        print(Fore.RED + "ERREUR : Impossible de charger les produits.")
        return

    while True:
        code = input(Fore.CYAN + "Code produit (6 caractères alphanum.) : ( ex: P00012) " + Style.RESET_ALL).strip().upper()
        if not valider_code_produit(code):
            print(Fore.RED + "On veut un code de 6 caractères (chiffres/lettres).")
        elif code_produit_existe(code, df_produits):
            print(Fore.RED + "ERREUR : Le produit est déjà dans la liste.")
        else:
            break

    libelle = input(Fore.CYAN + "Libellé du produit : " + Style.RESET_ALL).strip()
    prix = saisir_prix_unitaire()

    nouveau_produit = pd.DataFrame([{
        'code_produit': code,
        'libelle': libelle,
        'prix_unitaire': prix
    }])

    try:
        df_final = pd.concat([df_produits, nouveau_produit], ignore_index=True)
        df_final.to_excel(os.path.join('data', 'Produits.xlsx'), index=False)
        
        print(Fore.GREEN + f"\nSUCCÈS : Produit '{libelle}' ajouté (Code: {code}).")
        afficher_produits()
        
    except Exception as e:
        print(Fore.RED + f"\nERREUR lors de l'enregistrement du produit : {str(e)}")

def menu_gestion_produits():
    while True:
        print(Fore.YELLOW + "\n=== GESTION DES PRODUITS ===")
        print("1. Ajouter un produit")
        print("2. Afficher les produits")
        print(Fore.RED + "0. Retour" + Style.RESET_ALL)
        
        choix = input(Fore.BLUE + "Votre choix : " + Style.RESET_ALL)
        
        if choix == '1':
            ajouter_produit()
        elif choix == '2':
            afficher_produits()
        elif choix == '0':
            break
        else:
            print(Fore.RED + "Option invalide.")