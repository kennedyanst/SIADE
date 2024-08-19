import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image


# Configurando a página
st.set_page_config(
    page_title="Medidas de Posição e Dispersão", 
    layout="wide",
    page_icon="./favicon_io/favicon.ico"
)

#Adicionando CSS para ajustar o tamanho dos botões
with open("css/estilo.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Verifica se o arquivo foi carregado na sessão
if 'arquivo' in st.session_state:
    arquivo = st.session_state['arquivo']
else:
    st.error("Nenhum arquivo foi carregado. Por favor, volte à página 1 e carregue um arquivo.")
    st.stop()

logo_udf = Image.open("logo_udf_online_branco.png")
st.sidebar.image(logo_udf, use_column_width=True)
#st.sidebar.markdown("Centro Universitário do Distrito Federal")
st.sidebar.markdown(
    "<hr style='border: 1px solid cyan;'>",
    unsafe_allow_html=True
)
logo_fap = Image.open("fap.jpg")
st.sidebar.image(logo_fap, use_column_width=True)


# Supondo que as amostras já foram salvas na sessão
base_completa = st.session_state.get('arquivo', pd.DataFrame())
amostra_simples = st.session_state.get('amostra_simples', pd.DataFrame())
amostra_sistematica = st.session_state.get('amostra_sistematica', pd.DataFrame())
amostra_grupos = st.session_state.get('amostra_grupos', pd.DataFrame())
amostra_estratificada = st.session_state.get('amostra_estratificada', pd.DataFrame())


#Página 4 - Seleção de Amostras e Distribuição de Frequência

# Lista de amostras para seleção
amostras = {
    "Base Completa": base_completa,
    "Amostra Simples": amostra_simples,
    "Amostra Sistemática": amostra_sistematica,
    "Amostra por Grupos": amostra_grupos,
    "Amostra Estratificada": amostra_estratificada
}

st.title("MEDIDAS DE POSIÇÃO E DISPERSÃO")
st.subheader("Selecione a amostra no sidebar para visualizar as medidas de posição e dispersão")

info_placeholder = st.empty()

# Selecionar amostra
amostra_selecionada_key = st.sidebar.selectbox("Selecione a Base:", list(amostras.keys()))
amostra_selecionada = amostras[amostra_selecionada_key]

st.header(f"Tabela selecionada: {amostra_selecionada_key}. ")
st.header(f"Nº de linhas e colunas {amostra_selecionada.shape}")

# Mostrar a tabela selecionada no sidebar
info_placeholder.write(amostra_selecionada)

# Funções de medidas estatísticas
def media(df):
    return df.mean()

def mediana(df):
    return df.median()

def moda(df):
    return df.mode().iloc[0]

def quartis(df):
    return df.quantile([0.25, 0.5, 0.75])

def percentis(df):
    return df.quantile([0.1, 0.25, 0.5, 0.75, 0.9])

def amplitude(df):
    return df.max() - df.min()

def desvio_padrao(df):
    return df.std()

def variancia(df):
    return df.var()

def coeficiente_de_variacao(df):
    return df.std() / df.mean()

# SEPARANDO O O TITULO E O SUBTITULO COM UMA LINHA
st.markdown(
    "<hr style='border: 1px solid cyan;'>",
    unsafe_allow_html=True
)


# Imprimindo as medidas de posição dos tipos de célula em uma tabela
st.title("Medidas de Posição e Dispersão de Todas as células")

# Sidebar para selecionar a coluna de amostra
amostra_coluna = st.sidebar.selectbox("Selecione a Amostra", amostra_selecionada.columns[1:], index=0)

# Função para identificar colunas categóricas ou de string
def colunas_categoricas(df):
    return df.select_dtypes(include=['object', 'category']).columns

# Obtendo as colunas categóricas da amostra selecionada
colunas_cat = colunas_categoricas(amostra_selecionada)

# Sidebar para selecionar as colunas de filtro
filtros = {}
if len(colunas_cat) > 0:
    for coluna in colunas_cat:
        valores_unicos = amostra_selecionada[coluna].unique()
        valor_selecionado = st.sidebar.selectbox(f"Selecione um valor para {coluna}", valores_unicos)
        filtros[coluna] = valor_selecionado

# Filtrando os dados com base nos valores selecionados
dados_filtrados = amostra_selecionada.copy()
for coluna, valor in filtros.items():
    dados_filtrados = dados_filtrados[dados_filtrados[coluna] == valor]

# Verificar se o filtro resultou em uma amostra não vazia
if dados_filtrados.empty:
    st.write("Nenhum dado corresponde aos filtros selecionados.")
else:
    # Selecionar a coluna numérica para exibir as medidas estatísticas
    colunas_numericas = dados_filtrados.select_dtypes(include=['number']).columns
    amostra_coluna = st.sidebar.selectbox("Selecione a Coluna Numérica", colunas_numericas, index=0)

    # Agrupando os dados filtrados pelo tipo de célula
    grouped = dados_filtrados.groupby(colunas_cat[0])[amostra_coluna]  # Usando a primeira coluna categórica como agrupamento

    # Calculando as medidas estatísticas
    tabela = pd.DataFrame({
        "Média": grouped.apply(media),
        "Mediana": grouped.apply(mediana),
        "Moda": grouped.apply(moda),
        "1º Quartil": grouped.apply(lambda x: quartis(x).loc[0.25]),
        "3º Quartil": grouped.apply(lambda x: quartis(x).loc[0.75]),
        "Percentil 10%": grouped.apply(lambda x: percentis(x).loc[0.1]),
        "Percentil 90%": grouped.apply(lambda x: percentis(x).loc[0.9]),
        "Amplitude": grouped.apply(amplitude),
        "Desvio Padrão": grouped.apply(desvio_padrao),
        "Variância": grouped.apply(variancia),
        "Coeficiente de Variação": grouped.apply(coeficiente_de_variacao)
    })

    # Exibindo as medidas estatísticas
    st.write(tabela)

    # Medidas de posição e dispersão da coluna numérica para o valor de célula selecionado
    st.title(f"Medidas de Posição e Dispersão da {amostra_selecionada_key}, {amostra_coluna} do tipo de célula: {filtros[colunas_cat[0]]}")

    coluna = pd.DataFrame({
        "Média": [media(dados_filtrados[amostra_coluna])],
        "Mediana": [mediana(dados_filtrados[amostra_coluna])],
        "Moda": [moda(dados_filtrados[amostra_coluna])],
        "1º Quartil": [quartis(dados_filtrados[amostra_coluna]).loc[0.25]],
        "3º Quartil": [quartis(dados_filtrados[amostra_coluna]).loc[0.75]],
        "Percentil 10%": [percentis(dados_filtrados[amostra_coluna]).loc[0.1]],
        "Percentil 90%": [percentis(dados_filtrados[amostra_coluna]).loc[0.9]],
        "Amplitude": [amplitude(dados_filtrados[amostra_coluna])],
        "Desvio Padrão": [desvio_padrao(dados_filtrados[amostra_coluna])],
        "Variância": [variancia(dados_filtrados[amostra_coluna])],
        "Coeficiente de Variação": [coeficiente_de_variacao(dados_filtrados[amostra_coluna])]
    })

    # Exibindo as medidas estatísticas
    st.write(coluna)
