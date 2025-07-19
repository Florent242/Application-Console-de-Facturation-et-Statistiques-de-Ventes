import pandas as pd
import os
from colorama import init, Fore, Style
from modules.client import trouver_client_par_code

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data')

def lire_fichier_excel(nom_fichier):
    chemin_complet = os.path.join(DATA_PATH, nom_fichier)
    try:
        df = pd.read_excel(chemin_complet)
        return df
    except FileNotFoundError:
        print(Fore.RED + f"Erreur : fichier {nom_fichier} introuvable dans {DATA_PATH}.")
        return pd.DataFrame(columns=["code_client", "nom", "contact", "IFU"] if "Clients" in nom_fichier else
                           ["code_produit", "libelle", "prix_unitaire"] if "Produits" in nom_fichier else
                           ["numero_carte", "code_client", "taux_reduction"])
    except Exception as e:
        print(Fore.RED + f"Erreur lors de la lecture de {nom_fichier} : {str(e)}")
        return None

def afficher_clients():
    df = lire_fichier_excel('Clients.xlsx')

    if df is not None and not df.empty:
        if "IFU" in df.columns:
            df["IFU"] = df["IFU"].apply(lambda x: '{:.0f}'.format(x) if pd.notna(x) else "")
        
        print(Fore.CYAN + "\n===== Liste des clients =====")
        print(Fore.WHITE + df.to_string(index=False))
        print(Fore.CYAN + "==============================\n")
        
    return df if df is not None else pd.DataFrame(columns=["code_client", "nom", "contact", "IFU"])

def afficher_produits():
    df = lire_fichier_excel('Produits.xlsx')
    if df is not None and not df.empty:
        print(Fore.GREEN + "\n===== Liste des produits =====")
        print(Fore.WHITE + df.to_string(index=False))
        print(Fore.GREEN + "===============================\n")

def afficher_cartes():
    df = lire_fichier_excel('CartesReduction.xlsx')
    if df is not None and not df.empty:
        print(Fore.MAGENTA + "\n===== Liste des cartes de fidélité =====")
        print(Fore.WHITE + df.to_string(index=False))
        print(Fore.MAGENTA + "=========================================\n")

def rechercher_client():
    code = input(Fore.CYAN + "Entrez le code du client à rechercher : " + Style.RESET_ALL).strip().upper()
    client = trouver_client_par_code(code, os.path.join(DATA_PATH, 'Clients.xlsx'))
    if client:
        print(Fore.CYAN + "\n===== Client trouvé =====")
        print(Fore.WHITE + pd.DataFrame([client]).to_string(index=False))
        print(Fore.CYAN + "=========================\n")
    else:
        print(Fore.RED + f"Aucun client trouvé avec le code {code}.")