from colorama import Fore
import pandas as pd
import os

def ajouter_client(donnees, src):
    try:
        if not donnees_sont_valides(donnees):
            print("Erreur : Les données du client ne sont pas valides.")
            return None
        df = pd.read_excel(src) if os.path.exists(src) else pd.DataFrame(columns=["code_client", "nom", "contact", "IFU"])
        df = pd.concat([df, pd.DataFrame([donnees])], ignore_index=True)
        df.to_excel(src, index=False)
        return donnees["code_client"]
    except Exception as e:
        print(f"Erreur lors de l'ajout du client : {e}")
        return None

def trouver_client_par_code(code, src) :
    df = pd.read_excel(src)
    return df[ df["code_client"] == code ]

def generer_code_client(src):
    try:
        df = pd.read_excel(src) if os.path.exists(src) else pd.DataFrame()
        dernier_id = len(df) + 1
        code = f"C{dernier_id:05d}"
        return code
    except Exception as e:
        print(f"Erreur lors de la génération du code client : {e}")
        return None

def donnees_sont_valides(donnees):
    try:
        df = pd.DataFrame([donnees])
        validations = {
            "code_client": df["code_client"].str.match(r'^[A-Z]\d{5}$', na=False), 
            "nom": df["nom"].str.match(r'^[A-Za-zÀ-ÿ\s]+$', na=False),
            "contact": df["contact"].str.match(r'^\d+$', na=False),
            "IFU": df.get("IFU", pd.Series([None])).apply(lambda x: pd.isna(x) or (isinstance(x, str) and x.isdigit() and len(x) == 13))
        }
        if not validations["code_client"].iloc[0]:
            print(Fore.RED + "Erreur : Le code client doit être au format C suivi de 5 chiffres (ex. C00001).")
        all_valid = pd.concat(validations, axis=1).all(axis=1)
        return all_valid.all()
    except Exception as e:
        print(f"Erreur lors de la validation des données : {e}")
        return False

def verifier_code_client(code, src):
    return trouver_client_par_code(code, src) is not None