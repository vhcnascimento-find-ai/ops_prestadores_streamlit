import streamlit as st
import folium
from folium.plugins import MarkerCluster
import pandas as pd
from streamlit_folium import st_folium

# Carregar os dados
# Substitua pelo caminho correto do arquivo CSV
@st.cache_data
def carregar_dados():
    # Exemplo: tb_estab_sp_hospital = pd.read_csv('tb_estab_sp_hospital.csv')
    # Substitua pelo caminho correto do arquivo
    return pd.read_csv('tb_estab_sp_hospital.csv')

tb_estab_sp_hosp = carregar_dados()

# Converter colunas de latitude e longitude para float
tb_estab_sp_hosp['NU_LATITUDE'] = tb_estab_sp_hosp['NU_LATITUDE'].astype(float)
tb_estab_sp_hosp['NU_LONGITUDE'] = tb_estab_sp_hosp['NU_LONGITUDE'].astype(float)

# Criar o filtro no Streamlit
st.title("Mapa de Estabelecimentos Hospitalares")
zona_cidade = st.selectbox(
    "Selecione a zona desejada:",
    options=["Todos"] + tb_estab_sp_hosp['ZONA_SP'].unique().tolist()
)

# Filtrar os dados com base no tipo selecionado
if zona_cidade != "Todos":
    tb_estab_sp_hosp = tb_estab_sp_hosp[tb_estab_sp_hosp['ZONA_SP'] == zona_cidade]

# Criar um mapa centralizado na média das coordenadas
latitude_media = tb_estab_sp_hosp['NU_LATITUDE'].mean()
longitude_media = tb_estab_sp_hosp['NU_LONGITUDE'].mean()

mapa = folium.Map(location=[latitude_media, longitude_media], zoom_start=10)

# Adicionar um cluster de marcadores
marker_cluster = MarkerCluster().add_to(mapa)

# Adicionar os pontos ao mapa
for _, row in tb_estab_sp_hosp.iterrows():
    folium.Marker(
        location=[row['NU_LATITUDE'], row['NU_LONGITUDE']],
        popup=row.get('NO_FANTASIA', 'Sem Nome')  # Substitua pela coluna desejada
    ).add_to(marker_cluster)

# Exibir o mapa no Streamlit
st_data = st_folium(mapa, width=700, height=500)