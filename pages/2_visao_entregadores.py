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

st.set_page_config(page_title='Visão Entregadores', layout='wide')

# ================================================
# FUNÇÕES
# ================================================


            
def top_delivers(df1, top_asc):
    df2 = (df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
                .groupby( ['City', 'Delivery_person_ID'])
                .mean()
                .sort_values( ['City', 'Time_taken(min)'], ascending=False).reset_index() )
            
    df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
    df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)

    df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)

    return df3
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

    
#Import Dataset
df = pd.read_csv('dataset/train.csv')

# cleanning code
df1 = clean_code(df)


# ==================================================
# Barra Lateral
# ===================================================

st.header('Marketplace - Visão Entregadores')

#image_path = 'C:/repos/ftc_programacao_python\logo.png' 
image = Image.open('logo.png')
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Cury Company') # o simbolo '#' níveis de fonte -  # titulo, ## subtitulo)
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown('''___''')

st.sidebar.markdown('## Selecione uma data limite')

#date_slider = st.sidebar.slider(
#    'Até qual valor?',
#    value=pd.to_datetime(2022, 4, 13),
#    min_value=pd.to_datetime(2022, 2, 11),
#    max_value=pd.to_datetime(2022, 4, 6),
#    format='DD-MM-YYYY')


#st.sidebar.markdown("""___""")

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

tab1, tab2, tab3 = st.tabs (['Visão Gerencial', '__', '__'])

with tab1:
    with st.container():
        st.title('Overhall Metric')
        # cria as 4 colunas do layout e o comando gap é tipo um espaçamento entre as colunas
        col1, col2, col3, col4 = st.columns(4, gap='large')
        #para testar se as colunas foram criadas  no layout
        with col1:
            # A maior idade dos entregadores
            #st.subheader('Maior idade')
            maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
            col1.metric('Maior de idade', maior_idade)
            
        with col2:
            # A menor idade dos entregadores
            #st.subheader('Menor idade')
            menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
            col2.metric('Menor de idade', menor_idade)
            
        with col3:
            # A melhor condição do veiculos
            #st.subheader('Melhor condição do veiculo')
            melhor_condicao = df1.loc[:, 'Vehicle_condition'].max()
            col3.metric('Melhor condição', melhor_condicao)
            
        with col4:
            # A pior condição do veiculo
            #st.subheader('Pior condição do veiculo')
            pior_condicao = df1.loc[:, 'Vehicle_condition'].min()
            col4.metric('Pior condição', pior_condicao)

    with st.container():
        st.markdown("""___""")
        st.title('Avalicoes')

        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(' ##### Avaliacoes medias por entregador')
            df_avg_ratings_per_deliver=(df1.loc[:, ['Delivery_person_Ratings', 'Delivery_person_ID']]
                                        .groupby('Delivery_person_ID')
                                        .mean()
                                        .reset_index())
            st.dataframe(df_avg_ratings_per_deliver)
                                            

        with col2:
            st.markdown(' ##### Avaliacao media por transito')
            df_avg_std_rating_by_traffic=(df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']]
                                            .groupby('Road_traffic_density')
                                            .agg( {'Delivery_person_Ratings':['mean', 'std']} ))
            # mudança de nome das colunas
            df_avg_std_rating_by_traffic.columns=['delivery_mean', 'delivery_std']

            # reset do index
            df_avg_std_rating_by_traffic=df_avg_std_rating_by_traffic.reset_index()
            st.dataframe(df_avg_std_rating_by_traffic)
            
            
            st.markdown(' ##### Avaliacao media por clima')
            df_avg_std_rating_by_weather=(df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']]
                                            .groupby('Weatherconditions')
                                            .agg( {'Delivery_person_Ratings':['mean', 'std']} ))
            # mudança de nome das colunas
            df_avg_std_rating_by_weather.columns=['delivery_mean', 'delivery_std']

            # reset do index
            df_avg_std_rating_by_weather=df_avg_std_rating_by_weather.reset_index()
            st.dataframe(df_avg_std_rating_by_weather)
            

    with st.container():
        st.markdown("""___""")
        st.title('Velocidade de entrega')

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('##### Top entregadores mais rápidos')
            df3 = top_delivers(df1, top_asc=True)
            st.dataframe(df3)
            

        with col2:
            st.markdown('##### Top entregadores mais lentos')
            df3 = top_delivers(df1, top_asc=False)        
            st.dataframe(df3)



            











































            
