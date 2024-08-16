import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from PIL import Image
import math
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Configurando a página
st.set_page_config(
    page_title="Intervalo de Confiança e Teste de Hipótese", 
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


# Página 6 - Intervalo de Confiança e Teste de Hipótese

# Lista de amostras para seleção
amostras = {
    "Base Completa": base_completa,
    "Amostra Simples": amostra_simples,
    "Amostra Sistemática": amostra_sistematica,
    "Amostra por Grupos": amostra_grupos,
    "Amostra Estratificada": amostra_estratificada
}

st.title("INTERVALO DE CONFIANÇA E TESTE DE HIPÓTESE")
st.subheader("Selecione a amostra no sidebar para visualizar as medidas de posição e dispersão")

info_placeholder = st.empty()

# Selecionar amostra
base_selecionada_key = st.sidebar.selectbox("Selecione a Base:", list(amostras.keys()))
amostra_selecionada = amostras[base_selecionada_key]

# Sidebar para selecionar a coluna de amostra
amostra_coluna = st.sidebar.selectbox("Selecione a Amostra", amostra_selecionada.columns[1:], index=0)

# Sidebar para selecionar o tipo de célula
tipos_de_celula = amostra_selecionada["Tipo de Célula"].unique()
tipo_de_celula_selecionado = st.sidebar.selectbox("Selecione o Tipo de Célula", tipos_de_celula)

st.header(f"Tabela selecionada: {base_selecionada_key}. ")
st.header(f"Nº de linhas e colunas {amostra_selecionada.shape}")

# Mostrar a tabela selecionada no sidebar
info_placeholder.write(amostra_selecionada)

# SEPARANDO O TÍTULO E O SUBTÍTULO COM UMA LINHA
st.markdown(
    "<hr style='border: 1px solid cyan;'>",
    unsafe_allow_html=True
)

# Intervalo de Confiança

# Função para o usuário selecionar o valor de alpha
def alpha():
    alpha = st.sidebar.number_input("Digite o valor de alpha", min_value=0.01, max_value=0.1, value=0.05, step=0.01)
    return alpha

# Função para calcular o intervalo de confiança
def intervalo_de_confianca(amostra, alpha):
    media = amostra.mean()
    desvio_padrao = amostra.std()
    n = len(amostra)
    z = stats.norm.ppf(1 - alpha / 2)
    erro_padrao = desvio_padrao / math.sqrt(n)
    margem_de_erro = z * erro_padrao
    inferior = media - margem_de_erro
    superior = media + margem_de_erro
    return inferior, superior

# Colocando o intervalo de confiança no sidebar
st.sidebar.markdown("### Intervalo de Confiança")
alpha = alpha()
inferior_1, superior_1 = intervalo_de_confianca(amostra_selecionada[amostra_coluna], alpha)

# Imprimindo o intervalo de confiança
st.title("Intervalo de Confiança e Teste T de Student")
# SEPARANDO O TÍTULO E O SUBTÍTULO COM UMA LINHA
st.markdown(
    "<hr style='border: 1px solid cyan;'>",
    unsafe_allow_html=True
)

# INTERVALO DE CONFIANÇA COM SCIPY
# Função para calcular o intervalo de confiança com scipy
def intervalo_de_confianca_scipy(amostra, alpha):
    inferior, superior = stats.norm.interval(1 - alpha, loc=amostra.mean(), scale=amostra.std())
    return inferior, superior

# Colocando o intervalo de confiança no sidebar
inferior, superior = intervalo_de_confianca_scipy(amostra_selecionada[amostra_coluna], alpha)

# Função para criar um card
def create_card(title, value, description):
    card_html = f"""
    <div style='display: flex; flex-direction: column; align-items: center; justify-content: center; 
                border: 1px solid #e6e6e6; border-radius: 10px; padding: 10px; margin: 10px; 
                box-shadow: 0 4px 8px rgba(0,0,0,0.1); background-color: white; width: 250px;'>
        <h3 style='margin: 0; color: #4CAF50;'>{title}</h3>
        <h2 style='margin: 10px 0; color: #333;'>{value}</h2>
        <p style='margin: 0; color: #666;'>{description}</p>
    </div>
    """
    return card_html


# Criando a função para o teste t de student
def teste_t_student(amostra, amostra_selecionada, alpha):
    amostra_selecionada = amostra_selecionada[amostra]
    media = amostra_selecionada.mean()
    desvio_padrao = amostra_selecionada.std()
    n = len(amostra_selecionada)
    t = stats.t.ppf(1 - alpha / 2, n - 1)
    erro_padrao = desvio_padrao / math.sqrt(n)
    margem_de_erro = t * erro_padrao
    inferior = media - margem_de_erro
    superior = media + margem_de_erro
    return inferior, superior
alpha = alpha
inferior_2, superior_2 = teste_t_student(amostra_coluna, amostra_selecionada, alpha)


# Criando a função para teste de hipotese z
def teste_hipotese_z(amostra, amostra_selecionada, alpha):
    amostra_selecionada = amostra_selecionada[amostra]
    media = amostra_selecionada.mean()
    desvio_padrao = amostra_selecionada.std()
    n = len(amostra_selecionada)
    z = stats.norm.ppf(1 - alpha / 2)
    erro_padrao = desvio_padrao / math.sqrt(n)
    margem_de_erro = z * erro_padrao
    inferior = media - margem_de_erro
    superior = media + margem_de_erro
    return inferior, superior

alpha = alpha
inferior_3, superior_3 = teste_hipotese_z(amostra_coluna, amostra_selecionada, alpha)

col1, col2, col3, col4 = st.columns(4)

# Imprimindo o intervalo de confiança com Scipy em um card
st.markdown("<div style='display: flex; justify-content: center; flex-wrap: wrap;'>", unsafe_allow_html=True)
intervalo_conf = f"{inferior_1:.2f} - {superior_1:.2f}"

with col1:
    st.markdown(create_card("Intervalo de Confiança", intervalo_conf, f"Intervalo de confiança para alpha={alpha}"), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Imprimindo o intervalo de confiança com Scipy em um card
st.markdown("<div style='display: flex; justify-content: center; flex-wrap: wrap;'>", unsafe_allow_html=True)
intervalo_conf = f"{inferior:.2f} - {superior:.2f}"
with col2:
    st.markdown(create_card("Intervalo de Confiança com Scipy", intervalo_conf, f"Intervalo de confiança para alpha={alpha}"), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='display: flex; justify-content: center; flex-wrap: wrap;'>", unsafe_allow_html=True)
teste_t = f"{inferior_2:.2f} - {superior_2:.2f}"
with col3:
    st.markdown(create_card("Teste T de Student", teste_t, f"Teste T de Student para alpha={alpha}"), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='display: flex; justify-content: center; flex-wrap: wrap;'>", unsafe_allow_html=True)
teste_z = f"{inferior_3:.2f} - {superior_3:.2f}"
with col4:
    st.markdown(create_card("Teste de Hipótese Z", teste_z, f"Teste de Hipótese Z para alpha={alpha}"), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# SEPARANDO O TÍTULO E O SUBTÍTULO COM UMA LINHA
st.markdown(
    "<hr style='border: 1px solid cyan;'>",
    unsafe_allow_html=True
)
# Filtrando os dados para a coluna de amostra selecionada
dados_filtrados = amostra_selecionada[["Tipo de Célula", amostra_coluna]]



# TESTE DE HIPOTESE ANOVA!!

# Função para o teste de hipótese ANOVA
def teste_de_hipotese_anova(amostra_selecionada, amostra_coluna, tipo_de_celula_selecionado):
    grupo_1 = amostra_selecionada[amostra_selecionada["Tipo de Célula"] == tipo_de_celula_selecionado][amostra_coluna]
    grupo_2 = amostra_selecionada[amostra_selecionada["Tipo de Célula"] != tipo_de_celula_selecionado][amostra_coluna]
    _, p_value = stats.f_oneway(grupo_1, grupo_2)
    return p_value

# Calculando o p-valor
p_value_anova = teste_de_hipotese_anova(dados_filtrados, amostra_coluna, tipo_de_celula_selecionado)

# Imprimindo o p-valor para o teste ANOVA
st.header(f"O p-valor para o teste de hipótese ANOVA é {p_value_anova:.4f}")

# Separando o título e o subtítulo com uma linha
st.markdown("<hr style='border: 1px solid cyan;'>", unsafe_allow_html=True)

# Função para o teste de Tukey
def teste_de_tukey(amostra_selecionada, amostra_coluna, alpha):
    tukey_result = pairwise_tukeyhsd(endog=amostra_selecionada[amostra_coluna], groups=amostra_selecionada['Tipo de Célula'], alpha=alpha)
    return tukey_result

# Calculando o resultado do teste de Tukey
tukey_result = teste_de_tukey(dados_filtrados, amostra_coluna, alpha)

# Imprimindo o resultado do teste de Tukey
st.markdown("Resultados do teste de Tukey:")
st.text(tukey_result)

# Separando o título e o subtítulo com uma linha
st.markdown("<hr style='border: 1px solid cyan;'>", unsafe_allow_html=True)

