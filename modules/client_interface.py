import pandas as pd

def ajouter_client(donnees, src):
    """Ajoute un client au fichier Excel après validation."""
    if not donnees_sont_valides([donnees]):
        raise ValueError("Données client invalides. Vérifiez le format du code (ex. A123), nom (alphabétique), contact (numérique), IFU (13 chiffres).")
    
    df = pd.read_excel(src)
    if donnees["code_client"] in df["code_client"].values:
        raise ValueError("Code client déjà existant.")
    
    new_client = pd.DataFrame([donnees])
    df = pd.concat([df, new_client], ignore_index=True)
    df.to_excel(src, index=False)

def trouver_client_par_code(code, src):
    """Retourne les données du client correspondant au code."""
    df = pd.read_excel(src)
    result = df[df["code_client"] == code]
    if result.empty:
        raise ValueError("Client non trouvé.")
    return result

def donnees_sont_valides(donnees):
    """Valide les données d'un client."""
    df = pd.DataFrame(donnees)
    
    validations = {
        "code_client": df["code_client"].str.match(r'^[A-Z]\d{3}$', na=False),
        "nom": df["nom"].str.match(r'^[A-Za-zÀ-ÿ\s]+$', na=False),
        "contact": df["contact"].str.match(r'^\d+$', na=False),
        "IFU": df["IFU"].str.match(r'^\d{13}$', na=False)
    }
    
    all_valid = pd.concat(validations, axis=1).all(axis=1)
    return all_valid.all()

def verifier_code_client(code, src):
    """Vérifie si le code client existe."""
    df = pd.read_excel(src)
    return not df[df["code_client"] == code].empty