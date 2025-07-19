import tkinter
import pandas
import re
from modules.client import ajouter_client, verifier_code_client, generer_code_client, donnees_sont_valides
from modules.consultation import lire_fichier_excel
from modules.facture import generer_facture
from utils.pdf import generer_facture_pdf

fenetre = tkinter.Tk()
fenetre.title("FACTURE APP")
fenetre.geometry("700x500")
fenetre.configure(bg="black")

menu = tkinter.Frame(fenetre, bg="black")
menu.pack(side="left")

droite = tkinter.Frame(fenetre, bg="black")
droite.pack(side="right")

produits_liste = []

def effacer_droite():
    for truc in droite.winfo_children():
        truc.destroy()

def montrer_clients():
    effacer_droite()
    donnees = lire_fichier_excel('Clients.xlsx')
    texte = ""
    if donnees is not None:
        texte = "CLIENTS\n-----\n"
        for i in donnees.index:
            texte += str(donnees.iloc[i]["code_client"]) + "  "
            texte += str(donnees.iloc[i]["nom"]) + "  "
            texte += str(donnees.iloc[i]["contact"]) + "  "
            texte += str(donnees.iloc[i]["IFU"]) + "\n"
    else:
        texte = "PAS D CLIENTS"
    label = tkinter.Label(droite, text=texte, fg="white", bg="black")
    label.pack()

def montrer_produits():
    effacer_droite()
    donnees = lire_fichier_excel('Produits.xlsx')
    texte = ""
    if donnees is not None:
        texte = "PRODUITS\n-----\n"
        for i in donnees.index:
            texte += str(donnees.iloc[i]["code_produit"]) + "  "
            texte += str(donnees.iloc[i]["libelle"]) + "  "
            texte += str(donnees.iloc[i]["prix_unitaire"]) + "\n"
    else:
        texte = "PAS DE PRODUITS"
    label = tkinter.Label(droite, text=texte, fg="white", bg="black")
    label.pack()

def ajout_client():
    effacer_droite()
    label1 = tkinter.Label(droite, text="NOM", fg="white", bg="black")
    label1.pack()
    nom = tkinter.Entry(droite, fg="white", bg="black")
    nom.pack()

    label2 = tkinter.Label(droite, text="CONTACTS", fg="white", bg="black")
    label2.pack(pady=10)
    contact = tkinter.Entry(droite, fg="white", bg="black")
    contact.pack()

    label3 = tkinter.Label(droite, text="IFU", fg="white", bg="black")
    label3.pack(pady=10)
    ifu = tkinter.Entry(droite, fg="white", bg="black")
    ifu.pack()

    def valider():
        n = nom.get()
        c = contact.get()
        i = ifu.get()
        if not n:
            label = tkinter.Label(droite, text="NOM VIDE", fg="white", bg="black")
            label.pack()
            return
        if not c.isdigit():
            label = tkinter.Label(droite, text="CONTACT PAS BON", fg="white", bg="black")
            label.pack()
            return
        if i and len(i) != 13:
            label = tkinter.Label(droite, text="IFU PAS 13", fg="white", bg="black")
            label.pack()
            return
        code = generer_code_client("data/Clients.xlsx")
        donnees = {"code_client": code, "nom": n, "contact": c, "IFU": i if i else None}
        if donnees_sont_valides(donnees):
            ajouter_client(donnees, "data/Clients.xlsx")
            label = tkinter.Label(droite, text="CLIENT OK", fg="white", bg="black")
            label.pack()
        else:
            label = tkinter.Label(droite, text="ERREUR", fg="white", bg="black")
            label.pack()

    bouton = tkinter.Button(droite, text="VALIDER", fg="white", bg="black", command=valider)
    bouton.pack(pady=5)

def faire_facture():
    effacer_droite()
    label1 = tkinter.Label(droite, text="CODE CLIENT", fg="white", bg="black")
    label1.pack()
    code_client = tkinter.Entry(droite, fg="white", bg="black")
    code_client.pack()

    label2 = tkinter.Label(droite, text="PREMIERE FACTURE? OUI/NON", fg="white", bg="black")
    label2.pack(pady=10)
    premiere = tkinter.Entry(droite, fg="white", bg="black")
    premiere.pack()

    def ajout_produit():
        effacer_droite()
        label3 = tkinter.Label(droite, text="CODE PRODUIT", fg="white", bg="black")
        label3.pack()
        code_prod = tkinter.Entry(droite, fg="white", bg="black")
        code_prod.pack()

        label4 = tkinter.Label(droite, text="QUANTITEES", fg="white", bg="black")
        label4.pack(pady=10)
        quantite = tkinter.Entry(droite, fg="white", bg="black")
        quantite.pack()

        def valider_produit():
            cp = code_prod.get()
            q = quantite.get()
            if q.isdigit():
                produits_liste.append({"code_produit": cp, "quantite": int(q)})
                label = tkinter.Label(droite, text="PRODUIT OK", fg="white", bg="black")
                label.pack()
                faire_facture()
            else:
                label = tkinter.Label(droite, text="QUANTITEE PAS BON", fg="white", bg="black")
                label.pack()

        bouton = tkinter.Button(droite, text="OK", fg="white", bg="black", command=valider_produit)
        bouton.pack(pady=5)
        bouton2 = tkinter.Button(droite, text="RETOUR", fg="white", bg="black", command=faire_facture)
        bouton2.pack()

    def valider_facture():
        c = code_client.get()
        p = premiere.get().lower() == "oui"
        if not verifier_code_client(c, "data/Clients.xlsx"):
            label = tkinter.Label(droite, text="CLIENT PAS BON", fg="white", bg="black")
            label.pack()
            return
        if not produits_liste:
            label = tkinter.Label(droite, text="PAS DE PRODUIT", fg="white", bg="black")
            label.pack()
            return
        prods = {item["code_produit"]: item["quantite"] for item in produits_liste}
        facture = generer_facture(c, prods, p)
        if facture:
            generer_facture_pdf(facture["nom_client"], facture["numero_facture"], facture["produits"], facture["total_ttc"])
            label = tkinter.Label(droite, text="FACTURE OK " + facture["numero_facture"], fg="white", bg="black")
            label.pack()
        else:
            label = tkinter.Label(droite, text="ERREUR FACTURE", fg="white", bg="black")
            label.pack()

    bouton = tkinter.Button(droite, text="AJOUTER PRODUIT", fg="white", bg="black", command=ajout_produit)
    bouton.pack(pady=5)
    bouton2 = tkinter.Button(droite, text="FAIRE FACTURE", fg="white", bg="black", command=valider_facture)
    bouton2.pack()

bouton1 = tkinter.Button(menu, text="CLIENTS", fg="white", bg="black", command=montrer_clients)
bouton1.pack()
bouton2 = tkinter.Button(menu, text="PRODUITS", fg="white", bg="black", command=montrer_produits)
bouton2.pack(pady=3)
bouton3 = tkinter.Button(menu, text="AJOUTER CLIENT", fg="white", bg="black", command=ajout_client)
bouton3.pack()
bouton4 = tkinter.Button(menu, text="FACTURE", fg="white", bg="black", command=faire_facture)
bouton4.pack(pady=7)
bouton5 = tkinter.Button(menu, text="QUITTER", fg="white", bg="black", command=fenetre.quit)
bouton5.pack()

fenetre.mainloop()