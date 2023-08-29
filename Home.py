import streamlit as st
from PIL import Image

#essa função junta as 3 paginas e busca dentro de uma pasta chama pages
st.set_page_config(
    page_title="Home"
    #page_icon=""
)



#image_path = 'C:/repos/ftc_programacao_python\logo.png' 
image = Image.open('logo.png')
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Cury Company') # o simbolo '#' níveis de fonte -  # titulo, ## subtitulo)
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown('''___''')

st.write("# Curry Company Growth Dashboard")
st.markdown(
    """
    Growth Dashboar foi construido para acopmanhar as metricas de crescimento dos entregadores e restaurantes.
    ### Como utilizar o Growth Dashboard?
    - Visão Empresas:
        - Visão gerencial: Métricas gerais de comportamento.
        - Visão tática: Indicadores semanais de geolocalização.
        - Visão geografica: insights de geolocalização.
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento
    - Visão Restaurante:
        - Indicadores semanais de crescimento dos restaurantes.
    ### Ask for help
    - Time de Data Science no Discord
        - Obrigado.
    """)
