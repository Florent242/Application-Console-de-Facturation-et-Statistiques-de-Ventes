import pandas as pd
from datetime import datetime
import os

# ---------------------------
# Créer les fichiers Excel s'ils n'existent pas
# ---------------------------
if not os.path.exists("data/CartesReduction.xlsx"):
    pd.DataFrame(columns=["numero_carte", "code_client", "taux_reduction"]).to_excel("data/CartesReduction.xlsx", index=False)

if not os.path.exists("data/Clients.xlsx"):
    pd.DataFrame(columns=["code_client", "nom", "contact", "IFU"]).to_excel("data/Clients.xlsx", index=False)

if not os.path.exists("data/Produits.xlsx"):
    pd.DataFrame(columns=["code_produit", "libelle", "prix_unitaire"]).to_excel("data/Produits.xlsx", index=False)

# ---------------------------
# Charger les fichiers Excel
# ---------------------------
clients_df = pd.read_excel("data/Clients.xlsx")
produits_df = pd.read_excel("data/Produits.xlsx")
cartes_df = pd.read_excel("data/CartesReduction.xlsx")

# ---------------------------
# Constantes
# ---------------------------
TAUX_TVA = 0.18
SEUILS_REDUCTION = {
    100000: 10,
    50000: 5
}

# ---------------------------
# Fonctions Utilitaires
# ---------------------------
def obtenir_remise(total_ht):
    for seuil, taux in sorted(SEUILS_REDUCTION.items(), reverse=True):
        if total_ht >= seuil:
            return taux
    return 0

def client_a_une_carte(code_client):
    return code_client in cartes_df["code_client"].values

def creer_carte_reduction(code_client, total_ht):
    global cartes_df
    if not client_a_une_carte(code_client):
        taux = obtenir_remise(total_ht)
        if taux > 0:
            nouveau_numero = str(len(cartes_df) + 1).zfill(6)
            nouvelle_carte = {
                "numero_carte": nouveau_numero,
                "code_client": code_client,
                "taux_reduction": taux
            }
            cartes_df = cartes_df.append(nouvelle_carte, ignore_index=True)
            cartes_df.to_excel("data/CartesReduction.xlsx", index=False)
            print(f"Carte de réduction créée ({taux}%) pour le client {code_client}")

def generer_facture(code_client, produits_commandes, is_premiere_facture=False):
    lignes = []
    total_ht = 0

    for code_produit, quantite in produits_commandes.items():
        produit = produits_df[produits_df["code_produit"] == code_produit].iloc[0]
        libelle = produit["libelle"]
        prix_unitaire = produit["prix_unitaire"]
        total_ligne = prix_unitaire * quantite
        total_ht += total_ligne
        lignes.append([code_produit, libelle, prix_unitaire, quantite, total_ligne])

    tva = round(total_ht * TAUX_TVA, 2)

    remise = 0
    taux_remise = 0
    if not is_premiere_facture and client_a_une_carte(code_client):
        taux_remise = cartes_df[cartes_df["code_client"] == code_client]["taux_reduction"].values[0]
        remise = round(total_ht * (taux_remise / 100), 2)

    total_apres_remise = total_ht - remise
    total_ttc = round(total_apres_remise + tva, 2)

    if is_premiere_facture:
        creer_carte_reduction(code_client, total_ht)

    return {
        "lignes": lignes,
        "total_ht": total_ht,
        "remise": remise,
        "taux_remise": taux_remise,
        "tva": tva,
        "total_ttc": total_ttc,
        "date": datetime.now().strftime("%d/%m/%Y")
    }
