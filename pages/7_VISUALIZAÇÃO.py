import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from scipy.interpolate import make_interp_spline

# Configurando a página
st.set_page_config(
    page_title="Gráficos", 
    layout="wide",
    page_icon="./favicon_io/favicon.ico"
)

# Adicionando CSS para ajustar o tamanho dos botões
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
st.sidebar.markdown(
    "<hr style='border: 1px solid cyan;'>",
    unsafe_allow_html=True
)
logo_fap = Image.open("fap.jpg")
st.sidebar.image(logo_fap, use_column_width=True)

# Supondo que as amostras já foram salvas na sessão
base_completa = st.session_state.get('arquivo', pd.DataFrame())
amostra_simples = st.session_state.get('amostra_simples', pd.DataFrame())

# Lista de amostras para seleção
amostras = {
    "Base Completa": base_completa,
    "Amostra Simples": amostra_simples,
}

st.title("GRÁFICOS E VISUALIZAÇÕES")
st.subheader("Selecione a amostra no sidebar para criar os gráficos.")

info_placeholder = st.empty()

# Selecionar amostra
base_selecionada_key = st.sidebar.selectbox("Selecione a Base:", list(amostras.keys()))
amostra_selecionada = amostras[base_selecionada_key]

st.header(f"Tabela selecionada: {base_selecionada_key}. ")
st.header(f"Nº de linhas e colunas {amostra_selecionada.shape}")

# Mostrar a tabela selecionada no sidebar
info_placeholder.write(amostra_selecionada)

# Separando o título e o subtítulo com uma linha
st.markdown(
    "<hr style='border: 1px solid cyan;'>",
    unsafe_allow_html=True
)

# Gráfico de linhas
st.title("Gráfico de Linhas")

col1, col2 = st.columns(2)

# Selecionando os valores únicos da coluna "Tipo de Célula"
tipos_de_celula = amostra_selecionada["Tipo de Célula"].unique()
with col1:
    tipo_de_celula_selecionado = st.selectbox("Selecione o Tipo de Célula", tipos_de_celula)

# Filtrando a amostra selecionada pelo tipo de célula
amostra_filtrada = amostra_selecionada[amostra_selecionada["Tipo de Célula"] == tipo_de_celula_selecionado]

# Selecionando a amostra para o eixo y
with col2:
    amostra_coluna = st.selectbox("Selecione a Amostra", amostra_selecionada.columns[1:])

# Extraindo os valores categóricos e numéricos
tipos_de_celula = amostra_selecionada["Tipo de Célula"].values
valores_amostra = amostra_selecionada[amostra_coluna].values




# Separando o título e o subtítulo com uma linha
st.markdown(
    "<hr style='border: 1px dashed cyan;'>",
    unsafe_allow_html=True
)

# GRÁFICO DE AREA

# Criando a função para o Gráfico de área

def grafico_de_area(df, coluna, tipo_de_celula):
    fig, ax = plt.subplots()
    sns.kdeplot(df[df["Tipo de Célula"] == tipo_de_celula][coluna], fill=True, color="#00ffff", ax=ax)
    
    # Definindo o título e as cores dos rótulos dos eixos
    ax.set_title(f"Gráfico de Área da coluna {coluna} para o tipo de célula {tipo_de_celula}", color="#ffffff")
    ax.set_xlabel(coluna, color="#ffffff")
    ax.set_ylabel('Densidade', color="#ffffff")
    
    # Definindo as cores das legendas dos eixos
    ax.tick_params(axis='x', colors="#ffffff")
    ax.tick_params(axis='y', colors="#ffffff")

    # Adicionando as 4 bordas ao plot
    ax.spines['bottom'].set_color('#00ffff')
    ax.spines['top'].set_color('#00ffff')
    ax.spines['right'].set_color('#00ffff')
    ax.spines['left'].set_color('#00ffff')
    
    ax.set_facecolor("#000000")
    fig.patch.set_facecolor("#000000")
    st.pyplot(fig)

# Calculando a média dos valores para cada tipo de célula
media_por_tipo = amostra_selecionada.groupby("Tipo de Célula")[amostra_coluna].mean().reset_index()


# Função para identificar e selecionar as opções de dados categóricos na base selecionada
def get_categoricos(data):
    categoricos = []
    for col in data.columns:
        if data[col].dtype == 'object':
            categoricos.append(col)
    return categoricos

# Função para identificar e selecionar as opções de dados numéricos na base selecionada
def get_numericos(data):
    numericos = []
    for col in data.columns:
        if data[col].dtype in ['int64', 'float64']:
            numericos.append(col)
    return numericos

# Selecionando os dados categóricos e numéricos
categoricos = get_categoricos(amostra_selecionada)
numericos = get_numericos(amostra_selecionada)

# Criando selectbox para selecionar os dados categóricos e numéricos    
coluna_categorica = categoricos[0]
coluna_numerica = numericos[0]

# Função para criar o gráfico de linha estilizado
def grafico_linha(df, coluna_categorica, coluna_numerica):
    fig, ax = plt.subplots(figsize=(12, 9))  # Aumentando a largura do gráfico
    sns.lineplot(x=coluna_categorica, y=coluna_numerica, data=df, ax=ax, color="#00ffff", marker="o")
    
    # Definindo o título e as cores dos rótulos dos eixos
    ax.set_title(f"Gráfico de Linha para a coluna {coluna_numerica}", color="#ffffff")
    ax.set_xlabel(coluna_categorica, color="#ffffff")
    ax.set_ylabel(coluna_numerica, color="#ffffff")
    
    # Definindo as cores das legendas dos eixos
    ax.tick_params(axis='x', colors="#ffffff")
    ax.tick_params(axis='y', colors="#ffffff")

    # Adicionando as 4 bordas ao plot
    ax.spines['bottom'].set_color('#00ffff')
    ax.spines['top'].set_color('#00ffff')
    ax.spines['right'].set_color('#00ffff')
    ax.spines['left'].set_color('#00ffff')
    
    ax.set_facecolor("#000000")
    fig.patch.set_facecolor("#000000")
    st.pyplot(fig)



# PLOTANDO OS 3 GRÁFICO NA MESMA LINHA EM 3 COLUNAS

col1, col2 = st.columns(2)

with col1:
    # Verificando se os valores não estão vazios
    if len(tipos_de_celula) == 0 or len(valores_amostra) == 0:
        st.error("A coluna selecionada não possui valores válidos para a criação do gráfico.")
    else:
        # Interpolação spline para suavizar a linha
        X_ = np.arange(len(tipos_de_celula))
        X_Y_Spline = make_interp_spline(X_, valores_amostra)
        X_interp = np.linspace(X_.min(), X_.max(), 500)
        Y_interp = X_Y_Spline(X_interp)

        fig, ax = plt.subplots()
        ax.plot(X_interp, Y_interp, color="#00ffff", markerfacecolor="#00ffff", markeredgewidth=2)

        # Adicionando as linhas de grade
        #ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='#00ffff')

        # Definindo o título e as cores dos rótulos dos eixos
        ax.set_title(f"Gráfico de Linha Suavizado para '{amostra_coluna}'", color="#ffffff")
        ax.set_xlabel("Quantidade", color="#ffffff")
        ax.set_ylabel("Intervalo", color="#ffffff")
        
        # Definindo as cores das legendas dos eixos
        ax.tick_params(axis='x', colors="#ffffff")
        ax.tick_params(axis='y', colors="#ffffff")

        # Ajustando os rótulos do eixo x para mostrar os tipos de células
        #ax.set_xticks(X_)
        #ax.set_xticklabels(tipos_de_celula, rotation=45, ha='right')

            
        # Adicionando as 4 bordas ao plot
        ax.spines['bottom'].set_color('#00ffff')
        ax.spines['top'].set_color('#00ffff')
        ax.spines['right'].set_color('#00ffff')
        ax.spines['left'].set_color('#00ffff')
        
        ax.set_facecolor("#000000")
        fig.patch.set_facecolor("#000000")
        st.pyplot(fig)
with col2:
    # Verificando se a amostra filtrada não está vazia
    if amostra_filtrada.empty:
        st.error("Não há dados para o tipo de célula selecionado.")
    else:
        # Extraindo os valores das amostras (todas as colunas, exceto a primeira)
        x = amostra_filtrada.columns[1:]  # Nomes das colunas das amostras
        y = amostra_filtrada.iloc[0, 1:].values  # Valores das amostras

        # Verificando se x e y não estão vazios
        if len(x) == 0 or len(y) == 0:
            st.error("A coluna selecionada não possui valores válidos para a criação do gráfico.")
        else:
            # Interpolação spline para suavizar a linha
            X_ = np.arange(len(x))
            X_Y_Spline = make_interp_spline(X_, y)
            X_interp = np.linspace(X_.min(), X_.max(), 500)
            Y_interp = X_Y_Spline(X_interp)

            fig, ax = plt.subplots()
            ax.plot(X_interp, Y_interp, color="#00ffff", markerfacecolor="#00ffff", markeredgewidth=2)

            # Adicionando as linhas de grade
            ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='#00ffff')

            # Definindo o título e as cores dos rótulos dos eixos
            ax.set_title(f"Gráfico de Linha Suavizado para o Tipo de Célula '{tipo_de_celula_selecionado}'", color="#ffffff")
            ax.set_xlabel("Amostras", color="#ffffff")
            ax.set_ylabel("Valores", color="#ffffff")
            
            # Definindo as cores das legendas dos eixos
            ax.tick_params(axis='x', colors="#ffffff")
            ax.tick_params(axis='y', colors="#ffffff")

            # Adicionando as 4 bordas ao plot
            ax.spines['bottom'].set_color('#00ffff')
            ax.spines['top'].set_color('#00ffff')
            ax.spines['right'].set_color('#00ffff')
            ax.spines['left'].set_color('#00ffff')
            
            ax.set_facecolor("#000000")
            fig.patch.set_facecolor("#000000")
            st.pyplot(fig)
with col1:
    # plotando o gráfico de área
    grafico_de_area(amostra_selecionada, amostra_coluna, tipo_de_celula_selecionado)
with col2:
    # Criando o gráfico de linha estilizado
    grafico_linha(amostra_selecionada, coluna_categorica, amostra_coluna)


# Separando o título e o subtítulo com uma linha
st.markdown(
    "<hr style='border: 1px solid cyan;'>",
    unsafe_allow_html=True
)

# Gráfico de linhas
st.title("Gráfico de Barras")

# Função para criar uma paleta de cores personalizada com ciano incluído
def criar_paleta_com_ciano(n):
    colors = sns.color_palette("cool", n)
    colors = [(0, 1, 1)] + list(colors[1:])  # Substitui a primeira cor por ciano
    return colors

# Função para criar o gráfico de barras
def grafico_de_barras(df, coluna_categorica, coluna_numerica, title, ax):
    colors = criar_paleta_com_ciano(len(df[coluna_categorica].unique()))
    bars = sns.barplot(x=coluna_categorica, y=coluna_numerica, data=df, ax=ax, palette=colors)
    
    # Definindo o título e as cores dos rótulos dos eixos
    ax.set_title(title, color="#ffffff")
    ax.set_xlabel(coluna_categorica, color="#ffffff")
    ax.set_ylabel(coluna_numerica, color="#ffffff")
    
    # Definindo as cores das legendas dos eixos
    ax.tick_params(axis='x', colors="#ffffff")
    ax.tick_params(axis='y', colors="#ffffff")

    # Adicionando as 4 bordas ao plot
    ax.spines['bottom'].set_color('#00ffff')
    ax.spines['top'].set_color('#00ffff')
    ax.spines['right'].set_color('#00ffff')
    ax.spines['left'].set_color('#00ffff')
    
    # Adicionando as linhas de grade
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='#00ffff')
    
    ax.set_facecolor("#000000")
    fig.patch.set_facecolor("#000000")
    
    # Adicionando os rótulos dos dados
    for bar in bars.patches:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),  # 5 points vertical offset
                    textcoords="offset points",
                    ha='center', color='#ffffff')

# Extraindo os valores categóricos e numéricos
tipos_de_celula = amostra_selecionada["Tipo de Célula"].values
valores_amostra = amostra_selecionada[amostra_coluna].values

# Verificando se os valores não estão vazios
if len(tipos_de_celula) == 0 or len(valores_amostra) == 0:
    st.error("A coluna selecionada não possui valores válidos para a criação do gráfico.")
else:
    # Criando um DataFrame temporário para passar para a função de gráfico
    temp_df = pd.DataFrame({
        "Tipo de Célula": tipos_de_celula,
        "Valores": valores_amostra,
        "Média": np.mean(valores_amostra),
        "Mediana": np.median(valores_amostra),
        "Variância": np.var(valores_amostra)
    })

    fig, axs = plt.subplots(2, 2, figsize=(20, 14))

    grafico_de_barras(temp_df, "Tipo de Célula", "Valores", f"Gráfico de Barras - Valores de {amostra_coluna}", axs[0, 0])
    grafico_de_barras(temp_df, "Tipo de Célula", "Média", f"Gráfico de Barras - Média de {amostra_coluna}", axs[0, 1])
    grafico_de_barras(temp_df, "Tipo de Célula", "Mediana", f"Gráfico de Barras - Mediana de {amostra_coluna}", axs[1, 0])
    grafico_de_barras(temp_df, "Tipo de Célula", "Variância", f"Gráfico de Barras - Variância de {amostra_coluna}", axs[1, 1])

    st.pyplot(fig)

# Separando o título e o subtítulo com uma linha
st.markdown(
    "<hr style='border: 1px dashed cyan;'>",
    unsafe_allow_html=True
)