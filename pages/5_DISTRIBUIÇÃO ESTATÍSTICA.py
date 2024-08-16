# DISTRIBUIÇÃO DE FREQUÊNCIA

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from PIL import Image
import math

# Configurando a página
st.set_page_config(
    page_title="Distribuição Estatística", 
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

# Página 5 - Distribuição Estatística

# Lista de amostras para seleção
amostras = {
    "Base Completa": base_completa,
    "Amostra Simples": amostra_simples,
    "Amostra Sistemática": amostra_sistematica,
    "Amostra por Grupos": amostra_grupos,
    "Amostra Estratificada": amostra_estratificada
}

st.title("DISTRIBUIÇÃO ESTATÍSTICA DOS DADOS")
st.subheader("Selecione a amostra no sidebar para visualizar a distribuição estatística")

info_placeholder = st.empty()

# Selecionar amostra
amostra_selecionada_key = st.sidebar.selectbox("Selecione a Base:", list(amostras.keys()))
amostra_selecionada = amostras[amostra_selecionada_key]

# Sidebar para selecionar a coluna de amostra
amostra_coluna = st.sidebar.selectbox("Selecione a Amostra", amostra_selecionada.columns[1:], index=0)

# Sidebar para selecionar o tipo de célula
tipos_de_celula = amostra_selecionada["Tipo de Célula"].unique()
tipo_de_celula_selecionado = st.sidebar.selectbox("Selecione o Tipo de Célula", tipos_de_celula)

st.header(f"Tabela selecionada: {amostra_selecionada_key}. ")
st.header(f"Nº de linhas e colunas {amostra_selecionada.shape}")

# Mostrar a tabela selecionada no sidebar
info_placeholder.write(amostra_selecionada)

# SEPARANDO O O TITULO E O SUBTITULO COM UMA LINHA
st.markdown(
    "<hr style='border: 1px solid cyan;'>",
    unsafe_allow_html=True
)


# DISTRIBUIÇÃO ESTATÍSTICAS

st.title(f"DISTRIBUIÇÃO DA BASE DE DADOS: {amostra_selecionada_key}")
st.subheader("Selecione a amostra no sidebar para visualizar a distribuição estadística")

# Função do histograma com cores personalizáveis
def histograma(df, coluna):
    fig, ax = plt.subplots()
    sns.histplot(df[coluna], kde=True, ax=ax, color="#00ffff")
    kde_line = ax.lines[0]
    kde_line.set_color("#00ffff")
    
    # Definindo o título e as cores dos rótulos dos eixos
    ax.set_title(f"Histograma da coluna {coluna}", color="#ffffff")
    ax.set_xlabel(coluna, color="#ffffff")
    ax.set_ylabel('Frequência', color="#ffffff")
    
    # Definindo as cores das legendas dos eixos
    ax.tick_params(axis='x', colors="#ffffff")
    ax.tick_params(axis='y', colors="#ffffff")

    # Adicionando as 4 bordas ao plot
    ax.spines['bottom'].set_color('#00ffff')
    ax.spines['top'].set_color('#00ffff')
    ax.spines['right'].set_color('#00ffff')
    ax.spines['left'].set_color('#00ffff')
    
    ax.set_facecolor("#000000")
    ax.legend(['KDE'], facecolor="#000000", edgecolor='none', fontsize='large')
    plt.setp(ax.get_legend().get_texts(), color="#ffffff")
    fig.patch.set_facecolor("#000000")
    st.pyplot(fig)


# Botão para plotar o histograma
histograma(amostra_selecionada, amostra_coluna)

# SEPARANDO O O TITULO E O SUBTITULO COM UMA LINHA
st.markdown(
    "<hr style='border: 1px solid cyan;'>",
    unsafe_allow_html=True
)

# DISTRIBUIÇÃO ESTATÍSTICAS - Tipo de célula

st.title(f"Distribuição Estatísticas: {amostra_selecionada_key}, Tipo de Célula: {tipo_de_celula_selecionado}, Coluna: {amostra_coluna}")
st.subheader("Selecione o tipo de célula no sidebar para visualizar a distribuição estatística")

# Função do histograma
def histograma_tipo_de_celula(df, coluna, tipo_de_celula):
    fig, ax = plt.subplots()
    sns.histplot(df[df["Tipo de Célula"] == tipo_de_celula][coluna], kde=True, ax=ax, color="#00ffff")
    ax.set_title(f"Histograma da coluna {coluna} para o tipo de célula {tipo_de_celula}")
    
    # Definindo o título e as cores dos rótulos dos eixos
    ax.set_title(f"Histograma da coluna {coluna} do Tipo de Célula {tipo_de_celula_selecionado}", color="#ffffff")
    ax.set_xlabel(coluna, color="#ffffff")
    ax.set_ylabel('Frequência', color="#ffffff")
    
    # Definindo as cores das legendas dos eixos
    ax.tick_params(axis='x', colors="#ffffff")
    ax.tick_params(axis='y', colors="#ffffff")

    # Adicionando as 4 bordas ao plot
    ax.spines['bottom'].set_color('#00ffff')
    ax.spines['top'].set_color('#00ffff')
    ax.spines['right'].set_color('#00ffff')
    ax.spines['left'].set_color('#00ffff')
    
    ax.set_facecolor("#000000")
    ax.legend(['KDE'], facecolor="#000000", edgecolor='none', fontsize='large')
    plt.setp(ax.get_legend().get_texts(), color="#ffffff")
    fig.patch.set_facecolor("#000000")
    st.pyplot(fig)

# plotando o histograma
histograma_tipo_de_celula(amostra_selecionada, amostra_coluna, tipo_de_celula_selecionado)


# SEPARANDO O O TITULO E O SUBTITULO COM UMA LINHA
st.markdown(
    "<hr style='border: 1px solid cyan;'>",
    unsafe_allow_html=True
)

# DISTRIBUIÇÃO ESTATÍSTICAS - PLOTANDO TODOS OAS GRÁFICOS DE UMA VEZ DO TIPO DE CÉLULA

st.title("Distribuição Estatísticas - Todos os tipos de célula")

# Função do histograma por tipo de célula
def histograma_por_tipo_de_celula(df, coluna):
    tipos_de_celula = df["Tipo de Célula"].unique()
    num_tipos = len(tipos_de_celula)
    num_colunas = 3
    num_linhas = math.ceil(num_tipos / num_colunas)
    
    fig, axes = plt.subplots(num_linhas, num_colunas, figsize=(15, 5 * num_linhas))
    axes = axes.flatten()
    
    for ax, tipo in zip(axes, tipos_de_celula):
        sns.histplot(df[df["Tipo de Célula"] == tipo][coluna], kde=True, ax=ax, color="#00ffff")
        ax.set_title(f"Tipo de célula: {tipo}", color="#ffffff")
        ax.set_xlabel(coluna, color="#ffffff")
        ax.set_ylabel("Frequência", color="#ffffff")
        
        # Definindo as cores das legendas dos eixos
        ax.tick_params(axis='x', colors="#ffffff")
        ax.tick_params(axis='y', colors="#ffffff")

        # Adicionando as 4 bordas ao plot
        ax.spines['bottom'].set_color('#00ffff')
        ax.spines['top'].set_color('#00ffff')
        ax.spines['right'].set_color('#00ffff')
        ax.spines['left'].set_color('#00ffff')
        
        ax.set_facecolor("#000000")
        ax.legend(['KDE'], facecolor="#000000", edgecolor='none', fontsize='large')
        plt.setp(ax.get_legend().get_texts(), color="#ffffff")
    
    for ax in axes[num_tipos:]:
        fig.delaxes(ax)
    
    fig.patch.set_facecolor("#000000")
    plt.tight_layout()
    st.pyplot(fig)

# Plotando o histograma
histograma_por_tipo_de_celula(amostra_selecionada, amostra_coluna)