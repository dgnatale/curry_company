# libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

#bibliotecas necessárias
import pandas as pd
import streamlit as st # erro de st ao executar o streamlite
from PIL import Image #biblioteca para trabalhar com imagens
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title='Visão Empresa', layout='wide')


# ================================================
# FUNÇÕES
# ================================================

def country_maps (df1):
    
    df_aux=df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']].groupby(['City', 'Road_traffic_density']).median().reset_index()
    map = folium.Map()
        
    for index, location_info in df_aux.iterrows():
        folium.Marker( [location_info['Delivery_location_latitude'], location_info['Delivery_location_longitude']], 
                    popup=location_info[['City', 'Road_traffic_density']]).add_to(map)
            
    folium_static (map, width=1024, height=600)

def order_share_by_week(df1):
    # Quantidade de pedidos por semana /  numero unico de entregadores por semana
    df_aux01=df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    df_aux02=df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby('week_of_year').nunique().reset_index()
    
    df_aux=pd.merge(df_aux01, df_aux02, how='inner', on='week_of_year')
    df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    
    fig=px.line(df_aux, x='week_of_year', y='order_by_deliver')
    return fig
           

def order_by_week(df1):
    #criar coluna de semana
    df1['week_of_year']=df1['Order_Date'].dt.strftime('%U')
    df_aux=df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    fig=px.line(df_aux, x='week_of_year', y='ID')
    return fig

def traffic_order_city(df1):     
            
    df_aux=(df1.loc[:, ['ID', 'City', 'Road_traffic_density']]
                .groupby(['City', 'Road_traffic_density'])
                .count()
                .reset_index() )

    df_aux=df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]    
    fig=px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City')                
    return fig


def traffic_order_share(df1):                
    df_aux=(df1.loc[:, ['ID', 'Road_traffic_density']]
            .groupby('Road_traffic_density')
            .count()
            .reset_index() )
    
    df_aux=df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]
    df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum()                
    fig = px.pie(df_aux, values='entregas_perc', names='Road_traffic_density')               
    return fig

    
def order_metric(df1):
    cols = ['ID', 'Order_Date']
    # seleção de linhas
    df_aux = df1.loc[:, cols].groupby('Order_Date').count().reset_index()
    # desenhar o grafico de linhas
    # utilizar propria função do streamlit para exibir o grafico (Plotly_chart)
    fig = px.bar(df_aux, x='Order_Date', y='ID')
    return fig


def clean_code( df1):
    
    """ Esta função tem a responsabilidade de limpar o dataframe
        Tipos de limpeza:
        1. Remoção dos dados NaN
        2. Mudança do tipo de coluna de dados
        3. Remoção dos espaços das variáveis de texto
        4. Formatação da coluna de datas
        5. Limpeza da colina de tempo (remoção do texto da variável numérica)

        Input: Dataframe
        Output: Dataframe
    """

    # 1- convertendo a coluna Delivery_person_Age em numeros
    linhas_selecionadas = df1['Delivery_person_Age'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = df1['Road_traffic_density'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = df1['City'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = df1['Festival'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)
    
    # 2 - convertendo a coluna Delivery_person_Ratings de texto para numero decimal (float)
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)
    
    # 3 - convertendo a coluna Order_Date de texto para data
    df1['Order_Date']=pd.to_datetime(df1['Order_Date'], format = '%d-%m-%Y')
    
    # 4 - convertendo multiple_deliveries de texto para numero inteiro (int)
    linhas_selecionadas = df1['multiple_deliveries'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)
    
    # 5 - removendo os espaços dos textos/strings/object
    # foi necessário fazer um reset de index antes de fazer o FOR, pois,
    # com a removação das linhas que continham o NaN ficou faltando o index daquelas linhas
    # e o FOR não consegue percorrer toda coluna
    
    #df1  = df1.reset_index(drop=True)
    # como o comando reset_index criar uma coluna adicional INDEX o comando DROP=TRUE exclui essa coluna
    #for i in range (42805):
    #df1.loc[i, 'ID'] = df1.loc[i, 'ID'].strip()
    # a função STRIP remove o espaço em branco
    
    # 6 - Removendo os espaçoes dentro de stnings/text/object
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()
    
    # 7 - Limpado a coluna de time_taken
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min) ')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    return df1

# ==================== INICIO DA ESTRUTURA LOGICA DO CODIGO ====================
    
# ================================================
# IMPORT DATASET
# ================================================

df = pd.read_csv('dataset/train.csv')


# ================================================
# LIMPEZA DOS DADOS
# ================================================
df1 = clean_code(df)

    
# ================================================
# VISAO EMRPESA
# ================================================

# colunas
cols = ['ID', 'Order_Date']

# selecao de linhas
df_aux = df1.loc[:, cols].groupby('Order_Date').count().reset_index()

#desenhar o grafico de linhas
import plotly.express as px
px.bar(df_aux, x='Order_Date', y='ID')


# ==================================================
# Barra Lateral
# ===================================================

st.header('Marketplace - Visão Cliente')

#image_path = 'C:/repos/ftc_programacao_python\logo.png' 
image = Image.open('logo.png')
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Cury Company') # o simbolo '#' níveis de fonte -  # titulo, ## subtitulo)
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown('''___''')

#st.sidebar.markdown('## Selecione uma data limite')

#date_slider = st.sidebar.slider(
    #   'Até qual valor?',
       # value=pd.to_datetime(2022, 4, 13),
       # min_value=pd.to_datetime(2022, 2, 11),
      # max_value=pd.to_datetime(2022, 4, 6),
      # # format='DD-MM-YYYY')
#

st.sidebar.markdown("""___""")

traffic_option = st.sidebar.multiselect(
        'Quais as condições do trânsito?',
        ['Low', 'Medium', 'High', 'Jam'],
        default=['Low'] )

st.sidebar.markdown("""___""")
st.sidebar.markdown('### Powered by Dario')

# filtro de data
#linhas_selecionadas = df1['Order_Date'] < date_slider
#df1 = df1.loc[linhas_selecionadas, :]

# filtro de transito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_option)
df1 = df1.loc[linhas_selecionadas, :]


# ================================================
# LAYOUT STREAMLIT
# ================================================

tab1, tab2, tab3 = st.tabs (['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1: # tudo que tiver identado dentro do tab1, vai ficar dentro do tab1
    with st.container():
        # Order Metric
        fig = order_metric(df1)
        st.markdown('# Order by Day')
        st.plotly_chart(fig, user_container_width=True)
        # colunas   
        
    with st.container():
        col1, col2 = st.columns (2) # vai criar 2 coluna no layout

        with col1:
            fig = traffic_order_share(df1)
            st.header('Traffic Order Share')
            st.plotly_chart(fig, use_container_width=True)            
            
            
        with col2:
            st.header('Traffic Order City')
            fig = traffic_order_city(df1)            
            st.plotly_chart(fig, use_container_width=True)
    

with tab2:
    with st.container():
        st.markdown("# Orde by week")
        fig = order_by_week(df1)
        st.plotly_chart(fig, use_containe_width=True)
       

    with st.container():
        st.markdown("# Order Share by week")
        fig = order_share_by_week(df1)
        st.plotly_chart(fig, use_container_width=True)
        
      


with tab3:
    st.markdown("# Country Maps")
    country_maps(df1)



                       






