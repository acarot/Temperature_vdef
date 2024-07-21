import streamlit as st
import pandas as pd

#Import des DataFrames
#Version VsCode
#st.session_state.df_ZonAnn = pd.read_csv("ZonAnn.Ts+dSST.csv")
#st.session_state.df_GLB = pd.read_csv("GLB.Ts+dSST.csv", skiprows=1)
#st.session_state.df_NH = pd.read_csv("NH.Ts+dSST.csv", skiprows = 1)
#st.session_state.df_SH = pd.read_csv("SH.Ts+dSST.csv", skiprows = 1)
#st.session_state.df_owid = pd.read_csv("owid-co2-data.csv")
#st.session_state.df_long_lat = pd.read_csv("longitude-latitude.csv")'''
#Version Collab
st.session_state.df_ZonAnn = pd.read_csv("/content/drive/MyDrive/Colab_Notebooks/NOV23-CDA-TEMP_TERRESTRE/ZonAnn.Ts+dSST.csv")
st.session_state.df_GLB = pd.read_csv("/content/drive/MyDrive/Colab_Notebooks/NOV23-CDA-TEMP_TERRESTRE/GLB.Ts+dSST.csv", skiprows=1)
st.session_state.df_NH = pd.read_csv("/content/drive/MyDrive/Colab_Notebooks/NOV23-CDA-TEMP_TERRESTRE/NH.Ts+dSST.csv", skiprows = 1)
st.session_state.df_SH = pd.read_csv("/content/drive/MyDrive/Colab_Notebooks/NOV23-CDA-TEMP_TERRESTRE/SH.Ts+dSST.csv", skiprows = 1)
st.session_state.df_owid = pd.read_csv("/content/drive/MyDrive/Colab_Notebooks/NOV23-CDA-TEMP_TERRESTRE/owid-co2-data.csv")
st.session_state.df_long_lat = pd.read_csv("/content/drive/MyDrive/Colab_Notebooks/NOV23-CDA-TEMP_TERRESTRE/longitude-latitude.csv")

st.set_page_config(
    page_title="Introduction",
    page_icon="👋",
    layout='wide'
)

st.title('Température Terrestre')

col1, col2 = st.columns([0.7,0.3])

with col1:
  st.write("## Objectif du projet")
  text = '''\*Constater le réchauffement (et le dérèglement) climatique global à l’échelle 
  de la planète sur les derniers siècles et dernières décennies. 
  - Analyse au niveau mondial
  - Analyse par zone géographique
  - Comparaison avec des phases d’évolution de température antérieure à notre époque.

  La source de données est celle de la NASA.\*
  '''
  #st.markdown(text)
  st.markdown("*« Constater le réchauffement (et le dérèglement) climatique global à l’échelle de la planète sur les derniers siècles et dernières décennies.*")
  st.markdown("*- Analyse au niveau mondial*")
  st.markdown("*- Analyse par zone géographique*")
  st.markdown("*- Comparaison avec des phases d’évolution de température antérieure à notre époque*")
  st.markdown("*La source de données est celle de la NASA. »*")

with col2:
  st.image("/content/drive/MyDrive/Colab_Notebooks/NOV23-CDA-TEMP_TERRESTRE/Streamlit/Image.jpg")

st.write("## Présentation des participants")
#st.markdown("**Alexandre CAROT**   *'Avoir évolué dans l’industrie automobile et le luxe m’ont fait réaliser que je n’étais pas en accord avec mes convictions profondes comme l’accord et le respect de son environnement. J’ai donc fait le choix de retrouver cet attrait pour la cause environnementale via le prisme de l’évolution des températures à travers cette reprise d’études dans la data analyse'*")

#st.markdown("**Flavien CLEMENT**   *'Il est parfois difficile de démêler le vrai du faux avec tous les points de vues différents que l’on peut entendre ici et là. C’est pourquoi, ce projet qui nous permet de mettre à profit nos connaissances et compétences dans le domaine de la data pour nous permettre de vérifier et constater par nous-mêmes, à partir de données réelles, l'ampleur du réchauffement climatique m’a tout de suite attiré'*")

#st.markdown("**Sandrine COUSIN**   *'Ayant grandi dans le milieu agricole, puis travaillé dans les énergies renouvelables implantées dans certaines régions cycloniques du globe, et maintenant dans une coopérative agricole, je me sens très concernées par ce sujet. Il me semblait donc très intéressant de choisir ce projet d'étude.'*")


col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Alexandre CAROT**")
    st.markdown("*'Avoir évolué dans l’industrie automobile et le luxe m’ont fait réaliser que je n’étais pas en accord avec mes convictions profondes comme l’accord et le respect de son environnement. J’ai donc fait le choix de retrouver cet attrait pour la cause environnementale via le prisme de l’évolution des températures à travers cette reprise d’études dans la data analyse'*")

with col2:
    st.markdown("**Flavien CLEMENT**")
    st.markdown("*'Il est parfois difficile de démêler le vrai du faux avec tous les points de vues différents que l’on peut entendre ici et là. C’est pourquoi, ce projet qui nous permet de mettre à profit nos connaissances et compétences dans le domaine de la data pour nous permettre de vérifier et constater par nous-mêmes, à partir de données réelles, l'ampleur du réchauffement climatique m’a tout de suite attiré'*")

with col3:
    st.markdown("**Sandrine COUSIN**")
    st.markdown("*'Ayant grandi dans le milieu agricole, puis travaillé dans les énergies renouvelables implantées dans certaines régions cycloniques du globe, et maintenant dans une coopérative agricole, je me sens très concernées par ce sujet. Il me semblait donc très intéressant de choisir ce projet d'étude.'*")

st.write("## Déroulement du projet")

text1 = '''
- La présentation et l'exploration des données, en particulier le dataset nommé "owid" dans lequel nous avons trouvé des informations diverses et interessantes pour notre projet.
- La visualisation des différentes données, les températures mais aussi des informations à corréler, comme les émissions de GES.
- La modélisation, pour estimer la progression des valeurs de températures sur le prochaines année.
- Et enfin nous conclurons cette présentation avec une "prise de recul" vis à vis des résultats obtenus.
'''
st.markdown(text1)

