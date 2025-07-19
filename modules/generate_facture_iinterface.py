import pandas as pd
from modules.facture import generer_facture

# Appel de la fonction
# 1. Charger les données clients
clients_df = pd.read_excel("data/Clients.xlsx")

# 2. Saisir un client existant 
code_client = input("Entrer le code du client : ")
is_premiere_facture = input("Est-ce la première facture de ce client ? (oui/non) : ").strip().lower() == "oui"

# 3. Saisir les produits achetés
produits_commandes = {}
while True:
    code_produit = input("Code produit (ou taper 'fin' pour terminer) : ").strip()
    if code_produit.lower() == "fin":
        break
    try:
        quantite = int(input("Quantité : "))
        produits_commandes[code_produit] = produits_commandes.get(code_produit, 0) + quantite
    except ValueError:
        print("Entrer un nombre valide pour la quantité")

# 4. Générer la facture
if produits_commandes:
    resultat = generer_facture(code_client, produits_commandes, is_premiere_facture)

    print("\n========= FACTURE =========")
    print(f"Date : {resultat['date']}")
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