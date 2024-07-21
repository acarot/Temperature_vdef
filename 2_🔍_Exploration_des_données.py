import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Exploration des données",
    page_icon="🔍",
    layout = 'wide'
)

st.write("## Présentation des données")

GLB = st.session_state.df_GLB
NH = st.session_state.df_NH
SH = st.session_state.df_SH
ZonAnn = st.session_state.df_ZonAnn
owid = st.session_state.df_owid
long_lat = st.session_state.df_long_lat


display = st.radio('Les datasets :', ('L-OTI GLB', 'L-OTI NH','L-OTI SH','L-OTI ZonAnn',
'OWID CO2 Data','Dataset longitude-latitude'))
if display == 'L-OTI GLB':
    st.dataframe(GLB.head())
    st.write(GLB.shape)
elif display == 'L-OTI NH':
    st.dataframe(NH.head())
    st.write(NH.shape)
elif display == 'L-OTI SH':
    st.dataframe(SH.head())
    st.write(SH.shape)
elif display == 'L-OTI ZonAnn':
    st.dataframe(ZonAnn.head())
    st.write(ZonAnn.shape)
elif display == 'OWID CO2 Data':
    st.dataframe(owid.head())
    st.write(owid.shape)
elif display == 'Dataset longitude-latitude':
    st.dataframe(long_lat.head())
    st.write(long_lat.shape)

st.header(" Dataset Owid")
st.subheader(" Analyse des valeurs nulles")

st.write("Moyenne NA : ",owid.isna().mean().mean())
st.write("Max NA : ",owid.isna().mean().max())
st.write("Min NA : ", owid.isna().mean().min())
st.write("Median NA : ", owid.isna().mean().median())
st.write("Q1 NA : ", owid.isna().mean().quantile(0.25))
st.write("Q3 NA : ", owid.isna().mean().quantile(0.75))

owid_na_rate = owid.isna().mean() #On récupère la liste des colonnes avec le taux moyen de valeur vides
#On convertit la séries en dataframe avec reset_index
owid_na_rate = owid_na_rate.reset_index()
owid_na_rate.columns = ['Column', 'NA_Rate']#On renomme les colonnes du DataFrame

st.markdown('Créons un boxplot pour visualiser la distribution du taux de NA')
fig = px.box(owid_na_rate, y='NA_Rate', points="all", hover_data = ["Column"], title='Distribution des taux de valeurs manquantes par colonne')
fig.update_layout(yaxis_title='Taux de valeurs manquantes', xaxis_title='Colonnes')
st.plotly_chart(fig)

st.markdown("Sélectionnons les champs utiles à l'analyse : 'country', 'year', 'iso_code','population', 'gdp','co2','total_ghg'")
selected_cols = ['country', 'year', 'iso_code','population', 'gdp','co2','total_ghg']
owid_filtered = owid[selected_cols]

#On compte les valeurs manquantes (Pays) par année et par variables
#On filtre sur la colonne iso_code pour ne prendre que les valeurs non vides (Afin de ne pas tenir compte des continents)
missing_values_by_year = owid_filtered.loc[owid_filtered["iso_code"].notnull()].groupby("year").agg({'country': 'count',
                                    'population': lambda x: ((x.notnull()) & (x != 0)).sum(), #Pour les variables, on retraite les vides, et les lignes égales à 0
                                      'gdp': lambda x: ((x.notnull()) & (x != 0)).sum(), #Pour les variables, on retraite les vides, et les lignes égales à 0
                                      'co2': lambda x: ((x.notnull()) & (x != 0)).sum(), #Pour les variables, on retraite les vides, et les lignes égales à 0
                                      'total_ghg' : lambda x: ((x.notnull()) & (x != 0)).sum()}) #Pour les variables, on retraite les vides, et les lignes égales à 0
                                      
missing_values_by_year = missing_values_by_year.rename(columns = {"country" : "Total count", "population" : "count of pop", "gdp" : "count of gdp", "co2" : "count of co2", "total_ghg" : "count of ghg"})


traces = []

for column in missing_values_by_year.columns:
    trace = go.Scatter(x=missing_values_by_year.index, y=missing_values_by_year[column], mode='lines+markers', name=column)
    traces.append(trace)


layout = go.Layout(title='Nombre de valeurs renseignées par années et par variable comparé au nombre maxi de données possible (Total count)',
                  xaxis=dict(title='Year'),
                  yaxis=dict(title='Count'))

fig = go.Figure(data=traces, layout=layout)

st.plotly_chart(fig)

st.subheader("Analyse de la colonne 'ISO_Code'")

count_iso_code = owid["iso_code"].count()
nb_na_iso_code = owid["iso_code"].isna().sum()
taux_na_iso_code = nb_na_iso_code / (count_iso_code + nb_na_iso_code)
st.write("Nombre de valeurs vides (ISO_Code)", nb_na_iso_code)
st.write("Taux de valeurs manquantes (ISO_Code) :", taux_na_iso_code * 100)

owid_na_iso_code = owid[owid["iso_code"].isna()]
if st.checkbox("Afficher les pays correspondants"):
    st.write(owid_na_iso_code["country"].unique())

st.subheader("Recapitulatif des retraitements à appliquer sur le Dataset")

text1 = '''
1 - Sélection des variables :
'''
st.markdown(text1)
st.code(''' 
owid_final = owid[["year","country","iso_code","gdp","population","co2"]]
''', language = 'python')
text2 = '''
2 - Retraitement des iso_code = null :
'''
st.markdown(text2)
st.code(''' 
owid_final = owid_final[owid_final["iso_code"].notnull()]
''', language = 'python')

text3 = '''
3 - Sélection de l'intervalle d'année :
'''
st.markdown(text3)
st.code(''' 
owid_final = owid_final[owid_final["year"].between(1990,2018)]
''', language = 'python')

text4 = '''
Le dataset est prêt pour les analyses
'''  
st.markdown(text4)

#Sélection des variables
owid_final = owid[["year","country","iso_code","gdp","population","co2"]]

#Retraitement des iso_code = null
owid_final = owid_final[owid_final["iso_code"].notnull()]

#Sélection de l'intervalle d'année
owid_final = owid_final[owid_final["year"].between(1990,2018)]

st.dataframe(owid_final.head())
st.write("Nombre de lignes :", owid_final.shape[0])
