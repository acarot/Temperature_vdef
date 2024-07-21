import streamlit as st
import numpy as np
import pandas as pd
import pickle
import plotly.graph_objects as go
from sklearn.metrics import mean_squared_error
from prophet.plot import plot_plotly

def charger_modele(nom_fichier):
    # Charger le modèle à partir du fichier Pickle
    with open(nom_fichier, "rb") as fichier_modele:
        modele = pickle.load(fichier_modele)
    return modele

def transform_df_hem (df):
  month_map = {"Jan": 1, "Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9, "Oct":10,"Nov":11,"Dec":12}
  df = df.drop(["J-D","D-N","DJF","MAM","JJA", "SON"], axis = 1)
  df = pd.melt(df, id_vars = ["Year"], var_name = "Month", value_name="Temp")
  df['Month'] = df['Month'].map(month_map)
  df['date'] = pd.to_datetime(df[['Year', 'Month']].assign(day=1))
  df = df.drop(["Year","Month"], axis = 1)
  df = df.set_index("date")
  df = df.sort_values(by='date')
  return df

#Import des modèles - VsCode
#arima_glob = "arima_glob.pkl"
#arima_glob_opti = "arima_glob_opti.pkl"
#sarima_glob = "sarima_glob.pkl"
#sarima_glob_opti = "sarima_glob_opti.pkl"
#prophet_glob = "prophet_glob.pkl"
#prophet_glob_opti = "prophet_glob_opti.pkl"
#arima_nh_opti = "arima_nh_opti.pkl"
#arima_sh_opti = "arima_sh_opti.pkl"
#sarima_nh_opti = "sarima_nh_opti.pkl"
#sarima_sh_opti = "sarima_sh_opti.pkl"
#prophet_nh_opti = "prophet_nh_opti.pkl"
#prophet_sh_opti = "prophet_sh_opti.pkl"

#Import des modèles - Colab
arima_glob = "/content/drive/MyDrive/Colab_Notebooks/NOV23-CDA-TEMP_TERRESTRE/Streamlit/arima_glob.pkl"
arima_glob_opti = "/content/drive/MyDrive/Colab_Notebooks/NOV23-CDA-TEMP_TERRESTRE/Streamlit/arima_glob_opti.pkl"
sarima_glob = "/content/drive/MyDrive/Colab_Notebooks/NOV23-CDA-TEMP_TERRESTRE/Streamlit/sarima_glob.pkl"
sarima_glob_opti = "/content/drive/MyDrive/Colab_Notebooks/NOV23-CDA-TEMP_TERRESTRE/Streamlit/sarima_glob_opti.pkl"
prophet_glob = "/content/drive/MyDrive/Colab_Notebooks/NOV23-CDA-TEMP_TERRESTRE/Streamlit/prophet_glob.pkl"
prophet_glob_opti = "/content/drive/MyDrive/Colab_Notebooks/NOV23-CDA-TEMP_TERRESTRE/Streamlit/prophet_glob_opti.pkl"
arima_nh_opti = "/content/drive/MyDrive/Colab_Notebooks/NOV23-CDA-TEMP_TERRESTRE/Streamlit/arima_nh_opti.pkl"
arima_sh_opti = "/content/drive/MyDrive/Colab_Notebooks/NOV23-CDA-TEMP_TERRESTRE/Streamlit/arima_sh_opti.pkl"
sarima_nh_opti = "/content/drive/MyDrive/Colab_Notebooks/NOV23-CDA-TEMP_TERRESTRE/Streamlit/sarima_nh_opti.pkl"
sarima_sh_opti = "/content/drive/MyDrive/Colab_Notebooks/NOV23-CDA-TEMP_TERRESTRE/Streamlit/sarima_sh_opti.pkl"
prophet_nh_opti = "/content/drive/MyDrive/Colab_Notebooks/NOV23-CDA-TEMP_TERRESTRE/Streamlit/prophet_nh_opti.pkl"
prophet_sh_opti = "/content/drive/MyDrive/Colab_Notebooks/NOV23-CDA-TEMP_TERRESTRE/Streamlit/prophet_sh_opti.pkl"

st.set_page_config(
    page_title="Modélisation",
    page_icon="📈",
    layout = "wide",
    initial_sidebar_state = "expanded"
)

ZonAnn = st.session_state.df_ZonAnn
ZonAnn = ZonAnn[["Year", "Glob"]]
ZonAnn['Year'] = pd.to_datetime(ZonAnn['Year'], format='%Y')
ZonAnn = ZonAnn.rename(columns={"Year":"Date","Glob":"Temp"})
ZonAnn=ZonAnn.set_index("Date")
st.session_state.df_ZonAnnRetraite = ZonAnn
st.session_state.df_GLBRetraite = transform_df_hem(st.session_state.df_GLB)

radio = st.sidebar.radio("**Modélisation - Sommaire**", ("Introduction","Prédictions des températures globales","Prédiction des températures par hémisphère","Conclusion"))

if radio == "Introduction":

    st.markdown("# Modélisation")
    st.markdown("## Introduction : objectifs, méthodologie")

    txt = '''Notre objectif dans cette étape de modélisation était de réussir à **prédire l'évolution des températures à l'horizon 2050**.  
    Pour ce faire, nous nous sommes basés sur des modèles de **séries temporelles** qui nous permettent de prédire des valeurs futures en \
    fonction des données historiques.  
    Parmi les modèles de séries temporelles existants, nous avons choisi pour notre analyse de nous \
    focaliser sur trois d'entre eux : Le modèle **ARIMA**, le modèle **SARIMA** et enfin, le modèle **PROPHET**.
    '''
    st.markdown(txt)

    txt = '''Pour mener à bien cette étape de modélisation nous avons appliqué la méthodologie suivante sur l'ensemble des modèles : 

    1. Entraînement d'un premier modèle sur les données d'entraînement
    2. Prédictions sur l'ensemble de test et évaluation du modèle grâce à la RMSE
    3. Prédictions à l'horizon 2050
    4. Optimisation du modèle grâce à l'outil ParameterGrid de Sklearn
    5. Entraînement du modèle optimisé sur l'ensemble des données et prédictions à l'horizon 2050
    '''
    st.markdown(txt)

    txt = '''Dans un premier temps, nous avons tenté de prédire les températures à l'échelle **globale**, puis nous avons complété notre analyse par des prédictions
    par **hémisphères** car comme nous l'avons vu précédemment, il peut exister des disparités importantes lorsque l'on regarde les évolutions de températures par zones géographiques.
    '''

    st.markdown(txt)

if radio == "Prédictions des températures globales":

        st.markdown("# Modélisation")
        st.markdown(f"## {radio}")
        st.markdown("Par soucis de simplicité nous ne présenterons ici que les résultats des modèles dits 'optimisés', c'est à dire après recherche des meilleures paramètres qui permettent d'atteindre la valeur de RMSE la plus faible.")
        
        tab1, tab2, tab3 = st.tabs(["ARIMA","SARIMA","PROPHET"])

        with tab1:
            st.markdown("### Prédictions à 2050 avec le modèle optimisé")

            txt = ''' Pour le modèle ARIMA, nous avons utilisé le dataset contenant les données annuelles. En effet, ARIMA n'ayant pas de composante saisonnière
            nous ne pouvions pas prendre les données mensuelles qui risquaient d'intégrer une saisonnalité.
            '''
            st.markdown(txt)

            with st.expander("Afficher les données utilisées pour l'analyse"):
                choix = st.radio("Afficher le dataframe 'Données annuelles' brut ou retraité ?", ["Brut","Retraité"], horizontal= True, label_visibility= "collapsed")
                if choix == "Brut":
                    st.dataframe(st.session_state.df_ZonAnn)
                elif choix == "Retraité":
                    st.dataframe(st.session_state.df_ZonAnnRetraite)

            st.markdown('#### Entraînement et prédictions sur un modèle optimisé')
            
            df = st.session_state.df_ZonAnnRetraite

            arima_opti = charger_modele(arima_glob_opti)
            pred = arima_opti.predict(0,170)

            st.metric("RMSE",0.1478) 
            #Pas possible de la recalculer car le modèle est entraîner sur tout l'ensemble
            #On récupère donc la RMSE issue de la ParamterGrid

            fig = go.Figure()

            fig.add_trace(go.Scatter(x = pred.index, y = df.Temp, mode = "lines+markers", name = "Actual", line=dict(color='blue')))
            fig.add_trace(go.Scatter(x = pred.index, y = pred, mode = "lines+markers", name = "Predicted",line=dict(color='red')))

            st.plotly_chart(fig, use_container_width= True)
      
        with tab2:
            st.markdown("### Prédictions avec le modèle SARIMA")

            txt = ''' Le modèle SARIMA intègre une composante saisonnière qui nous permet cette fois-ci d'effectuer les prédictions à partir des données mensuelles
            '''
            st.markdown(txt)

            with st.expander("Afficher les données utilisées pour l'analyse"):
                choix = st.radio("Afficher le dataframe 'Données mensuelles' brut ou retraité ?", ["Brut","Retraité"],key = 'annuel_1', horizontal= True, label_visibility= "collapsed")
                if choix == "Brut":
                    st.dataframe(st.session_state.df_GLB)
                elif choix == "Retraité":
                    st.dataframe(st.session_state.df_GLBRetraite)

            st.markdown('#### Prédictions à 2050 avec le modèle optimisé')
            
            df = st.session_state.df_GLBRetraite

            sarima_opti = charger_modele(sarima_glob_opti)
            pred = sarima_opti.predict(0,((2050-1880)*12)+11)

            st.metric("RMSE",0.1830) 
            #Pas possible de la recalculer car le modèle est entraîner sur tout l'ensemble
            #On récupère donc la RMSE issue de la ParamterGrid

            fig = go.Figure()

            fig.add_trace(go.Scatter(x = pred.index, y = df.Temp, mode = "lines+markers", name = "Actual", line=dict(color='blue')))
            fig.add_trace(go.Scatter(x = pred.index, y = pred, mode = "lines+markers", name = "Predicted",line=dict(color='red')))

            st.plotly_chart(fig, use_container_width= True)
        
        with tab3:
            st.markdown("### Prédictions avec le modèle PROPHET")

            txt = ''' Le modèle PROPHET étant adapté pour prédire des données mensuelles, nous utilisons là aussi le dataset avec les données par années et par mois.
            '''
            st.markdown(txt)

            with st.expander("Afficher les données utilisées pour l'analyse"):
                choix = st.radio("Afficher le dataframe 'Données mensuelles' brut ou retraité ?", ["Brut","Retraité"],key = 'annuel_2', horizontal= True, label_visibility= "collapsed")
                if choix == "Brut":
                    st.dataframe(st.session_state.df_GLB)
                elif choix == "Retraité":
                    st.dataframe(st.session_state.df_GLBRetraite)

            st.markdown('#### Prédictions à 2050 avec le modèle optimisé')
            
            df = st.session_state.df_GLBRetraite
            df = df.rename(columns={"date":"ds","Temp":"y"})

            st.metric("RMSE",0.1808)

            m = charger_modele(prophet_glob_opti)
            future = m.make_future_dataframe(periods=324, freq='MS')
            forecast = m.predict(future)

            st.plotly_chart(plot_plotly(m,forecast), use_container_width= True)

if radio == "Prédiction des températures par hémisphère":

        st.markdown("# Modélisation")
        st.markdown(f"## {radio}")
        txt = ''' Les résultats sur les températures globales étant assez satisfaisants nous avons poursuivi notre analyse sur les prédictions des températures
        par hémisphères, en conservant la même méthodologie que celle utilisée pour la prédiction des températures globales. Par soucis de simplification, nous ne présenterons ici
        que les prédictions issues des modèles "optimisés".
        '''
        st.markdown(txt)

        tab1, tab2, tab3 = st.tabs(["ARIMA","SARIMA","PROPHET"])

        with tab1:
            st.markdown("### Prédictions avec le modèle ARIMA")

            hem = st.radio("Choix hémisphère :", ["Hémisphère NORD", "Hémisphère SUD"], horizontal= True, label_visibility= 'collapsed')

            if hem == "Hémisphère NORD":

                st.markdown("#### Prédictions des températures pour l'hémisphère Nord")
                df = st.session_state.df_ZonAnn
                df = df[["Year","NHem"]]
                df['Year'] = pd.to_datetime(df['Year'], format='%Y')
                df = df.rename(columns={"Year":"Date","NHem":"Temp"})
                df = df.set_index("Date")
                st.session_state.df_ZonAnn_Nh_Retraite = df

                arima = charger_modele(arima_nh_opti)

                with st.expander("Afficher les données utilisées pour l'analyse"):
                    choix = st.radio("Afficher le dataframe 'Données mensuelles' brut ou retraité ?", ["Brut","Retraité"],key = 'annuel_nh', horizontal= True, label_visibility= "collapsed")
                    if choix == "Brut":
                        st.dataframe(st.session_state.df_ZonAnn)
                    elif choix == "Retraité":
                        st.dataframe(st.session_state.df_ZonAnn_Nh_Retraite)
                
                st.metric("RMSE :", 0.1286)

                pred = arima.predict(0,170)

                fig = go.Figure()

                fig.add_trace(go.Scatter(x = pred.index, y = df.Temp, mode = "lines+markers", name = "Actual", line=dict(color='blue')))
                fig.add_trace(go.Scatter(x = pred.index, y = pred, mode = "lines+markers", name = "Predicted",line=dict(color='red')))

                st.plotly_chart(fig, use_container_width= True)
            
            elif hem == "Hémisphère SUD":

                st.markdown("#### Prédictions des températures pour l'hémisphère Sud")
                df = st.session_state.df_ZonAnn
                df = df[["Year","SHem"]]
                df['Year'] = pd.to_datetime(df['Year'], format='%Y')
                df = df.rename(columns={"Year":"Date","SHem":"Temp"})
                df = df.set_index("Date")
                st.session_state.df_ZonAnn_Sh_Retraite = df

                arima = charger_modele(arima_sh_opti)

                with st.expander("Afficher les données utilisées pour l'analyse"):
                    choix = st.radio("Afficher le dataframe 'Données mensuelles' brut ou retraité ?", ["Brut","Retraité"],key = 'annuel_sh', horizontal= True, label_visibility= "collapsed")
                    if choix == "Brut":
                        st.dataframe(st.session_state.df_ZonAnn)
                    elif choix == "Retraité":
                        st.dataframe(st.session_state.df_ZonAnn_Sh_Retraite)
                
                st.metric("RMSE :", 0.0786)

                pred = arima.predict(0,170)

                fig = go.Figure()

                fig.add_trace(go.Scatter(x = pred.index, y = df.Temp, mode = "lines+markers", name = "Actual", line=dict(color='blue')))
                fig.add_trace(go.Scatter(x = pred.index, y = pred, mode = "lines+markers", name = "Predicted",line=dict(color='red')))

                st.plotly_chart(fig, use_container_width= True)

        with tab2:
            st.markdown("### Prédictions avec le modèle SARIMA")

            hem = st.radio("Choix hémisphère :", ["Hémisphère NORD", "Hémisphère SUD"], horizontal= True, label_visibility= 'collapsed', key = 'sarima_hem')

            if hem == "Hémisphère NORD":

                st.markdown("#### Prédictions des températures pour l'hémisphère Nord")
                df = st.session_state.df_NH
                df = transform_df_hem(df)
                st.session_state.df_NH_Retraite = df

                sarima = charger_modele(sarima_nh_opti)

                with st.expander("Afficher les données utilisées pour l'analyse"):
                    choix = st.radio("Afficher le dataframe 'Données mensuelles' brut ou retraité ?", ["Brut","Retraité"],key = 'mensuel_sarima_nh', horizontal= True, label_visibility= "collapsed")
                    if choix == "Brut":
                        st.dataframe(st.session_state.df_NH)
                    elif choix == "Retraité":
                        st.dataframe(st.session_state.df_NH_Retraite)
                
                st.metric("RMSE :", 0.2411)

                pred = sarima.predict(0,2051)

                fig = go.Figure()

                fig.add_trace(go.Scatter(x = pred.index, y = df.Temp, mode = "lines+markers", name = "Actual", line=dict(color='blue')))
                fig.add_trace(go.Scatter(x = pred.index, y = pred, mode = "lines+markers", name = "Predicted",line=dict(color='red')))

                st.plotly_chart(fig, use_container_width= True)
            
            elif hem == "Hémisphère SUD":

                st.markdown("#### Prédictions des températures pour l'hémisphère Sud")
                df = st.session_state.df_SH
                df = transform_df_hem(df)
                st.session_state.df_SH_Retraite = df

                sarima = charger_modele(sarima_sh_opti)

                with st.expander("Afficher les données utilisées pour l'analyse"):
                    choix = st.radio("Afficher le dataframe 'Données mensuelles' brut ou retraité ?", ["Brut","Retraité"],key = 'mensuel_sarima_sh', horizontal= True, label_visibility= "collapsed")
                    if choix == "Brut":
                        st.dataframe(st.session_state.df_SH)
                    elif choix == "Retraité":
                        st.dataframe(st.session_state.df_SH_Retraite)
                
                st.metric("RMSE :", 0.1740)

                pred = sarima.predict(0,2051)

                fig = go.Figure()

                fig.add_trace(go.Scatter(x = pred.index, y = df.Temp, mode = "lines+markers", name = "Actual", line=dict(color='blue')))
                fig.add_trace(go.Scatter(x = pred.index, y = pred, mode = "lines+markers", name = "Predicted",line=dict(color='red')))

                st.plotly_chart(fig, use_container_width= True)

        with tab3:
            st.markdown("### Prédictions avec le modèle PROPHET")

            hem = st.radio("Choix hémisphère :", ["Hémisphère NORD", "Hémisphère SUD"], horizontal= True, label_visibility= 'collapsed', key = 'prophet_hem')

            if hem == "Hémisphère NORD":

                st.markdown("#### Prédictions des températures pour l'hémisphère Nord")

                with st.expander("Afficher les données utilisées pour l'analyse"):
                    choix = st.radio("Afficher le dataframe 'Données mensuelles' brut ou retraité ?", ["Brut","Retraité"],key = 'mensuel_prophet_nh', horizontal= True, label_visibility= "collapsed")
                    if choix == "Brut":
                        st.dataframe(st.session_state.df_NH)
                    elif choix == "Retraité":
                        st.dataframe(st.session_state.df_NH_Retraite)

                st.metric("RMSE :", 0.2375)

                df = st.session_state.df_NH_Retraite
                df = df.rename(columns={"date":"ds","Temp":"y"})

                m =charger_modele(prophet_nh_opti)

                future = m.make_future_dataframe(periods= 324, freq = "MS")

                forecast = m.predict(future)

                st.plotly_chart(plot_plotly(m,forecast), use_container_width= True)

            elif hem == "Hémisphère SUD":
                
                st.markdown("#### Prédictions des températures pour l'hémisphère Sud")

                with st.expander("Afficher les données utilisées pour l'analyse"):
                    choix = st.radio("Afficher le dataframe 'Données mensuelles' brut ou retraité ?", ["Brut","Retraité"],key = 'mensuel_prophet_sh', horizontal= True, label_visibility= "collapsed")
                    if choix == "Brut":
                        st.dataframe(st.session_state.df_SH)
                    elif choix == "Retraité":
                        st.dataframe(st.session_state.df_SH_Retraite)
                
                st.metric("RMSE :", 0.1864)

                df = st.session_state.df_SH_Retraite
                df = df.rename(columns={"date":"ds","Temp":"y"})

                m =charger_modele(prophet_sh_opti)

                future = m.make_future_dataframe(periods= 324, freq = "MS")

                forecast = m.predict(future)

                st.plotly_chart(plot_plotly(m,forecast), use_container_width= True)

if radio == "Conclusion":

        st.markdown("# Modélisation")
        st.markdown(f"## {radio}")
        st.markdown("### Synthèse des prédictions au niveau global")

        result_global = {"RMSE" : ["0.1478", "0.1830", "0.1808"],
                         "Temp. 2050": ["+1.65°C", "+1.71°C", "+1.60°C"]}
        result_global = pd.DataFrame(result_global, index=["ARIMA Optimisé", "SARIMA Optimisé", "PROPHET Optimisé"]).T

        st.dataframe(result_global, use_container_width= True)

        txt = ''' Les résultats de ces prévisions à l'échelle globale sont plutôt encourageants. L'ensemble des modèles testés obtiennent des résultats
        plutôt satisfaisants, c'est à dire, une RMSE acceptable ainsi que des prévisions à 2050 en adéquation avec les données historiques. 
        De plus, on remarque que les prévisions retournées sont assez proches (de +1.60°C à +1.71°C) ce qui laisse penser que les résultats sont plutôt cohérents.
        '''
        st.markdown(txt)

        st.markdown("### Synthèse des prédictions par hémisphère")

        st.markdown("#### Hémisphère Nord")

        result_nh = {"RMSE" : ["0.1860", "0.2410", "0.2374"],
                         "Temp. 2050": ["+2.71°C", "+3.37°C", "+2.11°C"]}
        result_nh = pd.DataFrame(result_nh, index=["ARIMA Optimisé", "SARIMA Optimisé", "PROPHET Optimisé"]).T

        st.dataframe(result_nh, use_container_width= True)

        st.markdown("#### Hémisphère Sud")

        result_sh = {"RMSE" : ["0.0786", "0.1740", "0.1864"],
                         "Temp. 2050": ["+1.06°C", "+1.05°C", "+0.95°C"]}
        result_sh = pd.DataFrame(result_sh, index=["ARIMA Optimisé", "SARIMA Optimisé", "PROPHET Optimisé"]).T

        st.dataframe(result_sh, use_container_width= True)

        txt = '''Globalement, les résultats obtenus sur ces prévisions restent cohérents et soulignent une fois de plus les disparités qu'il peut exister entre
        différentes zones géographiques.  
        Sur l'hémisphère sud, les prévisions retournées semblent être cohérentes avec une RMSE correcte et des températures assez proches d'un modèle à un autre.  
        Sur l'hémipshère nord, les résultats sont plus mitigés avec une RMSE nettement supérieure à l'hémisphère Sud, ce qui suppose une marge d'erreur plus grande.
        De plus, les prévisions varient beaucoup d'un modèle à un autre, et encore plus avec le modèle SARIMA qui paraît avoir plus de mal à prédire les données de cet hémisphère.
        '''

        st.markdown(txt)