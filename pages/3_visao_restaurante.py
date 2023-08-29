# libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

#bibliotecas necessárias
import pandas as pd
import numpy as np
import streamlit as st # erro de st ao executar o streamlite
from PIL import Image #biblioteca para trabalhar com imagens
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title='Visão Restaurante', layout='wide')

# ================================================
# FUNÇÕES
# ================================================


def avg_std_time_on_traffic(df1):                    
    cols = ['City', 'Time_taken(min)', 'Road_traffic_density']
    df_aux = df1.loc[:, cols].groupby( [ 'City', 'Road_traffic_density']).agg({'Time_taken(min)' : ['mean', 'std']} )
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()

    fig=px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='avg_time',
                    color='std_time', color_continuous_scale='RdBu',
                    color_continuous_midpoint=np.average(df_aux['std_time'] ) )
    return fig


def avg_std_time_graph(df1):
    df_aux=df1.loc[:, ['City', 'Time_taken(min)']].groupby( 'City' ).agg( {'Time_taken(min)':['mean', 'std']})
    df_aux.columns=['avg_time', 'std_time']
    df_aux = df_aux.reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(name = 'Control', x = df_aux['City'], y = df_aux['avg_time'], error_y=dict(type = 'data', array=df_aux['std_time'])))
    fig.update_layout(barmode='group')
    return fig

def avg_std_time_delivery(df1, festival, op):

    """
    Esta função calcula o tempo medio e o desvio padrao do tempo de entrega.
    Parametros:
        Input:
            - df: Dataframe com os dados necessários para o calculo
            - op: tipo de operação que precisa ser calculado
                'avg_time': calcula o tempo medio
                'std_time': calcula o desvio padraõ do tempo
        Output:
            - df: Dataframe com 02 colunas e 01 linha.
    """
    cols=['Time_taken(min)', 'Festival']
    df_aux=df1.loc[:, cols].groupby('Festival').agg({'Time_taken(min)': ['mean', 'std']} )
    df_aux.columns=['avg_time', 'std_time'] # avg_time (tempo médio) / std_time (desvio padrão)
    df_aux=df_aux.reset_index()        
    df_aux=np.round(df_aux.loc[df_aux['Festival'] == 'Yes', 'avg_time'], 2) #np.round arredonda os números para 2 casas decimais neste caso
    return df_aux
    

def distance(df1, fig):
    if fig==False:
        cols=['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
        df1['distance']=df1.loc[:, cols].apply(lambda x: haversine( (x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude']) ), axis=1)
        avg_distance=np.round(df1['distance'].mean(), 2)
        return avg_distance

    else:
        cols=['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
        df1['distance']=df1.loc[:, cols].apply(lambda x: haversine( (x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude']) ), axis=1)
        avg_distance=df1.loc[:, ['City', 'distance']].groupby('City').mean().reset_index()
    
        fig=go.Figure(data=[go.Pie(labels=avg_distance['City'], values=avg_distance['distance'], pull=[0, 0.1, 0])]) # o comando pull configura a partição do pedaço em evidencia na pizza
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

#Import Dataset
df = pd.read_csv('dataset/train.csv')

# Cleaning code
df1=clean_code(df)



# ==================================================
# Barra Lateral
# ===================================================

st.header('Marketplace - Visão Restaurante')

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

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '_', '_'])

with tab1:
        with st.container():
            st.markdown("""___""")
            st.title("Overal Metrics")

            col1, col2, col3, col4, col5, col6 = st.columns (6)

            # A QUANTIDADE DE ENTREGADORES ÚNICOS            
            with col1:
                # st.markdown('##### Coluna 1')
                delivery_unique=len(df1.loc[:, 'Delivery_person_ID'].unique() )
                col1.metric('Entregadores unicos', delivery_unique)

            # A DISTANCIA MEDIA DOS RESTAURANTES E DOS LOCAIS DE ENTREGA
            with col2:
               # st.markdown('##### Coluna 2')
                avg_distance=distance(df1, fig=False)
                col2.metric('A distancia media das entregas', avg_distance)
             
              
            # TEMPO MÉDIO DE ENTREGA DURANTE OS FESTIVAIS
            with col3: 
                # st.markdown('##### Coluna 3')                
                df_aux = avg_std_time_delivery(df1, 'Yes','avg_time')
                col3.metric('Tempo médio de entrega c/ festival', df_aux)

            # DESVIO MEDIO PADRAO DE ENTREGA COM FESTIVAL
            with col4:
                #st.markdown('##### Coluna 4')
                df_aux = avg_std_time_delivery(df1, 'Yes', 'std_time')
                col4.metric('Desvio médio padrão de entrega c/ festival', df_aux)
                #cols=['Time_taken(min)', 'Festival']
                #df_aux=df1.loc[:, cols].groupby('Festival').agg({'Time_taken(min)': ['mean', 'std']} )
                #df_aux.columns=['avg_time', 'std_time'] # avg_time (tempo médio) / std_time (desvio padrão)
                #df_aux=df_aux.reset_index()        
                #df_aux=np.round(df_aux.loc[df_aux['Festival'] == 'Yes', 'std_time'], 2) #np.round arredonda os números para 2 casas decimais neste caso
                                

            # TEMPO MÉDIO DE ENTREGA SEM FESTIVAL
            with col5:
                #st.markdown('##### Coluna 5')
                df_aux = avg_std_time_delivery(df1, 'No', 'avg_time')
                col5.metric('Tempo médio de entrega s/ festival', df_aux)
                
                #cols=['Time_taken(min)', 'Festival']
                #df_aux=df1.loc[:, cols].groupby('Festival').agg({'Time_taken(min)': ['mean', 'std']} )
                #df_aux.columns=['avg_time', 'std_time'] # avg_time (tempo médio) / std_time (desvio padrão)
                #df_aux=df_aux.reset_index()        
                #df_aux=np.round(df_aux.loc[df_aux['Festival'] == 'No', 'avg_time'], 2) #np.round arredonda os números para 2 casas decimais neste caso
                
                
            # DESVIO MEDIO PADRAO DE ENTREGA SEM FESTIVAL
            with col6:
               # st.markdown('##### Coluna 6')
                df_aux = avg_std_time_delivery(df1, 'No', 'std_time')
                col6.metric('Desvio médio padrão de entrega s/ festival', df_aux)

                
                #ols=['Time_taken(min)', 'Festival']
                #df_aux=df1.loc[:, cols].groupby('Festival').agg({'Time_taken(min)': ['mean', 'std']} )
                #df_aux.columns=['avg_time', 'std_time'] # avg_time (tempo médio) / std_time (desvio padrão)
                #df_aux=df_aux.reset_index()        
                #df_aux=np.round(df_aux.loc[df_aux['Festival'] == 'No', 'std_time'], 2) #np.round arredonda os números para 2 casas decimais neste caso
                
                
         

        with st.container():
            st.markdown("""___""")
            st.title ("Distribuição do tempo")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""___""")
                fig=distance(df1, fig=True)
                st.plotly_chart(fig)      
                

            # O TEMPO MEDIO E O DESVIO PADRAO DE ENTREGA PÓR CIDADE E POR TIPO DE TRAFEGO
                with col2:
                    #st.markdown('##### col2')
                    fig=avg_std_time_on_traffic(df1)                        
                    st.plotly_chart(fig)
                
                
              
        with st.container():            
            st.markdown("""___""")
            col1, col2 = st.columns(2)
      
            # TEMPO MÉDIO E DESVIO PADRÃO DE ENTREGA POR CIDADE
            with col1:
                #st.markdown('##### col1')             
                    
                fig=avg_std_time_graph(df1)
                st.plotly_chart(fig)

            with col2:
                df_aux = (df1.loc[:, ['City', 'Time_taken(min)', 'Type_of_order']]
                        .groupby( ['City', 'Type_of_order'])
                        .agg( { 'Time_taken(min)' : ['mean', 'std'] } ))
                df_aux.columns = ['avg_time', 'std_time']
                df_aux = df_aux.reset_index()
                st.dataframe(df_aux)