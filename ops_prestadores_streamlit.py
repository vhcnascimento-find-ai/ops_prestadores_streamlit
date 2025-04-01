import streamlit as st
import folium
from folium.plugins import MarkerCluster
import pandas as pd
from streamlit_folium import st_folium

# Carregar os dados
@st.cache_data
def carregar_dados():
    # Substitua pelo caminho absoluto do arquivo CSV
    return pd.read_csv('tb_estab_sp_filtrado.csv', encoding='latin1', sep=';')

tb_estab_sp_filtrado = carregar_dados()

# Converter colunas de latitude e longitude para float
tb_estab_sp_filtrado['NU_LATITUDE'] = tb_estab_sp_filtrado['NU_LATITUDE'].astype(float)
tb_estab_sp_filtrado['NU_LONGITUDE'] = tb_estab_sp_filtrado['NU_LONGITUDE'].astype(float)

# Título do aplicativo
st.title("Mapa de Estabelecimentos Hospitalares")

# Adicionar filtro por tipo de estabelecimento (sem a opção "Todos")
tipo_selecionado = st.selectbox(
    "Selecione o tipo de estabelecimento:",
    options=tb_estab_sp_hosp['DS_TIPO_ESTABELECIMENTO'].unique().tolist(),
    index=2
)

# Filtrar os dados com base no tipo selecionado
tb_estab_sp_filtrado = tb_estab_sp_filtrado[tb_estab_sp_filtrado['DS_TIPO_ESTABELECIMENTO'] == tipo_selecionado]

# Adicionar filtro por zona
zona_selecionada = st.selectbox(
    "Selecione uma zona da cidade:",
    options=["Todas"] + tb_estab_sp_filtrado['ZONA_SP'].unique().tolist(),
    index=2
)

# Filtrar os dados com base na zona selecionada
if zona_selecionada != "Todas":
    tb_estab_sp_filtrado = tb_estab_sp_filtrado[tb_estab_sp_filtrado['ZONA_SP'] == zona_selecionada]

# Criar um mapa centralizado na média das coordenadas
latitude_media = tb_estab_sp_filtrado['NU_LATITUDE'].mean()
longitude_media = tb_estab_sp_filtrado['NU_LONGITUDE'].mean()

mapa = folium.Map(location=[latitude_media, longitude_media], zoom_start=10)

# Adicionar um cluster de marcadores
marker_cluster = MarkerCluster().add_to(mapa)

# Adicionar os pontos ao mapa
for _, row in tb_estab_sp_filtrado.iterrows():
    folium.Marker(
        location=[row['NU_LATITUDE'], row['NU_LONGITUDE']],
        popup=row.get('NO_FANTASIA', 'Sem Nome')  # Substitua pela coluna desejada
    ).add_to(marker_cluster)

# Exibir o mapa no Streamlit
st_data = st_folium(mapa, width=700, height=500)

# Selecionar as colunas desejadas para exibição na tabela
colunas_tabela = ['CO_CNES', 'NO_FANTASIA', 'NO_LOGRADOURO', 'NU_ENDERECO', 'NO_COMPLEMENTO', 'CO_CEP', 'ZONA_SP', 'NU_TELEFONE', 'NO_EMAIL']
tabela_dados = tb_estab_sp_filtrado[colunas_tabela]

# Exibir a tabela abaixo do mapa
st.subheader("Detalhes dos Estabelecimentos")
st.dataframe(tabela_dados)