import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="Conclusion",
    page_icon="✅",
    layout = 'wide'
)
st.write("## Conclusion")

st.subheader("Synthèse du travail effectué")

text = '''  - Après l'exploration des données et leurs visualisations, nous avons constaté des **tendances similaires** dans leurs évolutions au fil des ans. 
  - Les premiers résultats de Machine Learning nous confirmaient également l'**augentation des températures**. 
  - Nous avons affiné nos résultats à l'aide de l'outil **ParameterGrid**, qui nous a permis l'**optimisation** des paramètres à utiliser pour les modèles ARIMA, SARIMA et PROPHET. '''
  
st.markdown(text)

col1, col2 = st.columns([0.7,0.3])

with col1 :
  text3 = '''

  - Grâce à cela, nous avons réalisé des estimations **à 2050** très cohérentes, entre les 3 modèles.
  Les résultats, nous montrent une évolution des températures :
    - entre **+1.60°C** et **+1.71°C** sur l'ensemble du **Globe**, 
    - entre **+2.11°C** et **3.37°C** sur l'hémisphère **Nord**,
    - entre **+0.79°C** et **1.06°C** sur l'hémisphère **Sud**. 

  '''
  st.markdown(text3)
  st.write("**Ainsi nous constatons une augmentation des températures bien plus élevée dans la zone Nord du globe, là où l'activité humaine et industrielle y sont les plus importantes.**")

with col2:
  st.image("/content/drive/MyDrive/Colab_Notebooks/NOV23-CDA-TEMP_TERRESTRE/Streamlit/Image2.jpg")

st.subheader("Prise de recul sur les résultats")
text5 = '''
N'oublions pas que dans l'exercice de ce projet, les données de températures ont été visuellement mises en corrélation avec d'autres variables, comme par exemple les émissions de CO2. 
Mais les modélisations ont été réalisées **uniquement sur les températures** ; les résultats sont donc dans l'**hypothèse où aucune action** n'est mise en place pour réduire les activités humaines.
'''
st.markdown(text5)

text = ''' Nous pourrions étudier **différents scénarios** en fonction des variables secondaires à notre études, dans un esprit plus optimiste ou plus pessimiste. 
Cela nous permettrait d'avoir une vision plus précise sur les **impacts liés à cette évolution croissante** et sur les **actions à mener pour la ralentir**. '''

st.markdown(text)