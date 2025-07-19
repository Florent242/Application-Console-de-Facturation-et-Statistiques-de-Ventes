from re import A
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from modules.consultation_interface import afficher_clients, afficher_produits, afficher_cartes
from modules.client_interface import ajouter_client, verifier_code_client
from modules.facture_interface import generer_facture
from utils.pdf import generer_facture_pdf
from modules.produits_manager_interface import ajouter_produit

class FacturationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GestionApp")
        self.root.geometry("800x600")
        self.create_main_menu()

    def create_main_menu(self):
        """Crée le menu principal avec les options."""
        self.clear_window()

        tk.Label(self.root, text="GestionApp", font=("Arial", 20, "bold"), fg="cyan").pack(pady=20)

        tk.Button(self.root, text="Consulter un fichier", font=("Arial", 14), command=self.consultation_menu, bg="green", fg="white").pack(pady=10)
        tk.Button(self.root, text="Générer une facture", font=("Arial", 14), command=self.facture_menu, bg="green", fg="white").pack(pady=10)
        tk.Button(self.root, text="Ajouter un produit", font=("Arial", 14), command=self.ajouter_produit_menu, bg="green", fg="white").pack(pady=10)
        tk.Button(self.root, text="Ajouter un client", font=("Arial", 14), command=self.ajouter_client_menu, bg="green", fg="white").pack(pady=10)
        tk.Button(self.root, text="Quitter", font=("Arial", 14), command=self.root.quit, bg="red", fg="white").pack(pady=10)

    def clear_window(self):
        """Efface le contenu de la fenêtre."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def consultation_menu(self):
        """Menu pour consulter les fichiers."""
        self.clear_window()

        tk.Label(self.root, text="MENU CONSULTATION", font=("Arial", 18, "bold"), fg="cyan").pack(pady=20)

        tk.Button(self.root, text="Afficher les clients", font=("Arial", 12), command=self.show_clients, bg="blue", fg="white").pack(pady=5)
        tk.Button(self.root, text="Afficher les produits", font=("Arial", 12), command=self.show_produits, bg="blue", fg="white").pack(pady=5)
        tk.Button(self.root, text="Afficher les cartes", font=("Arial", 12), command=self.show_cartes, bg="blue", fg="white").pack(pady=5)
        tk.Button(self.root, text="Retour", font=("Arial", 12), command=self.create_main_menu, bg="red", fg="white").pack(pady=5)

    def show_table(self, df, title):
        """Affiche un DataFrame dans un tableau."""
        self.clear_window()
        tk.Label(self.root, text=title, font=("Arial", 16, "bold"), fg="cyan").pack(pady=10)

        tree = ttk.Treeview(self.root)
        tree["columns"] = list(df.columns)
        tree["show"] = "headings"

        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))

        tree.pack(fill="both", expand=True, padx=10, pady=10)
        tk.Button(self.root, text="Retour", command=self.consultation_menu, bg="red", fg="white").pack(pady=10)


    def show_clients_list(self):
        """Affiche la liste des clients."""
        df = afficher_clients()
        self.show_clients_list(df, "Liste des Clients")
        tree["columns"] = list(df.columns)
        tree["show"] = "headings"

        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))

        tree.pack(fill="both", expand=True, padx=10, pady=10)



    def show_clients(self):
        """Affiche la liste des clients."""
        df = afficher_clients()
        if df.empty:
            messagebox.showerror("Erreur", "Aucun client trouvé ou fichier introuvable.")
            self.consultation_menu()
        else:
            self.show_table(df, "Liste des Clients")

    def show_produits(self):
        """Affiche la liste des produits."""
        df = afficher_produits()
        if df.empty:
            messagebox.showerror("Erreur", "Aucun produit trouvé ou fichier introuvable.")
            self.consultation_menu()
        else:
            self.show_table(df, "Liste des Produits")

    def show_cartes(self):
        """Affiche la liste des cartes de fidélité."""
        df = afficher_cartes()
        if df.empty:
            messagebox.showerror("Erreur", "Aucune carte trouvée ou fichier introuvable.")
            self.consultation_menu()
        else:
            self.show_table(df, "Liste des Cartes de Fidélité")

    def facture_menu(self):
        """Menu pour générer une facture."""
        self.clear_window()
        tk.Label(self.root, text="GÉNÉRER UNE FACTURE", font=("Arial", 18, "bold"), fg="cyan").pack(pady=20)
        self.show_clients_list()
        tk.Label(self.root, text="Code client:", font=("Arial", 12)).pack()
        code_client_entry = tk.Entry(self.root, font=("Arial", 12))
        code_client_entry.pack(pady=5)

        tk.Label(self.root, text="Produits:", font=("Arial", 12)).pack()
        produits_frame = tk.Frame(self.root)
        produits_frame.pack(fill="both", expand=True)   

        produits_commandes = []
        produits_df = pd.read_excel("data/Produits.xlsx")
        produit_var = tk.StringVar(self.root)
        quantite_entry = tk.Entry(produits_frame, font=("Arial", 12), width=10)

        def add_produit():
            
            code_produit = produit_var.get()
            quantite = quantite_entry.get()
            if not quantite.isdigit():
                messagebox.showerror("Erreur", "Quantité invalide. Entrez un nombre entier positif.")
                return
            produits_commandes.append({"code_produit": code_produit, "quantite": int(quantite)})
            quantite_entry.delete(0, tk.END)
            messagebox.showinfo("Succès", f"Produit {code_produit} ajouté avec quantité {quantite}.")

        ttk.Combobox(produits_frame, textvariable=produit_var, values=list(produits_df["code_produit"])).pack(side="left", padx=5)
        quantite_entry.pack(side="left", padx=5)
        tk.Button(produits_frame, text="Ajouter produit", command=add_produit, bg="green", fg="white").pack(side="left", padx=5)

        def generate_facture():
            code_client = code_client_entry.get().strip().upper()
            if not verifier_code_client(code_client, "data/Clients.xlsx"):
                messagebox.showerror("Erreur", "Code client invalide ou inexistant.")
                return
            if not produits_commandes:
                messagebox.showerror("Erreur", "Aucun produit sélectionné.")
                return

            facture_data = generer_facture(code_client, produits_commandes)
            if not facture_data:
                messagebox.showerror("Erreur", "Erreur lors de la génération de la facture. Vérifiez les données du client ou des produits.")
                return

            try:
                pdf_path = generer_facture_pdf(
                    nom_client=facture_data["nom_client"],
                    facture_num=facture_data["numero_facture"],
                    produits=facture_data["produits"],
                    total_ttc=facture_data["total_ttc"]
                )
                messagebox.showinfo("Succès", f"Facture générée avec succès : {pdf_path}")
                self.create_main_menu()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la génération du PDF : {e}")

        tk.Button(self.root, text="Générer la facture", command=generate_facture, bg="green", fg="white").pack(pady=10)
        tk.Button(self.root, text="Retour", command=self.create_main_menu, bg="red", fg="white").pack(pady=10)

    def ajouter_produit_menu(self):
        """Menu pour ajouter un produit."""
        self.clear_window()
        tk.Label(self.root, text="AJOUTER UN PRODUIT", font=("Arial", 18, "bold"), fg="cyan").pack(pady=20)

        tk.Label(self.root, text="Code produit:", font=("Arial", 12)).pack()
        code_entry = tk.Entry(self.root, font=("Arial", 12))
        code_entry.pack(pady=5)

        tk.Label(self.root, text="Libellé:", font=("Arial", 12)).pack()
        libelle_entry = tk.Entry(self.root, font=("Arial", 12))
        libelle_entry.pack(pady=5)

        tk.Label(self.root, text="Prix unitaire:", font=("Arial", 12)).pack()
        prix_entry = tk.Entry(self.root, font=("Arial", 12))
        prix_entry.pack(pady=5)

        def save_produit():
            try:
                produit = {
                    "code_produit": code_entry.get().strip().upper(),
                    "libelle": libelle_entry.get().strip(),
                    "prix_unitaire": float(prix_entry.get().strip())
                }
                ajouter_produit(produit)
                messagebox.showinfo("Succès", "Produit ajouté avec succès!")
                self.create_main_menu()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'ajout du produit : {e}")

        tk.Button(self.root, text="Ajouter", command=save_produit, bg="green", fg="white").pack(pady=10)
        tk.Button(self.root, text="Retour", command=self.create_main_menu, bg="red", fg="white").pack(pady=10)

    def ajouter_client_menu(self):
        """Menu pour ajouter un client."""
        self.clear_window()
        tk.Label(self.root, text="AJOUTER UN CLIENT", font=("Arial", 18, "bold"), fg="cyan").pack(pady=20)

        tk.Label(self.root, text="Code client (ex. A123):", font=("Arial", 12)).pack()
        code_entry = tk.Entry(self.root, font=("Arial", 12))
        code_entry.pack(pady=5)

        tk.Label(self.root, text="Nom:", font=("Arial", 12)).pack()
        nom_entry = tk.Entry(self.root, font=("Arial", 12))
        nom_entry.pack(pady=5)

        tk.Label(self.root, text="Contact (numérique):", font=("Arial", 12)).pack()
        contact_entry = tk.Entry(self.root, font=("Arial", 12))
        contact_entry.pack(pady=5)

        tk.Label(self.root, text="IFU (13 chiffres):", font=("Arial", 12)).pack()
        ifu_entry = tk.Entry(self.root, font=("Arial", 12))
        ifu_entry.pack(pady=5)

        def save_client():
            try:
                client = {
                    "code_client": code_entry.get().strip().upper(),
                    "nom": nom_entry.get().strip(),
                    "contact": contact_entry.get().strip(),
                    "IFU": ifu_entry.get().strip()
                }
                ajouter_client(client, "data/Clients.xlsx")
                messagebox.showinfo("Succès", "Client ajouté avec succès!")
                self.create_main_menu()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'ajout du client : {e}")

        tk.Button(self.root, text="Ajouter", command=save_client, bg="green", fg="white").pack(pady=10)
        tk.Button(self.root, text="Retour", command=self.create_main_menu, bg="red", fg="white").pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = FacturationApp(root)
    root.mainloop()