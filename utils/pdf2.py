from fpdf import FPDF
from datetime import datetime
from num2words import num2words

class FacturePDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 8, "Groupe :", ln=1)
        noms = [
            "ANAGONOU Richard",
            "BOUDZOUMOU Florent",
            "KORE Ange",
            "SISSO Lionel",
            "ODJO Immaculee"
        ]

        for nom in noms:
            self.cell(0, 7, nom, ln=1)

        self.ln(2)  # espace vertical
        self.set_font("Arial", "", 11)
        self.cell(0, 8, f"Date : {datetime.now().strftime('%d/%m/%Y')}", ln=1, align="R")

    def footer(self):
        self.set_y(-20)
        self.set_font("Arial", "I", 10)
        self.cell(0, 10, "Merci de votre confiance !", 0, 0, "C")

#function pour generer une facture en pdf en recuperant les informations dans le fichiers de la facture
def generer_facture_pdf(fichier_txt="facture.txt", fichier_pdf="facture.pdf"):
    #lire le fichier  de la facture et recuperer les fichiers nom_client, facture_num, produits, total_ttc
    with open(fichier_txt, "r") as f:
        nom_client = f.readline()
        facture_num = f.readline()
        produits = eval(f.readline())
        total_ttc = float(f.readline())
    # convertir en lettres
    montant_en_lettres = num2words(total_ttc, lang="fr").capitalize() + " francs CFA"

    pdf = FacturePDF()
    pdf.add_page()

    # Infos client
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Client : {nom_client}", ln=1)

    # Titre facture
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"FACTURE N° {facture_num}", ln=1, align="C")

    # Tableau des produits
    pdf.set_font("Arial", "B", 11)
    pdf.cell(30, 10, "Code", 1)
    pdf.cell(60, 10, "Libellé", 1)
    pdf.cell(25, 10, "PU", 1)
    pdf.cell(20, 10, "Qté", 1)
    pdf.cell(35, 10, "Total HT", 1, ln=1)

    pdf.set_font("Arial", "", 11)
    for code, libelle, pu, quantite, total_ht in produits:
        pdf.cell(30, 10, code, 1)
        pdf.cell(60, 10, libelle, 1)
        pdf.cell(25, 10, f"{pu:.2f}", 1)
        pdf.cell(20, 10, str(quantite), 1)
        pdf.cell(35, 10, f"{total_ht:.2f}", 1, ln=1)

    # Total TTC
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Total TTC : {total_ttc:.2f} FCFA", ln=1, align="R")

    # Montant en lettres
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 10, f"Arrêtée, la présente facture à la somme de : {montant_en_lettres}")

    pdf.output(fichier_pdf)
    print(f"La facture a été générée avec succès : {fichier_pdf}")


#produits = [
   # ("P001", "Clavier Azerty", 7500, 2, 15000),
   # ("P005", "Souris optique", 3000, 1, 3000)
#]

#generer_facture_pdf(
    #nom_client="KODJO FIRMINE",
    #facture_num="000045",
    #produits=produits,
    #total_ttc=19116
#)
