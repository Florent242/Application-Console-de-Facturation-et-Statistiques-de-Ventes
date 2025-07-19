import pandas as pd

def ajouter_client(donnees, src) :
    # Append to Excel (creates a new sheet)
    with pd.ExcelWriter(src, mode='a', engine='openpyxl', if_sheet_exists='new') as writer:
        pd.DataFrame(donnees).to_excel(writer, sheet_name="NewClients", index=False)
    return

def trouver_client_par_code(code, src) :
    df = pd.read_excel(src)
    return df[ df["code_client"] == code ]

import pandas as pd

def donnees_sont_valides(donnees):
    df = pd.DataFrame(donnees)
    
    # Validation rules
    validations = {
        "code_client": df["code_client"].str.match(r'^[A-Z]\d{3}$', na=False),
        "nom": df["nom"].str.match(r'^[A-Za-zÀ-ÿ\s]+$', na=False),  # Alphabétique + espaces/accents
        "contact": df["contact"].str.match(r'^\d+$', na=False),     # Numérique uniquement
        "IFU": df["IFU"].str.match(r'^\d{13}$', na=False)           # Exactement 13 chiffres
    }
    
    # Combine all validations
    all_valid = pd.concat(validations, axis=1).all(axis=1)
    invalid_entries = df[~all_valid]
    
    # Detailed error reporting
    if not invalid_entries.empty:
        return False
    return True

def verifier_code_client(code, src):
    df = pd.read_excel(src)
    if df[df["code_client"] == code].empty:
        return False
    return True