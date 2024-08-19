# Importando as Bibliotecas

import streamlit as st
import pandas as pd
from PIL import Image
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv


# Configurando a página
st.set_page_config(
    page_title="Início", 
    layout="wide",
    page_icon="./favicon_io/favicon.ico"

    )

#Adicionando CSS para ajustar o tamanho dos botões
with open("css/estilo.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Criando a página
logo_udf = Image.open("logo_udf_online_branco.png")
st.sidebar.image(logo_udf, use_column_width=True)
#st.sidebar.markdown("Centro Universitário do Distrito Federal")
st.sidebar.markdown(
    "<hr style='border: 1px solid cyan;'>",
    unsafe_allow_html=True
)
logo_fap = Image.open("fap.jpg")
st.sidebar.image(logo_fap, use_column_width=True)

#TÍTULO
st.title("S.I.A.D.E - Sistema de Análise de Dados e Estatística")

# Descrição
st.header("Este é um aplicativo para análise de dados e validação estatística de hipóteses. Contendo 7 páginas: **Base**, **Amostragem**, **Distribuição de Frequência**, **Posição e Dispersão**, **Distribuição Estatística**, **Intervalo de Confiança e Teste de Hipótese**, e **Visualização**. Cada uma dessas páginas contém diferentes tipos de ferramentas matemáticas para análise de dados.")

st.header("O modelo de tabela deve ser o seguinte:")

# Exemplo de tabela no modelo especificado
data = {
    'Tipo de Célula': ['A', 'B', 'C', 'D'],
    'Amostra 1': [10, 20, 30, 40],
    'Amostra 2': [5.5, 15.5, 25.5, 35.5],
    'Amostra 3': [100, 200, 300, 400],
    'Amostra 4': [50, 150, 250, 350],
    'Amostra 5': [25, 75, 125, 175],
    'Amostra 6': [12.5, 37.5, 62.5, 87.5],
    'Amostra 7': [15, 45, 75, 105],
    'Amostra 8': [7.5, 22.5, 37.5, 52.5],
    'Amostra 9': [3.75, 11.25, 18.75, 26.25],
    'Amostra 10': [1.875, 5.625, 9.375, 13.125]
}

df = pd.DataFrame(data)

# Exibindo a tabela de exemplo
st.markdown("### Exemplo de Tabela:")
st.write(df)
         

# Botão para selecionar um arquivo excel
st.markdown('<h2>Selecione Um Arquivo Excel (.xlsx) ou CSV (.csv) para Análise</h2>', unsafe_allow_html=True)

st.markdown('Arquivo CSV precisam ter o separador "," e o encoding "UTF-8".')



# Função para selecionar o arquivo
def selecionar_arquivo():
    arquivo = st.file_uploader("Escolha um arquivo Excel ou CSV.", type=["xlsx", "csv"], key="file_uploader")
    if arquivo is not None:
        if arquivo.name.endswith('.xlsx'):
            planilha = pd.ExcelFile(arquivo)
            st.write("Planilhas disponíveis:")
            for sheet in planilha.sheet_names:
                st.write(f"- {sheet}")
            sheet = st.selectbox("Selecione a planilha", planilha.sheet_names)
            df = planilha.parse(sheet)
        elif arquivo.name.endswith('.csv'):
            df = pd.read_csv(arquivo)
        st.session_state['arquivo'] = df
        st.write(df)
    else:
        st.write("Nenhum arquivo selecionado.")

# Função para carregar novamente um arquivo
def carregar_novo_arquivo():
    st.session_state.pop('arquivo')
    selecionar_arquivo()

# Carregando os dados e matendo o arquivo carregado na sessão / Criando uma função para carregar novo arquivo
if 'arquivo' not in st.session_state:
    selecionar_arquivo()
else:
    df = st.session_state['arquivo']
    st.write(df)

    # Função para carregar novo arquivo
    if st.button("Carregar novo arquivo"):
        carregar_novo_arquivo()	




# ORGANIZANDO O LAYOUT DOS BOTÕES E CRIANDO A TELA PARA VISUALIZAÇÃO DOS DADOS QUANDO OS BOTÕES FOREM SELECIONADOS
col1, col2, col3, col4 = st.columns(4)


# Espaço reservado para exibir as informações
info_placeholder = st.empty()

with col1:
    if st.button("Ver as 10 primeiras linhas"):
        info_placeholder.write(df.head(10))
    if st.button("Ver tipos de dados"):
        info_placeholder.write(df.dtypes)
with col2:
    if st.button("Ver as 10 últimas linhas"):
        info_placeholder.write(df.tail(10))
    if st.button("Ver estatísticas descritivas"):
        info_placeholder.write(df.describe())
with col3:
    if st.button("Nº de linhas e colunas"):
        info_placeholder.write(f"O ARQUIVO SELECIONADO TEM {df.shape[0]} LINHAS E {df.shape[1]} COLUNAS")
    if st.button("Ver colunas"):
        info_placeholder.write(df.columns)
with col4:
    if st.button("Nº de células em branca"):
        info_placeholder.write(df.isnull().sum())
    if st.button("Ver valores únicos"):
        info_placeholder.write(df.nunique())
