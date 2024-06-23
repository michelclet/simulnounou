import math
import pandas as pd
import streamlit as st


def brut2net(brut):
    return brut * (1 - 21.88025/100)


# INPUTS
c1_input, c2_input, c3_input, c4_input = st.columns(4)
part_garde = c1_input.number_input("Part de garde", value=50, min_value=0, max_value=100)

salaire_brut_heure = c2_input.number_input("Salaire brut / heure", value=12.75)
salaire_net_heure = brut2net(salaire_brut_heure)
# salaire_net_heure = math.ceil(salaire_net_heure * 100)/100
c2_input.text(f"net / heure: {math.ceil(salaire_net_heure * 100)/100} €")

st.write("")
n_heure_hebdo = c3_input.number_input("Heures / semaine", value=48, min_value=0, max_value=50)

part_couple = c4_input.number_input("Répartition dans le couple", value=50, min_value=0, max_value=100)
c4_input.text(f"{part_couple}/{100-part_couple}")

# COMPUTE
part_couple /= 100
part_garde /= 100
part_garde = round(part_garde, 2)
part_restant = 1 - part_garde
part_restant = round(part_restant, 2)

n_heure_mois = math.ceil(n_heure_hebdo*52/12)

n_heure_hebdo_maj_25 = 0
n_heure_hebdo_maj_50 = 0
n_heure_mois_maj_25 = 0
n_heure_mois_maj_50 = 0

seuil_heure_maj_25 = 40
seuil_heure_maj_50 = 48
seuil_heure_max = 50

n_heure_hebdo_no_maj = min(n_heure_hebdo, seuil_heure_maj_25)
n_heure_mois_no_maj = math.ceil(n_heure_hebdo_no_maj*52/12)

if n_heure_hebdo > seuil_heure_maj_25:
    n_heure_hebdo_maj_25 = n_heure_hebdo - seuil_heure_maj_25
    n_heure_hebdo_maj_25 = min(n_heure_hebdo_maj_25, seuil_heure_maj_50 - seuil_heure_maj_25)
    n_heure_mois_maj_25 = math.ceil(n_heure_hebdo_maj_25*52/12)

if n_heure_hebdo > seuil_heure_maj_50:
    n_heure_hebdo_maj_50 = n_heure_hebdo - seuil_heure_maj_50    
    n_heure_mois_maj_50 = math.ceil(n_heure_hebdo_maj_50*52/12)
if n_heure_hebdo > seuil_heure_max:
    st.error("Le nombre d'heure effectives par semaine ne peut pas dépasser 50")
    st.stop()


# Salaires brut et net
salaire_brut_mois = salaire_brut_heure * (
    math.ceil(n_heure_mois_no_maj*part_garde)
    + math.ceil(n_heure_mois_maj_25*part_garde)*1.25
    + math.ceil(n_heure_mois_maj_50*part_garde)*1.5
    )

salaire_brut_mois_restant = salaire_brut_heure * (
    math.ceil(n_heure_mois_no_maj*part_restant)
    + math.ceil(n_heure_mois_maj_25*part_restant)*1.25
    + math.ceil(n_heure_mois_maj_50*part_restant)*1.5
    )

salaire_net_mois = brut2net(salaire_brut_mois)
salaire_net_mois_restant = brut2net(salaire_brut_mois_restant)

# Salaire versé
navigo = 43.20
exo_cot_heure_sup = 32.45
salaire_net_mois_verse = salaire_net_mois + navigo + exo_cot_heure_sup
salaire_net_mois_verse_restant = salaire_net_mois_restant + navigo + exo_cot_heure_sup


# Cotisations sociales
cotisations_sociales = 66/100 * salaire_brut_mois # 921.14
charges = cotisations_sociales

# Aides
# Prise en charge CAF des cot.sociales à 50 % plafonnée
aide_caf = .5 * cotisations_sociales
# Montant de la déduction forfaitaire
deduction_forfaitaire = 194.00
# Versement mensuel CMG remunération
aide_cmg = 200.22
# Allocation AMGED Asnières versée
aide_amged_asnieres = 0
# Allocation AMGED Courbevoie versée
aide_amged_courbevoie = 0
# Allocation BEBEDOM
aide_bebedom = 0
aides = aide_caf + deduction_forfaitaire + aide_cmg + aide_amged_asnieres + aide_amged_courbevoie + aide_bebedom

# Dépenses
depenses_mois = salaire_net_mois_verse + charges - aides - exo_cot_heure_sup

# Total dépenses annuelles
depenses_an = depenses_mois*12

# Montant du crédit d'impôt: 50% plaffoné à 12k€ (15k€ la 1ère année) pour 1 enfant
seuil_credit_impot = 12000
montant_credit = 50/100 * min(depenses_an, seuil_credit_impot)
depenses_apres_credit = depenses_an - montant_credit

depenses_apres_seuil = 0
if depenses_an > seuil_credit_impot:
    depenses_apres_seuil = depenses_an - seuil_credit_impot

# Summary heures
columns = ["Co-Famille 1 (nous)", "Co-Famille 2", "Auxilaire"]
data = {
    "Nombre d'heures non majorées": [
        math.ceil(n_heure_mois_no_maj*part_garde),
        math.ceil(n_heure_mois_no_maj*part_restant),
        n_heure_mois_no_maj,
        ],
    "Nombre d'heures supplémentaires majorées 25%": [
        math.ceil(n_heure_mois_maj_25*part_garde),
        math.ceil(n_heure_mois_maj_25*part_restant),
        n_heure_mois_maj_25
        ],
    "Nombre d'heures supplémentaires majorées 50%": [
        math.ceil(n_heure_mois_maj_50*part_garde),
        math.ceil(n_heure_mois_maj_50*part_restant),
        n_heure_mois_maj_50
        ],
    }
df_heures = pd.DataFrame.from_dict(data, orient='index', columns=columns)

# Summary salaires
columns = ["Co-Famille 1 (nous)", "Co-Famille 2", "Auxilaire"]
data = {
    "Salaire brut (€)": [
        round(salaire_brut_mois, 2),
        round(salaire_brut_mois_restant, 2),
        round(salaire_brut_mois + salaire_brut_mois_restant, 2)
        ],
    "Montant net (€)": [
        round(salaire_net_mois, 2),
        round(salaire_net_mois_restant, 2),
        round(salaire_net_mois + salaire_net_mois_restant, 2)
        ],
    "+ 50% du prix du titre de transport (€)": [
        round(navigo, 2),
        round(navigo, 2),
        round(navigo*2, 2)
        ],
    (f"Salaire net versé (dont exo cot heures sup {exo_cot_heure_sup}€ (€)"): [
        round(salaire_net_mois_verse, 2),
        round(salaire_net_mois_verse_restant, 2),
        round(salaire_net_mois_verse + salaire_net_mois_verse_restant, 2)
        ],
    }
df_salaires = pd.DataFrame.from_dict(data, orient='index', columns=columns)

# Summary dépenses et impots
columns = ["Mensuel", "Annuel"]
data = {
    "Dépense effective après charges sociales (€)": [
        round(depenses_mois, 2),
        round(depenses_an, 2)
        ],
    (f"Dépenses effective part {int(100*part_couple)}% couple (€)"): [
        round(part_couple*depenses_mois, 2),
        round(part_couple*depenses_an, 2)
        ],
    (f"Dépenses effective part {int(100-100*part_couple)}% couple (€)"): [
        round((1-part_couple)*depenses_mois, 2),
        round((1-part_couple)*depenses_an, 2)
        ],
    "Montant du crédit d'impôt (€)": [
        round((montant_credit)/12, 2),
        round((montant_credit), 2)
        ],
    "Dépenses mensuelle réelles après crédit (€)": [
        round(depenses_apres_credit/12, 2),
        round(depenses_apres_credit, 2)
        ],
    (f"Dépenses mensuelle réelles part {int(100*part_couple)}% couple (€)"): [
        round(part_couple*depenses_apres_credit/12, 2),
        round(part_couple*depenses_apres_credit, 2)
        ],
    (f"Dépenses mensuelle réelles part {int(100-100*part_couple)}% couple (€)"): [
        round((1-part_couple)*depenses_apres_credit/12, 2),
        round((1-part_couple)*depenses_apres_credit, 2)
        ]
    }
df_impots = pd.DataFrame.from_dict(data, orient='index', columns=columns)

# --------
# DISPLAY
# --------

# --- HOURS
c1_hour, c2_hour, c3_hour, c4_hour = st.columns([7, 3, 2, 4])
c1_hour.text("Nombre d'heures non majorées")
c2_hour.text(f"{n_heure_hebdo_no_maj}/semaine")

c1_hour.text("Nombre d'heures supp majorées 25%")
c2_hour.text(f"{n_heure_hebdo_maj_25}/semaine")

c1_hour.text("Nombre d'heures supp majorées 50%")
c2_hour.text(f"{n_heure_hebdo_maj_50}/semaine")
st.write("---")

# --- Summary heures
st.subheader("Heure travaillées mensuelless")
st.dataframe(df_heures, use_container_width=True)

# --- Summary salaires
st.subheader("Salaires mensuels")
st.dataframe(df_salaires, use_container_width=True)

# Summary dépenses et impots
st.subheader("Dépenses totales pour Co-famille 1 (nous)")
st.dataframe(df_impots, use_container_width=True)
