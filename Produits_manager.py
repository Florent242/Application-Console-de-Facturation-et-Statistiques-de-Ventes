
import pandas as pd
import os
from data_manager import (
    lire_fichier_excel,
    DATA_PATH,
    afficher_produits,
    Fore,
    Style
)

def valider_code_produit(code):
    """Valide le format du code produit (6 caractères alphanumériques)"""
    return len(code) == 6 and code.isalnum()

def code_produit_existe(code, df_produits):
    """Vérifie si un code produit existe déjà"""
    return code in df_produits['code_produit'].values

def saisir_prix_unitaire():
    """Gère la saisie sécurisée du prix"""
    while True:
        try:
            prix = float(input(Fore.CYAN + "Prix unitaire[{}FCFA]: " + Style.RESET_ALL))
            if prix <= 0:
                print(Fore.RED + "Le prix doit être positif")
            else:
                return round(prix, 2)
        except ValueError:
            print(Fore.RED + "Veuillez entrer un nombre valide")

def ajouter_produit():
    """Fonction principale pour ajouter un nouveau produit (intégrée avec Ange)"""
    print(Fore.YELLOW + "\n=== AJOUT D'UN NOUVEAU PRODUIT ===")
    
    # Chargement via la fonction du Membre 1
    df_produits = lire_fichier_excel('Produits.xlsx')
    if df_produits is None:
        print(Fore.RED + "ERREUR : Impossible de charger les produits")
        return

    # Validation du code produit
    while True:
        code = input(Fore.CYAN + "Code produit (6 caractères alphanum.) : " + Style.RESET_ALL).strip().upper()
        if not valider_code_produit(code):
            print(Fore.RED + "Format invalide : code de 6 caractères (chiffres/lettres)")
        elif code_produit_existe(code, df_produits):
            print(Fore.RED + "ERREUR : Ce code existe déjà")
        else:
            break

    # Saisie des autres informations
    libelle = input(Fore.CYAN + "Libellé du produit : " + Style.RESET_ALL).strip()
    prix = saisir_prix_unitaire()

    # Création du nouveau produit
    nouveau_produit = pd.DataFrame([{
        'code_produit': code,
        'libelle': libelle,
        'prix_unitaire': prix
    }])

    # Fusion et sauvegarde
    try:
        df_final = pd.concat([df_produits, nouveau_produit], ignore_index=True)
        df_final.to_excel(os.path.join(DATA_PATH, 'Produits.xlsx'), index=False)
        
        print(Fore.GREEN + f"\nSUCCÈS : Produit '{libelle}' ajouté (Code: {code})")
        afficher_produits()  # Utilisation de la fonction du Membre 1
        
    except Exception as e:
        print(Fore.RED + f"\nERREUR lors de l'enregistrement : {str(e)}")

def menu_gestion_produits():
    """Menu spécifique pour le Membre 3"""
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
            print(Fore.RED + "Option invalide")

if __name__ == "__main__":
    # Test 
    print(Fore.BLUE + "\n=== TEST DU MODULE PRODUCT_MANAGER ===")
    print(f"Chemin des données : {DATA_PATH}")
    menu_gestion_produits()
