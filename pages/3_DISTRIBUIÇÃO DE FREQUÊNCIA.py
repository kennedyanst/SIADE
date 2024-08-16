import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# Configurando a página
st.set_page_config(
    page_title="Distribuição de Frequência", 
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

# Lista de amostras para seleção
amostras = {
    "Base Completa": base_completa,
    "Amostra Simples": amostra_simples,
    "Amostra Sistemática": amostra_sistematica,
    "Amostra por Grupos": amostra_grupos,
    "Amostra Estratificada": amostra_estratificada
}

# Página 3 - Seleção de Amostras e Distribuição de Frequência
st.title("DISTRIBUIÇÃO DE FREQUÊNCIA")

# Selecionar a amostra no sidebar
amostra_selecionada = st.sidebar.selectbox("Selecione a Base:", list(amostras.keys()))

def remover_colunas_com_strings(df):
    return df.select_dtypes(exclude='object')

# CONVERTENDO AS COLUNAS PARA NÚMEROS
#amostras[amostra_selecionada] = amostras[amostra_selecionada].apply(pd.to_numeric, errors='coerce')

# Função para substituir valores vazios pela média
def substituir_vazios_por_media(df):
    df = remover_colunas_com_strings(df)
    return df.fillna(df.mean())

# Função para substituir valores vazios pela mediana
def substituir_vazios_por_mediana(df):
    df = remover_colunas_com_strings(df)
    return df.fillna(df.median())

# Função para substituir valores vazios pela moda
def substituir_vazios_por_moda(df):
    df = remover_colunas_com_strings(df)
    return df.fillna(df.mode().iloc[0])

# Função para substituir valores vazios por zero
def substituir_vazios_por_zero(df):
    df = remover_colunas_com_strings(df)
    return df.fillna(0)

col1, col2, col3, col4 = st.columns(4)

# CRIANDO OS BOTÕES PARA CHAMAR AS FUNÇÕES

# BOTÃO PARA SUBSTITUIR VALORES VAZIOS PELA MÉDIA
with col1:
    if st.button("Substituir valores vazios pela média", key="media"):
        amostras[amostra_selecionada] = substituir_vazios_por_media(amostras[amostra_selecionada])

# BOTÃO PARA SUBSTITUIR VALORES VAZIOS PELA MEDIANA
with col2:
    if st.button("Substituir valores vazios pela mediana", key="mediana"):
        amostras[amostra_selecionada] = substituir_vazios_por_mediana(amostras[amostra_selecionada])

# BOTÃO PARA SUBSTITUIR VALORES VAZIOS PELA MODA
with col3:
    if st.button("Substituir valores vazios pela moda", key="moda"):
        amostras[amostra_selecionada] = substituir_vazios_por_moda(amostras[amostra_selecionada])

# BOTÃO PARA SUBSTITUIR VALORES VAZIOS POR ZERO
with col4:
    if st.button("Substituir valores vazios por zero", key="zero"):
        amostras[amostra_selecionada] = substituir_vazios_por_zero(amostras[amostra_selecionada])



# Removendo colunas com valores vazios
amostras[amostra_selecionada] = amostras[amostra_selecionada].dropna(axis=1, how='all')



# Exibir a amostra selecionada
st.write(f"Amostra Selecionada: {amostra_selecionada}. Arquivo com {len(amostras[amostra_selecionada])} linhas e {len(amostras[amostra_selecionada].columns)} colunas.")
st.write(amostras[amostra_selecionada])

# Botão para salvar a amostra
if st.button("Salvar Amostra"):
    st.session_state[amostra_selecionada] = amostras[amostra_selecionada]
    st.write("Amostra salva com sucesso!")


# DISTRIBUIÇÃO DE FREQUENCIA

# FUNÇÃO PARA CALCULAR A APLITUDE DA TABELA SELECIONADA
def amplitude_tabela(tabela):
    tabela = remover_colunas_com_strings(tabela)
    return tabela.iloc[-1, 0] - tabela.iloc[0, 0]

# FUNÇÃO PARA CALCULAR A AMPLITUDE DO INTERVALO
def amplitude_intervalo(tabela):
    tabela = remover_colunas_com_strings(tabela)
    return tabela.iloc[1, 0] - tabela.iloc[0, 0]

# FUNÇÃO PARA CALCULAR O NÚMERO DE CLASSES
def numero_classes(coluna):
    # Se uma coluna str for selecionada aparecer uma mensagem de erro:
    if coluna.dtype == 'object':
        return "Selecione uma coluna numérica"

    n = len(coluna)
    k = int(1 + 3.322 * np.log10(n))
    bins = pd.cut(coluna, bins=k, retbins=True)[1]
    return k, bins


col1, col2, col3 = st.columns(3)




# CRIANDO OS BOTÕES PARA CHAMAR AS FUNÇÕES

# BOTÃO PARA AMPLITUDE DA TABELA
with col1:
    if st.button("Amplitude da Tabela"):
        st.write(f"A amplitude da tabela é: {amplitude_tabela(amostras[amostra_selecionada])}")


# BOTÃO PARA AMPLITUDE DO INTERVALO
with col2:
    if st.button("Amplitude do Intervalo"):
        st.write(f"A amplitude do intervalo é: {amplitude_intervalo(amostras[amostra_selecionada])}")


# BOTÃO PARA SELECIONAR A COLUNA
coluna = st.sidebar.selectbox("Selecione a coluna para calcular o número de classes", amostras[amostra_selecionada].columns, key="coluna")



with col3:
    if st.button("Número de Classes"):
        resultado = numero_classes(amostras[amostra_selecionada][coluna])
        if isinstance(resultado, str):
            st.write(resultado)
        else:
            num_classes, classes = resultado
            st.write(f"O número de classes da coluna {coluna} é: {num_classes}")
            st.write("As classes são: ")
            for i in range(len(classes) - 1):
                st.write(f"Classe {i+1}: {classes[i]} - {classes[i+1]}")



