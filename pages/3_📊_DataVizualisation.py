import streamlit as st
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
from scipy.stats import pearsonr

st.set_page_config(
    page_title="DataVizualisation",
    page_icon="📊",
    layout = 'wide'
)

#Import des dataframes après retraitements à partir du fichier import_data.py

df_owid = st.session_state.df_owid
long_lat = st.session_state.df_long_lat
loti_ZonAnn = st.session_state.df_ZonAnn

# Stockage des dataframes transformés :
#long_lat cleaned
longlat_cleaned = long_lat.drop(['ISO-ALPHA-2','FIFA','ISO-Name','Historical','WikiData_ID','WikiData_Latitude','WikiData_Longitude','WikiData_Label','WikiData_Description'],axis = 1)
#On commence par supprimer les lignes où le code ISO n'est pas renseigné
longlat_cleaned = longlat_cleaned[longlat_cleaned["ISO-ALPHA-3"].notnull()]
#Ensuite, on supprime les lignes identifiées en doublons avec Latitude et Longitude différente afin de conserver celles qui semblent être les plus pertinentes
index_west_germany = longlat_cleaned.loc[longlat_cleaned["Country"]== "West Germany"].index
longlat_cleaned = longlat_cleaned.drop(index_west_germany)
index_north_yemen = longlat_cleaned.loc[longlat_cleaned["Country"]== "North Yemen"].index
longlat_cleaned = longlat_cleaned.drop(index_north_yemen)
#Ensuite, on supprime tous les autres doublons (peu importe celui que l'on conserve car ils ont la même valeur de latitude et longitude)
longlat_cleaned = longlat_cleaned.drop_duplicates(subset = "ISO-ALPHA-3", keep = "first")
st.session_state.longlat_cleaned = longlat_cleaned

#df_owid3
# On fusionne le df owid avec le fichier latitudes nettoyé grâce à merge
dico = {'iso_code':'ISO-ALPHA-3'}
df_owid = df_owid.rename(dico, axis = 1)
df_owid2 = df_owid.merge(right = longlat_cleaned, on = 'ISO-ALPHA-3')

# On supprimes les NaN en se basant sur la colonne iso alpha 3
df_owid3 = df_owid2.dropna(axis=0,subset = 'ISO-ALPHA-3')

# On séquence les pays / hémisphere et latitudes :/3 et /8
# Création d'une colonne avec l'hémisphère d'appartenance
def hemisphere1(x):
    if x >= 0:
        return 'HN'
    if x <= 0:
        return 'HS'

df_owid3['Hemisphere'] = df_owid3['Latitude'].apply(hemisphere1)

# Création d'une colonne avec la strate d'appartenance (/3)
def hemisphere2(x):
    if x >= 24:
        return '24N-90N'
    if x > -24 and x < 24:
        return '24S-24N'
    if x < -24:
        return '90S-24S'

df_owid3['Cut 3 strats'] = df_owid3['Latitude'].apply(hemisphere2)

# Création d'une colonne avec la strate d'appartenance (/8)
def hemisphere3(x):
    if x > 64:
        return '64N-90N'
    if x > 44 and x < 64:
        return '44N-64N'
    if x > 24 and x < 44:
        return '24N-44N'
    if x > 0 and x < 24:
        return 'EQU-24N'
    if x < 0 and x > -24:
        return '24S-EQU'
    if x < -24 and x > -44:
        return '44S-24S'
    if x < -44 and x > -64:
        return '64S-44S'
    if x < -64:
        return '90S-64S'

df_owid3['Cut 8 strats'] = df_owid3['Latitude'].apply(hemisphere3)

st.session_state.df_owid3 = df_owid3

#df_gdp_co2_ghg
#Sélection des champs utiles à l'analyse et réduction du Dataset
#Population / GDP / Co2 / GHG
selected_cols = ['country', 'year', 'ISO-ALPHA-3','population', 'gdp','co2','total_ghg']
df_filtered = df_owid3[selected_cols]

#Sélection des champs utiles à l'analyse et réduction du Dataset
cols_gdp_co2_ghg = ['country', 'year', 'ISO-ALPHA-3','gdp','co2','population','total_ghg']

#On filtre sur iso_code not null pour supprimer les données des continents
#On sélectionne l'intervalle de date qui paraît la plus optimale car intégrant une disponibilité de données de manière égale (1990 - 2018)
df_gdp_co2_ghg = df_owid3.loc[(df_owid3["ISO-ALPHA-3"].notnull()) & (df_owid3["year"].between(1990,2018)),selected_cols]

st.session_state.df_gdp_co2_ghg = df_gdp_co2_ghg

st.title("DataVizualisation")


radio = st.sidebar.radio("**DataVizualisation - Sommaire**", ("Introduction","Fusion bases de données","Evolutions entre 1990 et 2018","Evolution températures de 1880 à 2023","Corrélation entre variables","Conclusion"))

if radio == "Introduction":

    st.write("**Nous allons à présent réaliser des projections visuels sur les jeux de données en notre possession :**")
    st.markdown("- Dans un premier temps, nous allons faire un rapprochement entre le dataframe owid et l'évolution des températures par année du fichier loti ZonAnn")
    st.markdown("- Dans un deuxième temps, cela nous permettra de montrer l'évolution des températures sur la période sélectionnée, par zone")
    st.markdown("- Ensuite, dans un troisième temps, nous allons nous concentrer sur l'évolution des températures par zones de 1880 à 2023")
    st.markdown("- Enfin, nous allons montrer la corrélation entre variables")


if radio == "Fusion bases de données":

    st.write("Comme annoncé en préambule, nous allons faire un rapprochement entre le dataframe owid et l'évolution des températures par année du fichier loti ZonAnn")
    st.write("Ce rapprochement entre les deux bases de données sera réalisé grâce à un fichier qui reprend les longitudes-latitudes pour tous les pays du globe")

    st.markdown("- Le fichier se présente de la manière suivante")
    st.dataframe(long_lat.head())
    st.markdown("- Informations dataframe")
    col1, col2, col3 = st.columns(3)
    #Nombre d'indicateurs
    col1.metric("Nombre de colonnes", long_lat.shape[1])
    col2.metric("Nombre de lignes", long_lat.shape[0])
    col3.metric("Taux de valeurs manquantes", (long_lat.isna().mean().mean() *100).round(2))

    col_text, col_img = st.columns([0.7,0.3])

    with col_text:
      st.markdown("- On ne retient du fichier de latitudes longitudes que les données qui nous intéressent")

      longlat_cleaned = long_lat.drop(['ISO-ALPHA-2','FIFA','ISO-Name','Historical','WikiData_ID','WikiData_Latitude','WikiData_Longitude','WikiData_Label','WikiData_Description'],axis = 1)
      st.dataframe(longlat_cleaned.head())
    
    with col_img:
      st.image("/content/drive/MyDrive/Colab_Notebooks/NOV23-CDA-TEMP_TERRESTRE/Streamlit/Image3.jpg")

    st.write("**Notre dataframe longitude-latitude nécessite encore les opérations suivantes avant la fusion avec la base owid :**")
    st.markdown("- Suppression des lignes où le code ISO n'est pas renseigné")
    st.markdown("- Suppression des lignes identifiées en doublons avec Latitude et Longitude différente afin de conserver celles qui semblent être les plus pertinentes")
    st.markdown("- Suppresion d'autres doublons sur le code ISO ALPHA 3")

    st.write("**Sur le nouveau dataframe créé :**")
    st.markdown("- Fusion des dataframes sur la colonne ISO ALPHA 3")
    st.markdown("- Suppression des valeurs nulles sur ISO ALPHA 3")
    st.markdown("- Séquençage des pays par hémisphère, par strates de 3 et strates de 8")
    
    st.dataframe(df_owid3.head())

    st.write("**Notre dataset est prêt pour nos visuels !**:smiley:")
    
if radio == "Evolutions entre 1990 et 2018":
    
    df_owid3 = st.session_state.df_owid3

    st.write("Nous pouvons à présent réaliser des premiers visuels par zones de 1990 à 2018")
    st.markdown("## Au niveau global :")
    st.markdown("- Après rédution du dataset, suppression des valeurs nulles et des valeurs qui ne nous intéressent pas dans notre étude, nous avons la base ci-dessous :")

    st.dataframe(df_gdp_co2_ghg.head())

    st.markdown("### Création d'un dataframe par variables que l'on va projeter :")
    st.write("A noter que le dernier dataframe va nous permettre de suivre la disponibilité des valeurs au fil des années")
    #On crée le dataframe pour l'évolution du co2 par année à l'échelle mondiale
    co2_by_year = df_gdp_co2_ghg.groupby("year")["co2"].sum()

    #On crée le dataframe pour l'évolution du gdp par année à l'échelle mondiale
    gdp_by_year = df_gdp_co2_ghg.groupby("year")["gdp"].sum()

    #On crée le dataframe pour l'évolution de la population par année à l'échelle mondiale
    pop_by_year = df_gdp_co2_ghg.groupby("year")["population"].sum()

    #On crée le dataframe pour l'évolution du ghg par année à l'échelle mondiale
    ghg_by_year = df_gdp_co2_ghg.groupby("year")["total_ghg"].sum()

    #On crée un dataframe qui va permettre de compter pour chacune des variables le nombre de valeurs renseignées
    values_by_year = df_gdp_co2_ghg.groupby("year").agg({'country': 'count',
                                        'gdp': lambda x: ((x.notnull()) & (x != 0)).sum(),
                                        'co2': lambda x: ((x.notnull()) & (x != 0)).sum(),
                                            'total_ghg': lambda x: ((x.notnull()) & (x != 0)).sum(),
                                            'population': lambda x: ((x.notnull()) & (x != 0)).sum()})

    with st.expander("Afficher les dataframes utilisées pour l'analyse"):
        choix = st.radio("Afficher les dataframes ?", ["CO2/An","PIB/An","Population/An","Gaz à effet de serre/An","Décompte Valeurs"], horizontal= True, label_visibility= "collapsed")
        if choix == "CO2/An":
            st.dataframe(co2_by_year)
        if choix == "PIB/An":
            st.dataframe(gdp_by_year)
        if choix == "Population/An":
            st.dataframe(pop_by_year)
        if choix == "Gaz à effet de serre/An":
            st.dataframe(ghg_by_year)
        if choix == "Décompte Valeurs":
            st.dataframe(values_by_year)


    st.markdown("### Projection visuelle des données globales :")

    #CO2
    co2 = make_subplots(rows=2, cols=1, subplot_titles=('CO2 Emissions', 'Count variables'), vertical_spacing= 0.5, shared_xaxes= True)
    co2.add_trace(go.Scatter(x = co2_by_year.index, y = co2_by_year.values,mode='lines+markers', name='Evol Co2' ))

    traces = []
    for column in values_by_year.columns:
        trace = go.Scatter(x=values_by_year.index, y=values_by_year[column], mode='lines+markers', name='Value count')
    traces.append(trace)
    for trace in traces:
        co2.add_trace(trace, row = 2, col = 1)

    co2.update_layout(xaxis_title = "Year", yaxis_title = "CO2")

    #gdp
    gdp = make_subplots(rows=2, cols=1, subplot_titles=('GDP Emissions', 'Count variables'), vertical_spacing= 0.5, shared_xaxes= True)
    gdp.add_trace(go.Scatter(x = gdp_by_year.index, y = gdp_by_year.values,mode='lines+markers', name='Evol Co2' ))

    traces = []
    for column in values_by_year.columns:
        trace = go.Scatter(x=values_by_year.index, y=values_by_year[column], mode='lines+markers', name="Value count")
    traces.append(trace)
    for trace in traces:
        gdp.add_trace(trace, row=2, col=1)

    gdp.update_layout(xaxis_title = "Year", yaxis_title = "GDP")

    #population
    pop = make_subplots(rows=2, cols=1, subplot_titles=('Population', 'Count variables'), vertical_spacing = 0.5, shared_xaxes= True)
    pop.add_trace(go.Scatter(x = pop_by_year.index, y = pop_by_year.values,mode='lines+markers', name='Evol Co2' ))

    traces = []
    for column in values_by_year.columns:
        trace = go.Scatter(x=values_by_year.index, y=values_by_year[column], mode='lines+markers', name="Value count")
    traces.append(trace)
    for trace in traces:
        pop.add_trace(trace, row=2, col=1)

    pop.update_layout(xaxis_title = "Year", yaxis_title = "Population")

    #ghg
    ghg = make_subplots(rows=2, cols=1, subplot_titles=('GHG Emissions', 'Count variables'), vertical_spacing = 0.5, shared_xaxes= True)
    ghg.add_trace(go.Scatter(x = ghg_by_year.index, y = ghg_by_year.values,mode='lines+markers', name='Evol Co2' ))

    traces = []
    for column in values_by_year.columns:
        trace = go.Scatter(x=values_by_year.index, y=values_by_year[column], mode='lines+markers', name="Value count")
    traces.append(trace)
    for trace in traces:
        ghg.add_trace(trace, row=2, col=1)

    ghg.update_layout(xaxis_title = "Year", yaxis_title = "GHG")

    tab1, tab2, tab3, tab4 = st.tabs(["CO2 Evolution","GDP Evolution","Population Evolution","GHG Evolution"])
    with tab1 :
        st.plotly_chart(co2)
    with tab2 :
        st.plotly_chart(gdp)
    with tab3 :
        st.plotly_chart(pop)
    with tab4 :
        st.plotly_chart(ghg)

    st.markdown("## Par Hémiphère Nord et Sud :")
    st.markdown("- Nous allons à présent pousser cette analyse dans le détail géographique en commençant par les hémisphères :")

    #Sélection des champs utiles à l'analyse et réduction du Dataset
    infos_strates = ['country', 'year', 'ISO-ALPHA-3','gdp','co2','total_ghg','population','Hemisphere','Cut 3 strats','Cut 8 strats']
    strates = df_owid3[infos_strates]

    # Evolution des variables sur les hémisphères
    # Création du df avec seulement l'HN de 1990 à 2018
    strates_hn = strates.loc[(strates['Hemisphere'] == 'HN') & (strates['year'].between(1990,2018))]

    # Création du df avec seulement l'HS de 1990 à 2018
    strates_hs = strates.loc[(strates['Hemisphere'] == 'HS') & (strates['year'].between(1990,2018))]

    st.markdown("### Projections réalisées à partir des 2 dataframes ci-dessous :")

    with st.expander("Afficher les dataframes utilisées pour l'analyse"):
            choix = st.radio("Afficher les dataframes ?", ["Dataframe Hémisphère Nord","Dataframe Hémisphère Sud"], horizontal= True, label_visibility= "collapsed")
            if choix == "Dataframe Hémisphère Nord":
                st.dataframe(strates_hn)
            if choix == "Dataframe Hémisphère Sud":
                st.dataframe(strates_hs)

    #On crée le dataframe pour l'évolution du co2 par année pour HN
    co2_hn = strates_hn.groupby("year")["co2"].sum()

    #On crée le dataframe pour l'évolution du gdp par année pour HN
    gdp_hn = strates_hn.groupby("year")["gdp"].sum()

    #On crée le dataframe pour l'évolution du ghg par année pour HN
    ghg_hn = strates_hn.groupby("year")["total_ghg"].sum()

    #On crée le dataframe pour l'évolution de la population par année pour HN
    pop_hn = strates_hn.groupby("year")["population"].sum()

    #On crée le dataframe pour l'évolution du co2 par année pour HS
    co2_hs = strates_hs.groupby("year")["co2"].sum()

    #On crée le dataframe pour l'évolution du gdp par année pour HS
    gdp_hs = strates_hs.groupby("year")["gdp"].sum()

    #On crée le dataframe pour l'évolution du ghg par année pour HS
    ghg_hs = strates_hs.groupby("year")["total_ghg"].sum()

    #On crée le dataframe pour l'évolution de la population par année pour HS
    pop_hs = strates_hs.groupby("year")["population"].sum()

    #On crée les df qui vont permettre de compter pour chaque hémisphère le nombre de valeurs renseignées
    values_by_year_hn = strates_hn.groupby("year").agg({'country': 'count',
                                        'gdp': lambda x: ((x.notnull()) & (x != 0)).sum(),
                                        'co2': lambda x: ((x.notnull()) & (x != 0)).sum(),
                                            'total_ghg': lambda x: ((x.notnull()) & (x != 0)).sum(),
                                            'population': lambda x: ((x.notnull()) & (x != 0)).sum()})

    values_by_year_hs = strates_hs.groupby("year").agg({'country': 'count',
                                        'gdp': lambda x: ((x.notnull()) & (x != 0)).sum(),
                                        'co2': lambda x: ((x.notnull()) & (x != 0)).sum(),
                                            'total_ghg': lambda x: ((x.notnull()) & (x != 0)).sum(),
                                            'population': lambda x: ((x.notnull()) & (x != 0)).sum()})

    # Décompte de la disponibilité des données par hémisphère
    h_count = make_subplots(rows=1, cols=2, subplot_titles=('Décompte variables HN','Décompte variables HS'))

    tab1, tab2, tab3, tab4, tab5 = st.tabs([" Evolution CO2","Evolution Gaz à effet de serre","Evolution population","Evolution PIB","Décompte valeurs"])
    with tab1 :
        # Tracé des visuels par hémisphère
        h_co2n = go.Figure()
        h_co2n.add_trace(go.Scatter(x = co2_hn.index, y = co2_hn.values,mode='lines+markers', name='Evol HN' ))
        h_co2n.update_layout(title = "Evolution Hémisphère Nord")
        st.plotly_chart(h_co2n)

        h_co2s = go.Figure()
        h_co2s.add_trace(go.Scatter(x = co2_hs.index, y = co2_hs.values,mode='lines+markers', name='Evol HS' ))
        h_co2s.update_layout(title = "Evolution Hémisphère Sud")
        st.plotly_chart(h_co2s)

    with tab2 :
        h_ghgn = go.Figure()
        h_ghgn.add_trace(go.Scatter(x = ghg_hn.index, y = ghg_hn.values,mode='lines+markers', name='Evol HN' ))
        h_ghgn.update_layout(title = "Evolution Hémisphère Nord")
        st.plotly_chart(h_ghgn)

        h_ghgs = go.Figure()
        h_ghgs.add_trace(go.Scatter(x = ghg_hs.index, y = ghg_hs.values,mode='lines+markers', name='Evol HS' ))
        h_ghgs.update_layout(title = "Evolution Hémisphère Sud")
        st.plotly_chart(h_ghgs)

    with tab3 :
        h_popn = go.Figure()
        h_popn.add_trace(go.Scatter(x = pop_hn.index, y = pop_hn.values,mode='lines+markers', name='Evol HN' ))
        h_popn.update_layout(title = "Evolution Hémisphère Nord")
        st.plotly_chart(h_popn)

        h_pops = go.Figure()
        h_pops.add_trace(go.Scatter(x = pop_hs.index, y = pop_hs.values,mode='lines+markers', name='Evol HS' ))
        h_pops.update_layout(title = "Evolution Hémisphère Sud")
        st.plotly_chart(h_pops)

    with tab4 :
        h_gdpn = go.Figure()
        h_gdpn.add_trace(go.Scatter(x = gdp_hn.index, y = gdp_hn.values, mode = "lines+markers", name = "Evol HN" ))
        h_gdpn.update_layout(title = "Evolution Hémisphère Nord")
        st.plotly_chart(h_gdpn)

        h_gdps = go.Figure()
        h_gdps.add_trace(go.Scatter(x = gdp_hs.index, y = gdp_hs.values, mode = "lines+markers", name = "Evol HS" ))
        h_gdps.update_layout(title = "Evolution Hémisphère Sud")
        st.plotly_chart(h_gdps)

    with tab5 :
        traces = []
        traces_2 = []

        for column in values_by_year_hn.columns:
            trace_hn = go.Scatter(x=values_by_year_hn.index, y=values_by_year_hn[column], mode='lines+markers', name=column)
            traces.append(trace_hn)

        for column in values_by_year_hs.columns:
            trace_hs = go.Scatter(x=values_by_year_hs.index, y=values_by_year_hs[column], mode='lines+markers', name=column)
            traces_2.append(trace_hs)

        for trace_hn in traces:h_count.add_trace(trace_hn, row=1, col=1)
        for trace_hs in traces_2:h_count.add_trace(trace_hs, row=1, col=2)
        st.plotly_chart(h_count)

    st.markdown("## Par strates sur 3 niveaux :")
    st.markdown("- Nous allons à présent nous concentrer sur le découpage par 3 strates :")
    st.markdown("- Après réduction du dataset, nous appliquons un groupby qui va faire la somme de chaque variable par année :")

    # Evolution des variables sur les 3 strates
    # Création du df avec seulement la strate 1/3 de 1990 à 2018
    strates_1_3 = strates.loc[(strates['Cut 3 strats'] == '24N-90N') & (strates['year'].between(1990,2018))]

    # Création du df avec seulement la strate 2/3 de 1990 à 2018
    strates_2_3 = strates.loc[(strates['Cut 3 strats'] == '24S-24N') & (strates['year'].between(1990,2018))]

    # Création du df avec seulement la strate 1/3 de 1990 à 2018
    strates_3_3 = strates.loc[(strates['Cut 3 strats'] == '90S-24S') & (strates['year'].between(1990,2018))]

    #On crée le dataframe pour l'évolution du co2 par année pour 1/3
    co2_1_3 = strates_1_3.groupby("year")["co2"].sum()

    #On crée le dataframe pour l'évolution du gdp par année pour 1/3
    gdp_1_3 = strates_1_3.groupby("year")["gdp"].sum()

    #On crée le dataframe pour l'évolution du ghg par année pour 1/3
    ghg_1_3 = strates_1_3.groupby("year")["total_ghg"].sum()

    #On crée le dataframe pour l'évolution de la population par année pour 1/3
    pop_1_3 = strates_1_3.groupby("year")["population"].sum()

    #On crée le dataframe pour l'évolution du co2 par année pour 2/3
    co2_2_3 = strates_2_3.groupby("year")["co2"].sum()

    #On crée le dataframe pour l'évolution du gdp par année pour 2/3
    gdp_2_3 = strates_2_3.groupby("year")["gdp"].sum()

    #On crée le dataframe pour l'évolution du ghg par année pour 2/3
    ghg_2_3 = strates_2_3.groupby("year")["total_ghg"].sum()

    #On crée le dataframe pour l'évolution de la population par année pour 2/3
    pop_2_3 = strates_2_3.groupby("year")["population"].sum()

    #On crée le dataframe pour l'évolution du co2 par année pour 3/3
    co2_3_3 = strates_3_3.groupby("year")["co2"].sum()

    #On crée le dataframe pour l'évolution du gdp par année pour 3/3
    gdp_3_3 = strates_3_3.groupby("year")["gdp"].sum()

    #On crée le dataframe pour l'évolution du ghg par année pour 3/3
    ghg_3_3 = strates_3_3.groupby("year")["total_ghg"].sum()

    #On crée le dataframe pour l'évolution de la population par année pour 3/3
    pop_3_3 = strates_3_3.groupby("year")["population"].sum()

    #On crée les df qui vont permettre de compter pour chaque strate le nombre de valeurs renseignées
    values_by_year_1_3 = strates_1_3.groupby("year").agg({'country': 'count',
                                        'gdp': lambda x: ((x.notnull()) & (x != 0)).sum(),
                                        'co2': lambda x: ((x.notnull()) & (x != 0)).sum(),
                                            'total_ghg': lambda x: ((x.notnull()) & (x != 0)).sum(),
                                            'population': lambda x: ((x.notnull()) & (x != 0)).sum()})

    values_by_year_2_3 = strates_2_3.groupby("year").agg({'country': 'count',
                                        'gdp': lambda x: ((x.notnull()) & (x != 0)).sum(),
                                        'co2': lambda x: ((x.notnull()) & (x != 0)).sum(),
                                            'total_ghg': lambda x: ((x.notnull()) & (x != 0)).sum(),
                                            'population': lambda x: ((x.notnull()) & (x != 0)).sum()})

    values_by_year_3_3 = strates_3_3.groupby("year").agg({'country': 'count',
                                        'gdp': lambda x: ((x.notnull()) & (x != 0)).sum(),
                                        'co2': lambda x: ((x.notnull()) & (x != 0)).sum(),
                                            'total_ghg': lambda x: ((x.notnull()) & (x != 0)).sum(),
                                            'population': lambda x: ((x.notnull()) & (x != 0)).sum()})


    tab1, tab2, tab3, tab4, tab5 = st.tabs([" Evolution CO2","Evolution Gaz à effet de serre","Evolution population","Evolution PIB","Décompte valeurs"])
    with tab1 :
        # Tracé des visuels pour les 3 strates
        co2_st = go.Figure()
        co2_st.add_trace(go.Scatter(x = co2_1_3.index, y = co2_1_3.values,mode='lines+markers', name='1.24N-90N'))
        co2_st.add_trace(go.Scatter(x = co2_2_3.index, y = co2_2_3.values,mode='lines+markers', name='2.24S-24N'))
        co2_st.add_trace(go.Scatter(x = co2_3_3.index, y = co2_3_3.values,mode='lines+markers', name='3.90S-24S'))
        co2_st.update_layout(title = 'Evolution CO2')
        st.plotly_chart(co2_st)

    with tab2 :
        ghg_st = go.Figure()
        ghg_st.add_trace(go.Scatter(x = ghg_1_3.index, y = ghg_1_3.values,mode='lines+markers', name='1.24N-90N'))
        ghg_st.add_trace(go.Scatter(x = ghg_2_3.index, y = ghg_2_3.values,mode='lines+markers', name='2.24S-24N'))
        ghg_st.add_trace(go.Scatter(x = ghg_3_3.index, y = ghg_3_3.values,mode='lines+markers', name='3.90S-24S'))
        ghg_st.update_layout(title = 'Evolution Gaz à effet de serre')
        st.plotly_chart(ghg_st)

    with tab3 :
        pop_st = go.Figure()
        pop_st.add_trace(go.Scatter(x = pop_1_3.index, y = pop_1_3.values,mode='lines+markers', name='1.24N-90N'))
        pop_st.add_trace(go.Scatter(x = pop_2_3.index, y = pop_2_3.values,mode='lines+markers', name='2.24S-24N'))
        pop_st.add_trace(go.Scatter(x = pop_3_3.index, y = pop_3_3.values,mode='lines+markers', name='3.90S-24S'))
        pop_st.update_layout(title = 'Evolution Population')
        st.plotly_chart(pop_st)

    with tab4 :
        gdp_st = go.Figure()
        gdp_st.add_trace(go.Scatter(x = gdp_1_3.index, y = gdp_1_3.values,mode='lines+markers', name='1.24N-90N'))
        gdp_st.add_trace(go.Scatter(x = gdp_2_3.index, y = gdp_2_3.values,mode='lines+markers', name='2.24S-24N'))
        gdp_st.add_trace(go.Scatter(x = gdp_3_3.index, y = gdp_3_3.values,mode='lines+markers', name='3.90S-24S'))
        gdp_st.update_layout(title = 'Evolution PIB')
        st.plotly_chart(gdp_st)

    with tab5 :
        # Décompte de la disponibilité des données par strate
        fig = make_subplots(rows=1, cols=3, subplot_titles=('Décompte variables 1ère strate','Décompte variables 2ème strate','Décompte variables 3ème strate'))

        traces = []
        traces_2 = []
        traces_3 = []

        for column in values_by_year_1_3.columns:
            trace_1_3 = go.Scatter(x=values_by_year_1_3.index, y=values_by_year_1_3[column], mode='lines+markers', name=column)
            traces.append(trace_1_3)

        for column in values_by_year_2_3.columns:
            trace_2_3 = go.Scatter(x=values_by_year_2_3.index, y=values_by_year_2_3[column], mode='lines+markers', name=column)
            traces_2.append(trace_2_3)

        for column in values_by_year_3_3.columns:
            trace_3_3 = go.Scatter(x=values_by_year_3_3.index, y=values_by_year_3_3[column], mode='lines+markers', name=column)
            traces_3.append(trace_3_3)

        for trace_1_3 in traces:fig.add_trace(trace_1_3, row=1, col=1)
        for trace_2_3 in traces_2:fig.add_trace(trace_2_3, row=1, col=2)
        for trace_3_3 in traces_3:fig.add_trace(trace_3_3, row=1, col=3)
        st.plotly_chart(fig)

    st.markdown("## Par strates sur 8 niveaux :")
    st.markdown("- Nous allons à présent nous concentrer sur le découpage par 8 strates :")
    st.markdown("- Après réduction du dataset, nous appliquons un nouveau groupby qui va faire la somme de chaque variable par année sur une strate précisé:")

    # Evolution des variables sur les 8 strates
    # Création du df avec seulement la strate 1/8 de 1990 à 2018
    strates_1_8 = strates.loc[(strates['Cut 8 strats'] == '64N-90N') & (strates['year'].between(1990,2018))]

    # Création du df avec seulement la strate 2/8 de 1990 à 2018
    strates_2_8 = strates.loc[(strates['Cut 8 strats'] == '44N-64N') & (strates['year'].between(1990,2018))]

    # Création du df avec seulement la strate 3/8 de 1990 à 2018
    strates_3_8 = strates.loc[(strates['Cut 8 strats'] == '24N-44N') & (strates['year'].between(1990,2018))]

    # Création du df avec seulement la strate 4/8 de 1990 à 2018
    strates_4_8 = strates.loc[(strates['Cut 8 strats'] == 'EQU-24N') & (strates['year'].between(1990,2018))]

    # Création du df avec seulement la strate 5/8 de 1990 à 2018
    strates_5_8 = strates.loc[(strates['Cut 8 strats'] == '24S-EQU') & (strates['year'].between(1990,2018))]

    # Création du df avec seulement la strate 6/8 de 1990 à 2018
    strates_6_8 = strates.loc[(strates['Cut 8 strats'] == '44S-24S') & (strates['year'].between(1990,2018))]

    # Création du df avec seulement la strate 7/8 de 1990 à 2018
    strates_7_8 = strates.loc[(strates['Cut 8 strats'] == '64S-44S') & (strates['year'].between(1990,2018))]

    # Création du df avec seulement la strate 8/8 de 1990 à 2018
    strates_8_8 = strates.loc[(strates['Cut 8 strats'] == '90S-64S') & (strates['year'].between(1990,2018))]

    #On crée le dataframe pour l'évolution du co2 par année pour 1/8
    co2_1_8 = strates_1_8.groupby("year")["co2"].sum()

    #On crée le dataframe pour l'évolution du gdp par année pour 1/8
    gdp_1_8 = strates_1_8.groupby("year")["gdp"].sum()

    #On crée le dataframe pour l'évolution du ghg par année pour 1/8
    ghg_1_8 = strates_1_8.groupby("year")["total_ghg"].sum()

    #On crée le dataframe pour l'évolution de la population par année pour 1/8
    pop_1_8 = strates_1_8.groupby("year")["population"].sum()

    #On crée le dataframe pour l'évolution du co2 par année pour 2/8
    co2_2_8 = strates_2_8.groupby("year")["co2"].sum()

    #On crée le dataframe pour l'évolution du gdp par année pour 2/8
    gdp_2_8 = strates_2_8.groupby("year")["gdp"].sum()

    #On crée le dataframe pour l'évolution du ghg par année pour 2/8
    ghg_2_8 = strates_2_8.groupby("year")["total_ghg"].sum()

    #On crée le dataframe pour l'évolution de la population par année pour 2/8
    pop_2_8 = strates_2_8.groupby("year")["population"].sum()

    #On crée le dataframe pour l'évolution du co2 par année pour 3/8
    co2_3_8 = strates_3_8.groupby("year")["co2"].sum()

    #On crée le dataframe pour l'évolution du gdp par année pour 3/8
    gdp_3_8 = strates_3_8.groupby("year")["gdp"].sum()

    #On crée le dataframe pour l'évolution du ghg par année pour 3/8
    ghg_3_8 = strates_3_8.groupby("year")["total_ghg"].sum()

    #On crée le dataframe pour l'évolution de la population par année pour 3/8
    pop_3_8 = strates_3_8.groupby("year")["population"].sum()

    #On crée le dataframe pour l'évolution du co2 par année pour 4/8
    co2_4_8 = strates_4_8.groupby("year")["co2"].sum()

    #On crée le dataframe pour l'évolution du gdp par année pour 4/8
    gdp_4_8 = strates_4_8.groupby("year")["gdp"].sum()

    #On crée le dataframe pour l'évolution du ghg par année pour 4/8
    ghg_4_8 = strates_4_8.groupby("year")["total_ghg"].sum()

    #On crée le dataframe pour l'évolution de la population par année pour 4/8
    pop_4_8 = strates_4_8.groupby("year")["population"].sum()

    #On crée le dataframe pour l'évolution du co2 par année pour 5/8
    co2_5_8 = strates_5_8.groupby("year")["co2"].sum()

    #On crée le dataframe pour l'évolution du gdp par année pour 5/8
    gdp_5_8 = strates_5_8.groupby("year")["gdp"].sum()

    #On crée le dataframe pour l'évolution du ghg par année pour 5/8
    ghg_5_8 = strates_5_8.groupby("year")["total_ghg"].sum()

    #On crée le dataframe pour l'évolution de la population par année pour 5/8
    pop_5_8 = strates_5_8.groupby("year")["population"].sum()

    #On crée le dataframe pour l'évolution du co2 par année pour 6/8
    co2_6_8 = strates_6_8.groupby("year")["co2"].sum()

    #On crée le dataframe pour l'évolution du gdp par année pour 6/8
    gdp_6_8 = strates_6_8.groupby("year")["gdp"].sum()

    #On crée le dataframe pour l'évolution du ghg par année pour 6/8
    ghg_6_8 = strates_6_8.groupby("year")["total_ghg"].sum()

    #On crée le dataframe pour l'évolution de la population par année pour 6/8
    pop_6_8 = strates_6_8.groupby("year")["population"].sum()

    # On ne crée pas de df pour la strate 7/8 car ne retournant pas de résultat

    #On crée le dataframe pour l'évolution du co2 par année pour 8/8
    co2_8_8 = strates_8_8.groupby("year")["co2"].sum()

    #On crée le dataframe pour l'évolution du gdp par année pour 8/8
    gdp_8_8 = strates_8_8.groupby("year")["gdp"].sum()

    #On crée le dataframe pour l'évolution du ghg par année pour 8/8
    ghg_8_8 = strates_8_8.groupby("year")["total_ghg"].sum()

    #On crée le dataframe pour l'évolution de la population par année pour 8/8
    pop_8_8 = strates_8_8.groupby("year")["population"].sum()

    tab1, tab2, tab3, tab4 = st.tabs([" Evolution CO2","Evolution Gaz à effet de serre","Evolution population","Evolution PIB"])
    with tab1 :
        co2_1 = go.Figure()
        co2_1.add_trace(go.Scatter(x = co2_1_8.index, y = co2_1_8.values,mode='lines+markers', name='1.64N-90N'))
        co2_1.add_trace(go.Scatter(x = co2_2_8.index, y = co2_2_8.values,mode='lines+markers', name='2.44N-64N'))
        co2_1.add_trace(go.Scatter(x = co2_3_8.index, y = co2_3_8.values,mode='lines+markers', name='3.24N-44N'))
        co2_1.add_trace(go.Scatter(x = co2_4_8.index, y = co2_4_8.values,mode='lines+markers', name='4.EQU-24N'))
        co2_1.add_trace(go.Scatter(x = co2_5_8.index, y = co2_5_8.values,mode='lines+markers', name='5.24S-EQU'))
        co2_1.add_trace(go.Scatter(x = co2_6_8.index, y = co2_6_8.values,mode='lines+markers', name='6.44S-24S'))
        co2_1.add_trace(go.Scatter(x = co2_8_8.index, y = co2_8_8.values,mode='lines+markers', name='8.90S-64S'))
        st.plotly_chart(co2_1)

    with tab2 :
        ghg_1 = go.Figure()
        ghg_1.add_trace(go.Scatter(x = ghg_1_8.index, y = ghg_1_8.values,mode='lines+markers', name='1.64N-90N'))
        ghg_1.add_trace(go.Scatter(x = ghg_2_8.index, y = ghg_2_8.values,mode='lines+markers', name='2.44N-64N'))
        ghg_1.add_trace(go.Scatter(x = ghg_3_8.index, y = ghg_3_8.values,mode='lines+markers', name='3.24N-44N'))
        ghg_1.add_trace(go.Scatter(x = ghg_4_8.index, y = ghg_4_8.values,mode='lines+markers', name='4.EQU-24N'))
        ghg_1.add_trace(go.Scatter(x = ghg_5_8.index, y = ghg_5_8.values,mode='lines+markers', name='5.24S-EQU'))
        ghg_1.add_trace(go.Scatter(x = ghg_6_8.index, y = ghg_6_8.values,mode='lines+markers', name='6.44S-24S'))
        ghg_1.add_trace(go.Scatter(x = ghg_8_8.index, y = ghg_8_8.values,mode='lines+markers', name='8.90S-64S'))
        st.plotly_chart(ghg_1)

    with tab3 :
        pop_1 = go.Figure()
        pop_1.add_trace(go.Scatter(x = pop_1_8.index, y = pop_1_8.values,mode='lines+markers', name='1.64N-90N'))
        pop_1.add_trace(go.Scatter(x = pop_2_8.index, y = pop_2_8.values,mode='lines+markers', name='2.44N-64N'))
        pop_1.add_trace(go.Scatter(x = pop_3_8.index, y = pop_3_8.values,mode='lines+markers', name='3.24N-44N'))
        pop_1.add_trace(go.Scatter(x = pop_4_8.index, y = pop_4_8.values,mode='lines+markers', name='4.EQU-24N'))
        pop_1.add_trace(go.Scatter(x = pop_5_8.index, y = pop_5_8.values,mode='lines+markers', name='5.24S-EQU'))
        pop_1.add_trace(go.Scatter(x = pop_6_8.index, y = pop_6_8.values,mode='lines+markers', name='6.44S-24S'))
        pop_1.add_trace(go.Scatter(x = pop_8_8.index, y = pop_8_8.values,mode='lines+markers', name='8.90S-64S'))
        st.plotly_chart(pop_1)

    with tab4 :
        gdp_1 = go.Figure()
        gdp_1.add_trace(go.Scatter(x = gdp_1_8.index, y = gdp_1_8.values,mode='lines+markers', name='1.64N-90N'))
        gdp_1.add_trace(go.Scatter(x = gdp_2_8.index, y = gdp_2_8.values,mode='lines+markers', name='2.44N-64N'))
        gdp_1.add_trace(go.Scatter(x = gdp_3_8.index, y = gdp_3_8.values,mode='lines+markers', name='3.24N-44N'))
        gdp_1.add_trace(go.Scatter(x = gdp_4_8.index, y = gdp_4_8.values,mode='lines+markers', name='4.EQU-24N'))
        gdp_1.add_trace(go.Scatter(x = gdp_5_8.index, y = gdp_5_8.values,mode='lines+markers', name='5.24S-EQU'))
        gdp_1.add_trace(go.Scatter(x = gdp_6_8.index, y = gdp_6_8.values,mode='lines+markers', name='6.44S-24S'))
        gdp_1.add_trace(go.Scatter(x = gdp_8_8.index, y = gdp_8_8.values,mode='lines+markers', name='8.90S-64S'))
        st.plotly_chart(gdp_1)

    st.session_state.df_gdp_co2_ghg = df_gdp_co2_ghg

if radio == "Evolution températures de 1880 à 2023":

    st.write("Nous allons à présent réaliser les visuels pour comprendre les évolutions de température de 1880 à 2020 grâce au dataset l-oti_ZonAnn")
    with st.expander("Voir dataframe l-oti ZonAnn"):
        st.dataframe(loti_ZonAnn)

    st.markdown("## Evolution globale et par hémisphère :")
    # Pour avoir une meilleure idée de l'évolution des températures, on demande un tracé de la tendance sur la période couverte au niveau globale et par hémisphère
    fig_px = px.scatter(loti_ZonAnn, x="Year", y=["Glob","NHem",'SHem'], trendline="ols", labels = ["1. Global","2. HN","3. HS"])
    st.plotly_chart(fig_px)
    st.markdown("**Constat :** Au terme de de cette première projection, on peut constater que l'hémisphère nord contribue le plus à l'augmentation globale des températures. On peut voir que la période 1930 voit un inversement de position entre l'hémisphère nord et l'hémisphère sud en terme d'augmentation.")

    st.markdown("## Evolution par latitude sur 3 strates :")
    # Dans l'optique d'avoir une vision encore plus fine de l'évolution des températures par zone géographique, on fait découpage par trois par latitude
    # Nous ajoutons une courbe des tendances sur chaque variable pour avoir une meilleure appréciation de l'évolution
    fig_pxx = px.scatter(loti_ZonAnn, x="Year", y=["24N-90N","24S-24N",'90S-24S'], trendline="ols")
    st.plotly_chart(fig_pxx)
    st.markdown("**Constat:** On peut constater une fois encore que les températures augmentent sur toutes les zones. Cependant, la strate la plus au nord connait l'augmentation des températures la plus importante. La seconde strate au niveau de l'équateur est la 2ème plus importante, mais reste proche de la tendance de la strate la plus au sud.")

    st.markdown("## Evolution par latitude sur 8 strates :")
    # Avec la volonté d'avoir un découpage toujours plus fin, nous regardons l'évolution des températures selon un découpage par latitude sur 8 zones
    # Nous ajoutons une courbe des tendances sur chaque variable pour avoir une meilleure appréciation de l'évolution
    fig_pxxx = px.scatter(loti_ZonAnn, x="Year", y=["64N-90N","44N-64N",'24N-44N','EQU-24N','24S-EQU','44S-24S','64S-44S','90S-64S'],
                    trendline="ols")
    st.plotly_chart(fig_pxxx)
    st.markdown("**Constat :** Toutes les courbes sont en augmentation mais avec une intensité différente. Les deux zones les plus au nord connaissant les évolutions de température les plus importantes.")

if radio == "Corrélation entre variables":

    df_gdp_co2_ghg = st.session_state.df_gdp_co2_ghg

    st.markdown("## Étude de corrélations entre les différentes variables")

    option = st.selectbox("Quelles variables souhaitez-vous comparer ?",
                ("Co2 et GDP", "Température et Co2"))

    if option == "Co2 et GDP":

        st.markdown("### Visualisation des variables")

        # Création du graphique co2 / gdp
        co2_by_year = df_gdp_co2_ghg.groupby("year")["co2"].sum() #Evolution du co2 par années
        gdp_by_year = df_gdp_co2_ghg.groupby("year")["gdp"].sum() #Evolution du gdp par années
        values_by_year = df_gdp_co2_ghg.groupby("year").agg({'country': 'count',
                                        'gdp': lambda x: ((x.notnull()) & (x != 0)).sum(),
                                        'co2': lambda x: ((x.notnull()) & (x != 0)).sum()}) #compter pour chacune des variables le nombre de valeurs renseignées


        fig = make_subplots(rows=1, cols=2, subplot_titles=('CO2 Emissions', 'GDP'))

        fig.add_trace(go.Scatter(x = co2_by_year.index, y = co2_by_year.values,mode='lines+markers', name='Evol Co2' ),row=1, col=1)
        fig.add_trace(go.Scatter(x = gdp_by_year.index, y = gdp_by_year.values, mode = "lines+markers", name = "Evol Gdp" ),row=1, col=2)

        fig.update_layout(title='CO2 and GDP Over Years',
                xaxis_title='Year',
                yaxis_title='Value')
        # Show the plot
        #fig.update_layout( width = 1200, height=400)
        st.plotly_chart(fig, use_container_width=True)

        commentaire = '''Ces deux graphiques montrent que les tendances à l'échelle mondiale semblent être similaires.
        En d'autres termes il semblerait que l'augmentation d'une des deux variables entraîne l'augmentation de l'autre variable.
        Bien que les résultats des graphiques soient déjà assez convaincants, \
        nous allons procéder à un test statistique pour vérifier l'hypothèse de corrélation entre ceux deux variables'''
        st.markdown(commentaire)

        st.markdown("### Vérification par un test statistique")

        commentaire = ''' Ces deux variables étant quantitatives nous allons procéder à un test de Pearson avec les hypothèses suivantes :
        h0 : Les variables Co2 et GDP ne sont pas corrélées
        h1 : Les variables sont corrélées '''

        st.markdown(commentaire)

        #On crée le dataframe avec les valeurs de co2 et gdp par années
        data_by_year = df_gdp_co2_ghg.groupby("year").agg({"co2" : "sum", "gdp" : "sum"})

        test_co2_gdp = pearsonr(data_by_year["gdp"],data_by_year["co2"])

        col1, col2 = st.columns(2)

        col1.metric("P-Valeur", test_co2_gdp[1] )
        col2.metric("Coefficient de Pearson", round(test_co2_gdp[0],2) )

        commentaire = ''' La P_valeur est très petite, ce qui signifie que nous pouvons rejeter l'hypothèe H0 et ainsi admettre une corrélation entre les deux variables.
        De plus, le coefficent de corrélation de Pearson proche de 1 nous indique qu'il y a une forte relation positive entre les deux variables '''

        st.markdown(commentaire)

    if option == "Température et Co2":

        st.markdown("### Visualisation des variables")

        co2_by_year = df_gdp_co2_ghg.groupby("year")["co2"].sum()
        df_temp_glob = loti_ZonAnn[["Year","Glob"]]

        fig = make_subplots(rows = 1, cols = 2, subplot_titles=('CO2 Emissions', 'Temperatures'))

        fig.add_trace(go.Scatter(x = co2_by_year.index, y = co2_by_year.values, mode = "lines+markers", name = "Evol Co2"), row = 1, col = 1)

        # Adding the Temperatures scatter plot with trendline
        fig.add_trace(go.Scatter(x=df_temp_glob["Year"], y=df_temp_glob["Glob"], mode="lines+markers", name="Evol Temp"), row=1, col=2)
        fig.add_trace(px.scatter(df_temp_glob, x="Year", y="Glob", trendline="ols").data[1], row=1, col=2)
        #.data[1] permet d'accéder uniquement à la courbe de tendance
        #px.scatter se compose donc des points --> .data[0] et de la droite .data[1]

        fig.update_layout(title='CO2 and Temp Over Years',
                xaxis_title='Year',
                yaxis_title='Value')

        st.plotly_chart(fig, use_container_width=True)

        commentaire = ''' Ces deux graphiques montrent d'un côté l'évolution des émissions de Co2 et de l'autre, l'évolution des températures.
        On remarque que les tendances observées sur la période sont très proches. On peut donc supposer qu'il existe un lien entre ces deux variables
        C'est ce que nous allons vérifier avec un test statistique'''

        st.markdown(commentaire)

        st.markdown("### Vérification par un test statistique")

        commentaire = ''' Ces deux variables étant quantitatives nous allons procéder à un test de Pearson avec les hypothèses suivantes :
        h0 : Les variables Co2 et GDP ne sont pas corrélées
        h1 : Les variables sont corrélées '''

        st.markdown(commentaire)

        #On crée le dataframe avec les valeurs de co2 et temp par années
        co2_temp_by_year = df_temp_glob.merge(right = co2_by_year, left_on = "Year", right_on = co2_by_year.index)

        test_co2_temp = pearsonr(co2_temp_by_year["Glob"],co2_temp_by_year["co2"])

        col1, col2 = st.columns(2)

        col1.metric("P-Valeur", test_co2_temp[1] )
        col2.metric("Coefficient de Pearson", round(test_co2_temp[0],2) )

        commentaire = ''' La P_valeur est très petite, ce qui signifie que nous pouvons rejeter l'hypothèe H0 et ainsi admettre une corrélation entre les deux variables.
        De plus, le coefficent de corrélation de Pearson proche de 1 nous indique qu'il y a une forte relation positive entre les deux variables '''

        st.markdown(commentaire)

if radio == "Conclusion":

        st.markdown('## Nous avons pu faire plusieurs constats au cours de cette partie :')
        st.markdown("### Evolution des températures :")
        st.markdown("- Oui les températures augmentent sur l'ensemble du globe, mais pas avec la même intensité selon les zones et les périodes")
        st.markdown("- Certaines zones de l'hémisphère nord ont connu une accélération à partir de 1930, les faisant même passer au-dessus d'autres zoness")

        st.markdown("### Evolution de l'activité humaine :")
        st.markdown("- Comme pour les températures, l'activité humaine n'évolue pas avec la même intensité selon les zones et les périodes")
        st.markdown("- Cette différence pour les zones peut d'une part s'expliquer via le nombre de pays")
        st.markdown("- D'autre part, selon la zone observée, on aura des pays avec un impact fort dû à leur activité")
        st.write("Compte tenu du niveau de disponibilité des données très disparates, nous prenons ces observations comme des tendances à observer plutôt qu'une vérité immuable.")
        st.write("Mais nous pouvons au terme avoir une compréhension sur l'évolution des variables sur un espace temps comme dans l'animation ci-dessous :")

        st.image("/content/drive/MyDrive/Colab_Notebooks/NOV23-CDA-TEMP_TERRESTRE/Flavien/Essais Streamlit/Streamlit/Evolution des températures globales par années.gif")
