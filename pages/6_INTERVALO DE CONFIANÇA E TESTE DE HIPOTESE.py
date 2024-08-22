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
st.subheader("Selecione a base no barra lateral para visualizar as amostras disponíveis para o teste de hipótese e o intervalo de confiança.")

info_placeholder = st.empty()

# Selecionar amostra
base_selecionada_key = st.sidebar.selectbox("Selecione a Base:", list(amostras.keys()))
amostra_selecionada = amostras[base_selecionada_key]

# Sidebar para selecionar a coluna de amostra
amostra_coluna = st.sidebar.selectbox("Selecione a Amostra", amostra_selecionada.columns[1:], index=0)

# Sidebar para selecionar o tipo de célula
tipos_de_celula = amostra_selecionada["Tipo de Célula"].unique()
#tipo_de_celula_selecionado = st.sidebar.selectbox("Selecione o Tipo de Célula", tipos_de_celula)

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
    alpha = st.number_input("Digite o valor de alpha", min_value=0.01, max_value=0.1, value=0.05, step=0.01)
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

# Imprimindo o intervalo de confiança
st.title("Intervalo de Confiança e Teste T de Student")

# Colocando o intervalo de confiança no sidebar

col1, col2, col3 = st.columns(3)
with col1:
    alpha = alpha()
inferior_1, superior_1 = intervalo_de_confianca(amostra_selecionada[amostra_coluna], alpha)


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

# Criando a função para o teste T de Student
def teste_t_student(amostra_1, amostra_2, alpha):
    stat, p_value = stats.ttest_ind(amostra_1, amostra_2)
    return stat, p_value

# Criando a função para teste de hipótese Z
def teste_hipotese_z(amostra_1, amostra_2, alpha):
    n1 = len(amostra_1)
    n2 = len(amostra_2)
    media_1 = amostra_1.mean()
    media_2 = amostra_2.mean()
    variancia_1 = amostra_1.var()
    variancia_2 = amostra_2.var()
    
    # Estatística Z
    z = (media_1 - media_2) / np.sqrt((variancia_1 / n1) + (variancia_2 / n2))
    p_value = stats.norm.sf(abs(z)) * 2  # P-value bilateral
    return z, p_value

# Selecionando dois tipos de células para comparação


with col2:
    tipo_1 = st.selectbox("Selecione o primeiro tipo de célula para comparação", tipos_de_celula)
with col3:
    tipo_2 = st.selectbox("Selecione o segundo tipo de célula para comparação", [tipo for tipo in tipos_de_celula if tipo != tipo_1])


# Filtrando os dados para cada tipo de célula
amostra_1 = amostra_selecionada[amostra_selecionada["Tipo de Célula"] == tipo_1][amostra_coluna]
amostra_2 = amostra_selecionada[amostra_selecionada["Tipo de Célula"] == tipo_2][amostra_coluna]

# Calculando os resultados dos testes
stat_t, p_value_t = teste_t_student(amostra_1, amostra_2, alpha)
z_stat, p_value_z = teste_hipotese_z(amostra_1, amostra_2, alpha)

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
    st.markdown(create_card("Intervalo de Confiança (Scipy)", intervalo_conf, f"Intervalo de confiança para alpha={alpha}"), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Imprimindo o resultado do Teste T de Student em um card
stat_t_str = f"Stat: {stat_t:.2f}"
p_value_t_str = f"P-Value: {p_value_t:.4f}"

with col3:
    st.markdown(create_card("Teste T de Student", stat_t_str, p_value_t_str), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Imprimindo o resultado do Teste Z em um card
z_stat_str = f"Z-Stat: {z_stat:.2f}"
p_value_z_str = f"P-Value: {p_value_z:.4f}"

with col4:
    st.markdown(create_card("Teste de Hipótese Z", z_stat_str, p_value_z_str), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Mostra os resultados dos testes na tela
st.subheader("Visualização dos Dados")
st.write(f"Comparação entre as amostras do tipo de célula '{tipo_1}' e '{tipo_2}' na coluna '{amostra_coluna}'.")

# Plotando os gráficos de boxplot e histograma para as amostras
fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# Gráfico de boxplot
sns.boxplot(data=amostra_selecionada[amostra_selecionada["Tipo de Célula"].isin([tipo_1, tipo_2])], x="Tipo de Célula", y=amostra_coluna, ax=ax[0])
ax[0].set_title("Boxplot")

# Gráfico de histograma
sns.histplot(amostra_1, color='blue', kde=True, label=tipo_1, ax=ax[1])
sns.histplot(amostra_2, color='green', kde=True, label=tipo_2, ax=ax[1])
ax[1].legend(title="Tipo de Célula")
ax[1].set_title("Histograma")

st.pyplot(fig)




# TESTE DE HIPOTESE ANOVA!!

def teste_de_hipotese_anova_todos(dados_filtrados, amostra_coluna):
    p_values = {}
    tipos_de_celula = dados_filtrados["Tipo de Célula"].unique()

    for tipo in tipos_de_celula:
        grupo_1 = dados_filtrados[dados_filtrados["Tipo de Célula"] == tipo][amostra_coluna]
        grupo_2 = dados_filtrados[dados_filtrados["Tipo de Célula"] != tipo][amostra_coluna]
        _, p_value = stats.f_oneway(grupo_1, grupo_2)
        p_values[tipo] = p_value
    
    return p_values

# Calculando os p-valores para todos os tipos de células
p_values_anova = teste_de_hipotese_anova_todos(amostra_selecionada, amostra_coluna)

# Criando um DataFrame para exibir os resultados
resultados_anova = pd.DataFrame(list(p_values_anova.items()), columns=["Tipo de Célula", "P-VALOR ANOVA"]).sort_values(by="P-VALOR ANOVA")

# Exibindo a tabela com os p-valores ANOVA

# Separando o título e o subtítulo com uma linha
st.markdown("<hr style='border: 1px solid cyan;'>", unsafe_allow_html=True)
st.title(f"Resultados do teste de hipótese ANOVA: {amostra_coluna}")
st.table(resultados_anova)


# Separando o título e o subtítulo com uma linha
st.markdown("<hr style='border: 1px solid cyan;'>", unsafe_allow_html=True)

# Função para o teste de Tukey
def teste_de_tukey(amostra_selecionada, amostra_coluna, alpha):
    tukey_result = pairwise_tukeyhsd(endog=amostra_selecionada[amostra_coluna], groups=amostra_selecionada['Tipo de Célula'], alpha=alpha)
    return tukey_result

# Calculando o resultado do teste de Tukey
tukey_result = teste_de_tukey(amostra_selecionada, amostra_coluna, alpha)

# Imprimindo o resultado do teste de Tukey
st.title(f"Resultados do teste de Tukey: {amostra_coluna}")
st.text(tukey_result)

# Separando o título e o subtítulo com uma linha
st.markdown("<hr style='border: 1px solid cyan;'>", unsafe_allow_html=True)

