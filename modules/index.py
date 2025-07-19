from modules.consultation import afficher_clients, afficher_produits, afficher_cartes
from modules.client import ajouter_client, trouver_client_par_code, donnees_sont_valides, verifier_code_client
from colorama import init, Fore
import os
import time
import pandas as pd

# Initialiser Colorama
init(autoreset=True)

def effacer_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def sous_menu_consultation():
    while True:
        effacer_console()
        print(Fore.CYAN + "==== MENU CONSULTATION ====")
        print(Fore.GREEN + "1." + Fore.WHITE + " Afficher les clients")
        print(Fore.GREEN + "2." + Fore.WHITE + " Ajouter un client")
        print(Fore.GREEN + "3." + Fore.WHITE + " Rechercher un client")
        print(Fore.GREEN + "4." + Fore.WHITE + " Afficher les produits")
        print(Fore.GREEN + "5." + Fore.WHITE + " Afficher les cartes de fidélité")
        print(Fore.RED + "6." + Fore.WHITE + " Retour menu principal")

        choix = input(Fore.YELLOW + "\nVotre choix : ")

        if choix == "1":
            afficher_clients()
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

        elif choix == "5":
            afficher_cartes()
            input(Fore.CYAN + "\nAppuyez sur Entrée pour continuer...")

        elif choix == "6":
            break

        else:
            print(Fore.RED + "Saisie incorrecte.")
            time.sleep(2)