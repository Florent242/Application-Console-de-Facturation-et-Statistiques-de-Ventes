import sys
import os
import time
import re
from colorama import init, Fore, Style
from modules import index  
from utils.effacer import effacer_console
from utils.pdf import generer_facture_pdf
from modules.consultation import afficher_clients, afficher_produits, afficher_cartes
from modules.index import sous_menu_consultation
from modules.client import ajouter_client, verifier_code_client, generer_code_client, donnees_sont_valides
from modules.produits_manager import ajouter_produit
from modules.facture import generer_facture

init(autoreset=True)

def afficher_titre(titre):
    print(Fore.CYAN + Style.BRIGHT + "="*50)
    print(Fore.CYAN + Style.BRIGHT + f"{titre.center(27)}")
    print(Fore.CYAN + Style.BRIGHT + "="*50)

def menu():
    while True:
        effacer_console()
        afficher_titre("APPLICATION DE FACTURATION")

        print(Fore.GREEN + "1." + Fore.WHITE + " Consulter un fichier")
        print(Fore.GREEN + "2." + Fore.WHITE + " Générer une facture")
        print(Fore.GREEN + "3." + Fore.WHITE + " Ajouter un produit")
        print(Fore.RED + "0." + Fore.WHITE + " Quitter l'application")

        choix = input(Fore.YELLOW + "\nQue voulez-vous faire ? " + Fore.WHITE)

        if choix == "1":
            index.sous_menu_consultation()
            print(Fore.CYAN + "\nRetour au menu principal dans 1 seconde...")
            time.sleep(1)

        elif choix == "2":
            while True:
                print(Fore.YELLOW + "Est-ce un nouveau client ? (oui/non) : ", end="")
                reponse = input().strip().lower()
                if reponse == "oui":
                    while True:
                        nom_client = input(Fore.YELLOW + "Entrez le nom du client : ").strip()
                        if not nom_client:
                            print(Fore.RED + "Erreur : le nom ne peut pas être vide.")
                        elif not re.match(r'^[A-Za-zÀ-ÿ\s]+$', nom_client):
                            print(Fore.RED + "Erreur : le nom doit contenir uniquement des lettres et des espaces.")
                        else:
                            break

                    while True:
                        contact_client = input(Fore.YELLOW + "Entrez le contact du client : ").strip()
                        if not contact_client:
                            print(Fore.RED + "Erreur : le contact ne peut pas être vide.")
                        elif not contact_client.isdigit():
                            print(Fore.RED + "Erreur : le contact doit contenir uniquement des chiffres.")
                        else:
                            break

                    while True:
                        ifu_client = input(Fore.YELLOW + "Entrez l'IFU du client (13 chiffres) : ").strip()
                        if not ifu_client or (ifu_client.isdigit() and len(ifu_client) == 13):
                            break
                        print(Fore.RED + "Erreur : l'IFU doit avoir 13 chiffres.")

                    code_client = generer_code_client("data/Clients.xlsx")
                    if not code_client:
                        print(Fore.RED + "Erreur : impossible de générer un code client.")
                        time.sleep(1)
                        continue

                    donnee = {
                        "code_client": code_client,
                        "nom": nom_client,
                        "contact": contact_client,
                        "IFU": ifu_client if ifu_client else None
                    }

                    if not donnees_sont_valides(donnee):
                        print(Fore.RED + "\nLes informations fournies ne sont pas correctes !")
                        time.sleep(1)
                        continue

                    code_client_added = ajouter_client(donnee, "data/Clients.xlsx")
                    if not code_client_added:
                        print(Fore.RED + "Erreur lors de l'ajout du client.")
                        time.sleep(1)
                        continue
                    print(Fore.GREEN + f"Le client a été ajouté avec le code {code_client_added}.")
                    code_client = code_client_added
                    is_premiere_facture = input(Fore.YELLOW + "Est-ce la première facture de ce client ? (oui/non) : ").strip().lower() == "oui"
                elif reponse == "non":
                    afficher_clients()
                    code_client = input(Fore.YELLOW + "Entrez le code du client : ").strip().upper()
                    if not verifier_code_client(code_client, "data/Clients.xlsx"):
                        print(Fore.RED + "Le code du client est invalide.")
                        time.sleep(1)
                        continue
                    is_premiere_facture = input(Fore.YELLOW + "Est-ce la première facture de ce client ? (oui/non) : ").strip().lower() == "oui"
                else:
                    print(Fore.RED + "Réponse non conforme. Veuillez répondre par 'oui' ou 'non'.")
                    time.sleep(1)
                    continue
                break

            produits_commandes = []
            while True:
                afficher_produits()
                code_produit = input("Code du produit (ou 'q' pour terminer) : ").strip().upper()
                if code_produit.lower() == 'q':
                    break

                quantite_str = input("Quantité : ").strip()
                if not quantite_str.isdigit():
                    print(Fore.RED + "Quantité invalide. Entrez un nombre entier positif.")
                    continue

                quantite = int(quantite_str)
                produits_commandes.append({"code_produit": code_produit, "quantite": quantite})

            if len(produits_commandes) == 0:
                print(Fore.RED + "Aucun produit saisi. Facture annulée.")
            else:
                produits_commandes_dict = {item["code_produit"]: item["quantite"] for item in produits_commandes}
                facture_data = generer_facture(code_client, produits_commandes_dict, is_premiere_facture)
                if facture_data:
                    generer_facture_pdf(
                        nom_client=facture_data["nom_client"],
                        facture_num=facture_data["numero_facture"],
                        lignes=facture_data["lignes"],
                        total_ht=facture_data["total_ht"],
                        remise=facture_data["remise"],
                        tva=facture_data["tva"],
                        total_ttc=facture_data["total_ttc"]
                    )
                else:
                    print(Fore.RED + "Erreur lors de la génération de la facture.")

            input(Fore.GREEN + "\nAppuyez sur Entrée pour revenir au menu...")

        elif choix == "3":
            try:
                ajouter_produit()
            except Exception as e:
                print(Fore.RED + f"Erreur lors de l'ajout du produit : {e}")
            input(Fore.GREEN + "\nAppuyez sur Entrée pour revenir au menu...")

        elif choix == "0":
            print(Fore.MAGENTA + "Merci d'avoir utilisé l'application. À bientôt !")
            sys.exit()

        else:
            print(Fore.RED + "Choix invalide. Veuillez entrer un chiffre entre 1 et 4.")
            time.sleep(1)

if __name__ == "__main__":
    menu()