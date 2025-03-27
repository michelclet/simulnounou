import streamlit as st

# Prorata pour les mois incompplets
col1, col2 = st.columns(2)
n_heures_absence = col1.text_input("Nombre d'heure d'absences", 0)
n_heures_absence = float(n_heures_absence)
n_heures_absence_maj25 = col2.text_input("Nombre d'heure d'absences majorées de 25%", 0)
n_heures_absence_maj25 = float(n_heures_absence_maj25)
calculer_button = st.button("Calculer")

if calculer_button:
    # n_heures_absence = 0
    # n_heures_absence_maj25 = 0
    salaire_horaire_net = 10.5
    n_heures_absence_total = n_heures_absence + n_heures_absence_maj25

    # Nombre d'heures de base
    n_heures_ref = 40*52/12
    n_heures_ref_maj25 = 8*52/12
    n_heures_ref_total = n_heures_ref + n_heures_ref_maj25
    salaire_ref = salaire_horaire_net*n_heures_ref/2
    salaire_ref_maj25 = salaire_horaire_net*n_heures_ref_maj25*1.25/2
    salaire_ref_net = salaire_ref + salaire_ref_maj25

    # Nombre d'heures réellement travaillées
    n_heures_reel = n_heures_ref - n_heures_absence
    n_heures_reel_maj25 = n_heures_ref_maj25 - n_heures_absence_maj25
    salaire_reel = salaire_ref_net - salaire_ref_net*n_heures_absence_total/n_heures_ref_total

    st.text("")
    st.text(f"salaire réel (€) {round(salaire_reel, 2)}")
    st.text("")
    st.text(f"salaire de référence (€) {round(salaire_ref_net, 2)}")
    st.text(f"Nombre d'heure pour la co-famille (h) {round(n_heures_reel/2)}")
    st.text(f"Nombre d'heure majorée 25% pour la co-famille (h) {round(n_heures_reel_maj25/2)}")
