import pandas as pd
import numpy as np

np.random.seed(42)

# -----------------------------
# CLIENTS INDUSTRIELS (type Air Liquide)
# -----------------------------
n_clients = 150

industries = [
    "Steel", "Automotive", "Pharma", "Chemicals",
    "Energy", "Electronics", "Food Processing"
]

countries = ["France", "Germany", "Italy", "Spain", "Belgium"]

clients = pd.DataFrame({
    "Client_ID": [f"ALC_{str(i).zfill(4)}" for i in range(1, n_clients+1)],
    "Industry": np.random.choice(industries, n_clients),
    "Country": np.random.choice(countries, n_clients),
    "Contract_Type": np.random.choice(
        ["Long-Term", "Spot", "Framework Agreement"],
        n_clients,
        p=[0.6, 0.2, 0.2]
    )
})

# -----------------------------
# PRODUITS (gaz industriels)
# -----------------------------
products = [
    "Oxygen", "Nitrogen", "Hydrogen",
    "Argon", "CO2", "Medical Gas Mix"
]

# -----------------------------
# OPPORTUNITÉS COMMERCIALES
# -----------------------------
n_opps = 1200

stages = ["Prospect", "Qualified", "Proposal", "Negotiation", "Closed Won", "Closed Lost"]

stage_probs = [0.15, 0.20, 0.20, 0.15, 0.20, 0.10]

opportunities = pd.DataFrame({
    "Opportunity_ID": [f"OPP_{str(i).zfill(5)}" for i in range(1, n_opps+1)],
    "Client_ID": np.random.choice(clients["Client_ID"], n_opps),
    "Product": np.random.choice(products, n_opps),
    "Stage": np.random.choice(stages, n_opps, p=stage_probs),

    # contrats industriels = montants élevés
    "Contract_Value_EUR": np.random.randint(5000, 500000, n_opps),

    # probabilité de conversion réaliste CRM
    "Probability_%": np.random.randint(10, 100, n_opps),

    # cycle de vente long industriel
    "Sales_Rep": np.random.choice(["Emma", "Lucas", "Nina", "Hugo"], n_opps),

    "Date": pd.to_datetime("2023-01-01") + pd.to_timedelta(
        np.random.randint(0, 900, n_opps), unit="D"
    )
})

# -----------------------------
# REVENUE (réel uniquement si gagné)
# -----------------------------
opportunities["Revenue_EUR"] = np.where(
    opportunities["Stage"] == "Closed Won",
    opportunities["Contract_Value_EUR"],
    0
)

# -----------------------------
# AJOUT DE LOGIQUE BUSINESS (IMPORTANT)
# -----------------------------

# Gros clients industriels (effet Air Liquide)
top_clients = clients.sample(8)["Client_ID"]

opportunities.loc[
    opportunities["Client_ID"].isin(top_clients),
    "Contract_Value_EUR"
] *= 3  # contrats industriels lourds

# Pharma = plus rentable mais plus exigeant
opportunities.loc[
    opportunities["Product"] == "Medical Gas Mix",
    "Contract_Value_EUR"
] *= 2

# -----------------------------
# EXPORT
# -----------------------------
clients.to_csv("data/airliquide_clients.csv", index=False)
opportunities.to_csv("data/airliquide_opportunities.csv", index=False)

print("Dataset industriel Air Liquide-like généré dans le dossier data/ ✔️")

print("Dataset industriel Air Liquide-like généré ✔️")
