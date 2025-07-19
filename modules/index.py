from colorama import init, Fore, Style
from modules.consultation import afficher_clients, afficher_produits, afficher_cartes, lire_fichier_excel
from modules.client import ajouter_client, trouver_client_par_code, donnees_sont_valides, verifier_code_client, generer_code_client
from utils.effacer import effacer_console
import time
import pandas as pd
import re

init(autoreset=True)

def sous_menu_consultation():
    while True:
        effacer_console()
        print(Fore.CYAN + "==== MENU CONSULTATION ====")
        print(Fore.GREEN + "1." + Fore.WHITE + " Afficher les clients")
        print(Fore.GREEN + "2." + Fore.WHITE + " Afficher les produits")
        print(Fore.GREEN + "3." + Fore.WHITE + " Afficher les cartes de fidélité")
        print(Fore.RED + "0." + Fore.WHITE + " Retour menu principal")

        choix = input(Fore.YELLOW + "\nVotre choix : ")

        if choix == "1":
            afficher_clients()
            input(Fore.CYAN + "\nAppuyez sur Entrée pour continuer...")
            while True:
                nom = input(Fore.GREEN + "\nSaisir le nom du client à ajouter\n" + 
                           Fore.WHITE + "Attention, le nom doit contenir uniquement des lettres et espaces : ").strip()
                if not nom:
                    print(Fore.RED + "Erreur : le nom ne peut pas être vide.")
                elif not re.match(r'^[A-Za-zÀ-ÿ\s]+$', nom):
                    print(Fore.RED + "Erreur : le nom doit contenir uniquement des lettres et des espaces.")
                else:
                    break

            while True:
                contact = input(Fore.GREEN + "\nSaisir le contact du client à ajouter\n" + 
                               Fore.WHITE + "Attention, le contact doit contenir uniquement des chiffres : ").strip()
                if not contact:
                    print(Fore.RED + "Erreur : le contact ne peut pas être vide.")
                elif not contact.isdigit():
                    print(Fore.RED + "Erreur : le contact doit contenir uniquement des chiffres.")
                else:
                    break

            while True:
                ifu = input(Fore.GREEN + "\nSaisir l'IFU du client à ajouter (optionnel, 13 chiffres)\n" + 
                           Fore.WHITE + "Laissez vide si aucun IFU : ").strip()
                if not ifu or (ifu.isdigit() and len(ifu) == 13):
                    break
                print(Fore.RED + "Erreur : l'IFU doit être vide ou contenir exactement 13 chiffres.")

            code_client = generer_code_client("data/Clients.xlsx")
            if not code_client:
                print(Fore.RED + "\nErreur : impossible de générer un code client.")
                time.sleep(1)
                input(Fore.CYAN + "\nAppuyez sur Entrée pour continuer...")
                continue

            donnees = {
                "code_client": code_client,
                "nom": nom,
                "contact": contact,
                "IFU": ifu if ifu else None
            }

            print(Fore.YELLOW + f"\nDonnées avant validation : {donnees}")

            if not donnees_sont_valides(donnees):
                print(Fore.RED + "\nLes informations fournies ne sont pas correctes !")
                input(Fore.CYAN + "\nAppuyez sur Entrée pour continuer...")
                continue

            code_client_added = ajouter_client(donnees, "data/Clients.xlsx")
            if code_client_added:
                print(Fore.GREEN + f"\nLe client a été bien enregistré avec le code {code_client_added} !")
            else:
                print(Fore.RED + "\nErreur lors de l'enregistrement du client.")
            input(Fore.CYAN + "\nAppuyez sur Entrée pour continuer...")

            code_client = input(Fore.GREEN + "\nSaisir le code du client à rechercher : ").strip().upper()
            client = trouver_client_par_code(code_client, "data/Clients.xlsx")
            if client:
                print(Fore.CYAN + "\n===== Informations du client =====")
                print(Fore.WHITE + pd.DataFrame([client]).to_string(index=False))
                print(Fore.CYAN + "==============================\n")
            else:
                print(Fore.RED + f"\nLe client avec le code {code_client} n'existe pas !")
            time.sleep(2)
            input(Fore.CYAN + "\nAppuyez sur Entrée pour continuer...")

        elif choix == "2":
            print(Fore.GREEN + "\nSaisir le " + Fore.WHITE + "nom du client a ajouter")
            nom = input(Fore.GREEN + "\nAttention!, " + Fore.WHITE + "le nom doit contenir que les lettres : ")

            print(Fore.GREEN + "\nSaisir le " + Fore.WHITE + "contact du client a ajouter")
            contact = input(Fore.GREEN + "\nAttention!, " + Fore.WHITE + "le contact doit contenir que les nombres : ")

            print(Fore.GREEN + "\nSaisir l' " + Fore.WHITE + "IFU du client a ajouter")            
            ifu = input(Fore.GREEN + "\nAttention!, " + Fore.WHITE + "le IFU consiste des nombres de 13 chiffres : ")

            les_informations = donnees_sont_valides(
                {
                    "code_client":["C004"],
                    "nom":[nom],
                    "contact":[contact],
                    "IFU":[ifu]
                }
            )

            if not les_informations : 
                print(Fore.GREEN + "\nLes informations pourvu sont pas correctes!")
                time.sleep(2)
                sous_menu_consultation()

            else : 
                ajouter_client(
                    {
                        "code_client":["C004"],
                        "nom":[nom],
                        "contact":[contact],
                        "IFU":[ifu]
                    },
                    "data/Clients.xlsx"
                )
                print(Fore.GREEN + "\nLe client a ete bien enregistre!")
                time.sleep(2)
            break

        elif choix == "3":
            code_client = input(Fore.GREEN + "\nSaisir " + "le code du client à rechercher : ").strip().upper()
            
            if verifier_code_client(code_client, "data/Clients.xlsx") :
                donnees = trouver_client_par_code(code_client, "data/Clients.xlsx")
                print(Fore.CYAN + "\n===== Informations du client =====")
                # print( donnees["code_client"] + " " + donnees["nom"] + donnees["contact"] + donnees["IFU"] )
                print(donnees)
                input(Fore.CYAN + "\nAppuyez sur Entrée pour continuer...")
 
            else :
                print(Fore.RED + "\nLe client avec le code " + code_client + " n'existe pas!")
                time.sleep(2)
            break

        elif choix == "4":
            afficher_produits()
            input(Fore.CYAN + "\nAppuyez sur Entrée pour continuer...")

        elif choix == "3":
            afficher_cartes()
            input(Fore.CYAN + "\nAppuyez sur Entrée pour continuer...")

        elif choix == "0":
            break

        else:
            print(Fore.RED + "Saisie incorrecte.")
            time.sleep(1)
            input(Fore.CYAN + "\nAppuyez sur Entrée pour continuer...")