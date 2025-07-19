import pandas as pd

def ajouter_produit(produit):
    df = pd.read_excel("data/Produits.xlsx")
    if produit["code_produit"] in df["code_produit"].values:
        raise ValueError("Code produit déjà existant.")
    if not produit["libelle"] or not isinstance(produit["prix_unitaire"], (int, float)) or produit["prix_unitaire"] <= 0:
        raise ValueError("Données produit invalides. Vérifiez le libellé et le prix unitaire.")
    
    new_produit = pd.DataFrame([produit])
    df = pd.concat([df, new_produit], ignore_index=True)
    df.to_excel("data/Produits.xlsx", index=False)