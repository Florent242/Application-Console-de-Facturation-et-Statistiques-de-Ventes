# fichier : pdf.py
from fpdf import FPDF
from datetime import datetime
from num2words import num2words
import os

def generer_facture_pdf(nom_client, facture_num, lignes, total_ht, remise, tva, total_ttc, fichier_pdf="facture.pdf"):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Groupe :", ln=1)
    for nom in ["ANAGONOU Richard", "BOUDZOUMOU Florent", "KORE Ange", "SISSO Lionel", "ODJO Immaculee"]:
        pdf.cell(0, 7, nom, ln=1)
    pdf.ln(2)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"Date : {datetime.now().strftime('%d/%m/%Y')}", ln=1, align="R")

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Client : {nom_client}", ln=1)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"FACTURE N° {facture_num}", ln=1, align="C")

    headers = [
        "N°", "Code", "Libellé", "P.U.", "Qté"
    ]
    col_widths = [8, 20, 40, 18, 12, 22, 18, 22, 22, 25]

    pdf.set_font("Arial", "B", 9)
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 8, header, 1, 0, "C")
    pdf.ln()

    pdf.set_font("Arial", "", 9)
    for ligne in lignes:
        valeurs = [
            ligne["numero"],
            ligne["code"],
            ligne["libelle"],
            f"{ligne['pu']:.2f}",
            ligne["quantite"],
        ]
        for i, val in enumerate(valeurs):
            pdf.cell(col_widths[i], 8, str(val), 1)
        pdf.ln()

    pdf.ln(5)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, f"Total HT      : {total_ht:.2f} FCFA", ln=1, align="R")
    pdf.cell(0, 8, f"Remise totale : {remise:.2f} FCFA", ln=1, align="R")
    pdf.cell(0, 8, f"THT remise    : {(total_ht - remise):.2f} FCFA", ln=1, align="R")
    pdf.cell(0, 8, f"TVA (18%)     : {tva:.2f} FCFA", ln=1, align="R")
    pdf.cell(0, 8, f"Total TTC     : {total_ttc:.2f} FCFA", ln=1, align="R")

    try:
        montant_en_lettres = num2words(total_ttc, lang="fr").capitalize() + " francs CFA"
    except:
        montant_en_lettres = "Montant non convertible en lettres"

    pdf.set_font("Arial", "", 11)
    pdf.ln(4)
    pdf.multi_cell(0, 10, f"Arrêtée, la présente facture à la somme de : {montant_en_lettres}")

    output_path = os.path.join("factures", f"facture_{facture_num}.pdf")
    try:
        os.makedirs("factures", exist_ok=True)
        pdf.output(output_path)
        print(f"Facture du client générée : {output_path}")
    except Exception as e:
        print(f"Enregistrement du PDF échoué : {e}")
    return output_path
