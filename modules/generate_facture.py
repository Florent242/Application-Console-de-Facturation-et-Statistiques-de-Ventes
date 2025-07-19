import pandas as pd
import os
from modules.facture import generer_facture
from modules.consultation import lire_fichier_excel

clients_df = lire_fichier_excel("Clients.xlsx") or pd.DataFrame(columns=["code_client", "nom", "contact", "IFU"])

code_client = input("Entrer le code du client : ").strip().upper()
if code_client not in clients_df["code_client"].values:
    print("Erreur : Client non trouvé.")
    exit()

is_premiere_facture = input("Est-ce la première facture de ce client ? (oui/non) : ").strip().lower() == "oui"

produits_commandes = {}
while True:
    code_produit = input("Code produit (ou taper 'fin' pour terminer) : ").strip().upper()
    if code_produit.lower() == "fin":
        break
    try:
        quantite = int(input("Quantité : "))
        if quantite <= 0:
            print("Erreur : La quantité doit être positive.")
            continue
        produits_commandes[code_produit] = produits_commandes.get(code_produit, 0) + quantite
    except ValueError:
        print("Erreur : Entrez un nombre valide pour la quantité.")

if produits_commandes:
    resultat = generer_facture(code_client, produits_commandes, is_premiere_facture)

    if resultat:
        print("\n========= FACTURE =========")
        print(f"Date : {resultat['date']}")
        print(f"Client : {resultat['nom_client']} ({code_client})")
        print("-----------------------------")
        for ligne in resultat['lignes']:
            print(f"{ligne[1]} ({ligne[0]}) - {ligne[2]} x {ligne[3]} = {ligne[4]} F")
        print("-----------------------------")
        print(f"Total HT : {resultat['total_ht']} F")
        if resultat['remise'] > 0:
            print(f"Remise ({resultat['taux_remise']}%) : -{resultat['remise']} F")
        print(f"TVA (18%) : {resultat['tva']} F")
        print(f"TOTAL TTC : {resultat['total_ttc']} F")
        print("=============================")
else:
    print("Aucun produit ajouté.")