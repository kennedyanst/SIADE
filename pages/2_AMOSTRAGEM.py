import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

st.set_page_config(layout="wide", 
                   page_title="Amostragem",
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

# Menu de opções - 2
st.title("AMOSTRAGEM")
st.write("Abaixo, você pode selecionar diferentes tipos de amostragem para visualizar e extrair os dados os dados. Atualemnte, as técnicas de amostragem disponíveis são: Amostragem Aleatória Simples, Amostragem Sistemática, Amostragem por Grupos e Amostragem Estratificada, cada uma com suas particularidades e aplicações específicas para diferentes tipos bases.")



logo_udf = Image.open("logo_udf_online_branco.png")
st.sidebar.image(logo_udf, use_column_width=True)
#st.sidebar.markdown("Centro Universitário do Distrito Federal")
st.sidebar.markdown(
    "<hr style='border: 1px solid cyan;'>",
    unsafe_allow_html=True
)
logo_fap = Image.open("fap.jpg")
st.sidebar.image(logo_fap, use_column_width=True)


st.markdown(
    "<hr style='border: 1px solid cyan;'>",
    unsafe_allow_html=True
)

#'''-------------------------------------- AMOSTRAGEM SIMPLES --------------------------------------'''
st.title("AMOSTRAGEM ALEÁTORIA SIMPLES")
st.header("A amostragem aleatória simples é um método de seleção de uma amostra onde cada elemento da população tem a mesma probabilidade de ser escolhido. É o tipo mais básico de amostragem, onde a seleção é feita aleatoriamente, sem qualquer estrutura pré-determinada.")

st.header("No código, a amostragem aleatória simples é realizada utilizando a função sample do pandas, que seleciona aleatoriamente um número especificado de linhas do DataFrame, garantindo que cada linha tenha a mesma probabilidade de ser escolhida.")

st.header("O código segue fielmente a teoria ao garantir que todos os elementos têm a mesma chance de serem incluídos na amostra, o que é um princípio fundamental da amostragem aleatória simples.")
             
st.header("A amostragem aleatória simples é um método eficaz para obter uma amostra representativa da população, desde que a seleção seja feita de forma aleatória e sem viés.")

st.markdown("Selecione o número de linhas que deseja extrair da amostra simples.")
st.write("Número de linhas no arquivo:", arquivo.shape[0])

n_linhas = st.number_input("Número de linhas", min_value=1, max_value=arquivo.shape[0], value=10, key='n_linhas1')

# Espaço reservado para exibir as informações a baixo dos botões
info_placeholder = st.empty()

# ORGANIZANDO O LAYOUT DOS BOTÕES E CRIANDO A TELA PARA VISUALIZAÇÃO DOS DADOS QUANDO OS BOTÕES FOREM SELECIONADOS
col1, col2 = st.columns(2)

# #def save_file_dialog(file_type):
#     root = Tk()
#     root.withdraw()  # Oculta a janela principal do Tkinter
#     root.attributes('-topmost', True)  # Garante que a janela de diálogo apareça na frente
#     file_path = filedialog.asksaveasfilename(defaultextension=file_type, filetypes=[(file_type.upper(), f"*.{file_type}")])
#     root.destroy()
#     return file_path

with col1:
    if st.button("Amostra Simples"):
        info_placeholder.write(arquivo.sample(n_linhas))


with col2:
    if st.button("Salvar na sessão"):
        st.session_state['amostra_simples'] = arquivo.sample(n_linhas)
        st.success("Amostra simples salva na sessão com sucesso!")



st.markdown(
    "<hr style='border: 1px solid cyan;'>",
    unsafe_allow_html=True
)




#'''-------------------------------------- AMOSTRAGEM SISTEMÁTICA --------------------------------------'''
st.title("AMOSTRAGEM SISTEMÁTICA")

st.header("Na amostragem sistemática, os elementos são selecionados em intervalos regulares de uma lista ordenada da população, começando a partir de um ponto inicial aleatório. Por exemplo, se você deseja uma amostra de 10% de uma população, pode selecionar cada décimo elemento após um ponto de partida aleatório.")

st.header("A amostragem sistemática é implementada dividindo a população em intervalos iguais e selecionando um ponto de partida aleatório dentro do primeiro intervalo. A partir daí, elementos são selecionados em intervalos regulares usando um loop que percorre o DataFrame com base no intervalo calculado.")

st.header("A abordagem sistemática usada no código reflete a teoria de selecionar elementos em intervalos regulares após a escolha de um ponto de partida aleatório. Isso é útil para evitar vieses, especialmente em populações ordenadas.")

st.header("A mostra sistemática é uma técnica eficaz e que pode ser mais eficiente do que a amostragem aleatória simples, pois garante que a amostra seja representativa da população. Porém, é importante garantir que a população seja aleatória e que não haja padrões nos dados que possam afetar a seleção dos elementos.")

st.markdown("Selecione o número de linhas que deseja extrair da amostra sistemática.")
st.write("Número de linhas no arquivo:", arquivo.shape[0])

col1_1, col2_1, col3_1 = st.columns(3)

with col1_1:
    n_linhas = st.number_input("Dividir por: ", min_value=1, max_value=arquivo.shape[0], value=10, key='n_linhas2')
with col2_1:    
    tamanha_amostra = st.number_input("Quantidade linhas: ", min_value=1, max_value=arquivo.shape[0], value=10, key='n_amostra2')
with col3_1:
    seed = st.number_input("Seed: ", min_value=1, max_value=arquivo.shape[0], value=10, key='n_seed2')


# Espaço reservado para exibir as informações a baixo dos botões
info_placeholder = st.empty()

# ORGANIZANDO O LAYOUT DOS BOTÕES E CRIANDO A TELA PARA VISUALIZAÇÃO DOS DADOS QUANDO OS BOTÕES FOREM SELECIONADOS
col1, col2= st.columns(2)

def amostragem_sistematica(df, dividir, tamanho_amostra, seed=None):
    tamanho_populacao = len(df)
    np.random.seed(seed)
    intervalo = tamanho_populacao // dividir
    ponto_partida = np.random.randint(0, intervalo)
    indices = [i for i in range(ponto_partida, tamanho_populacao, intervalo)]
    return df.iloc[indices[:tamanho_amostra]]

st.write("Número de linhas no arquivo:", arquivo.shape[0])

with col1:
    if st.button("Amostra Sistemática", key='amostra_sistematica1'):
        amostra_sistematica = amostragem_sistematica(arquivo, n_linhas, tamanha_amostra, seed)
        info_placeholder.write(amostra_sistematica)

with col2:
    if st.button("Salvar na sessão", key='amostra_sistematica4'):
        st.session_state['amostra_sistematica'] = arquivo.sample(n_linhas)
        st.success("Amostra sistemática salva na sessão com sucesso!")




st.markdown(
    "<hr style='border: 1px solid cyan;'>",
    unsafe_allow_html=True
)




#'''-------------------------------------- AMOSTRAGEM POR GRUPOS --------------------------------------'''

st.title("AMOSTRAGEM POR GRUPOS")

st.header("A amostragem por grupos envolve a divisão da população em grupos ou clusters, selecionando aleatoriamente alguns desses grupos, e incluindo todos os elementos dos grupos selecionados na amostra. É útil quando a população está naturalmente dividida em grupos.")

st.header("A função para amostragem por grupos primeiro divide a população em um número especificado de grupos usando np.array_split. Em seguida, grupos inteiros são selecionados aleatoriamente com np.random.choice, e a amostra é composta por todos os elementos desses grupos.")

st.header("O código reflete a teoria ao dividir a população em grupos e ao selecionar alguns desses grupos para formar a amostra. Isso é particularmente relevante quando os grupos naturais são heterogêneos entre si, mas homogêneos internamente.")

st.header("Amostragem em grupos mostra grande eficiência ao reduzir a variabilidade da amostra, especialmente quando os grupos são homogêneos internamente. No entanto, é importante garantir que os grupos sejam representativos da população e que não haja viés na seleção dos grupos.")

st.markdown("Selecione o número de linhas que deseja extrair da amostra por grupos.")
st.write("Número de linhas no arquivo:", arquivo.shape[0])

col1, col2 = st.columns(2)

with col1:
    n_linhas = st.number_input("Número de linhas", min_value=1, max_value=arquivo.shape[0], value=10, key='n_linhas3')

with col2:
    num_grupos = st.number_input("Número de grupos", min_value=1, max_value=arquivo.shape[0], value=5, key='num_grupos')

info_placeholder = st.empty()

def amostragem_por_grupos(df, num_grupos, n_linhas):
    """
    Realiza a amostragem por grupos a partir de um DataFrame.

    Args:
    df (pd.DataFrame): A população da qual a amostra será retirada.
    num_grupos (int): O número de grupos a serem selecionados.

    Returns:
    pd.DataFrame: A amostra por grupos.
    """
    # Dividir a população em grupos
    grupos = np.array_split(df, num_grupos)

    # Selecionar aleatoriamente os índices dos grupos
    indices_selecionados = np.random.choice(range(len(grupos)), size=num_grupos, replace=False)

    # Concatenar os grupos selecionados para formar a amostra
    amostra = pd.concat([grupos[i] for i in indices_selecionados])

    amostra = amostra.sample(n_linhas)

    return amostra

with col1:
    if st.button("Amostra por Grupos", key='amostra_grupos1'):
        amostra_grupos = amostragem_por_grupos(arquivo, num_grupos, n_linhas)
        info_placeholder.write(amostra_grupos)

with col2:
    if st.button("Salvar na sessão", key='amostra_grupos4'):
        st.session_state['amostra_grupos'] = arquivo.sample(n_linhas)
        st.success("Amostra por grupos salva na sessão com sucesso!")

st.markdown(
    "<hr style='border: 1px solid cyan;'>",
    unsafe_allow_html=True
)


# '''-------------------------------------- AMOSTRAGEM ESTRATIFICADA --------------------------------------'''

st.title("AMOSTRAGEM ESTRATIFICADA")

st.header("Na amostragem estratificada, a população é dividida em subgrupos ou estratos que compartilham características similares. Amostras são então extraídas de cada estrato proporcionalmente ao seu tamanho na população, garantindo que a amostra represente todas as subpopulações.")

st.header("A amostragem estratificada no código envolve agrupar os dados com base em uma coluna especificada pelo usuário, que representa os estratos. Em seguida, a função groupby do pandas é usada para aplicar a função sample a cada estrato, garantindo que cada estrato seja proporcionalmente representado na amostra.")

st.header("A implementação da amostragem estratificada garante que cada estrato da população seja representado na amostra de acordo com sua proporção no total, o que é essencial para captar a variabilidade dentro de diferentes subgrupos da população.")

st.header("A amostragem estratificada é particularmente útil quando a população é heterogênea e contém subgrupos distintos. Garante que cada subgrupo seja representado na amostra, o que é crucial para obter uma visão abrangente da população.")

st.markdown("Selecione o número de linhas que deseja extrair da amostra estratificada.")
st.write("Número de linhas no arquivo:", arquivo.shape[0])

col1, col2 = st.columns(2)
with col1:
    n_linhas = st.number_input("Número de linhas", min_value=1, max_value=arquivo.shape[0], value=10, key='n_linhas4')

with col2:
    coluna_estratificacao = st.selectbox("Selecione a coluna para estratificação", arquivo.columns)

# Função para alternar o estado do botão
def toggle_button_state(key):
    if key not in st.session_state:
        st.session_state[key] = False
    st.session_state[key] = not st.session_state[key]

# Espaço reservado para exibir as informações abaixo dos botões
info_placeholder = st.empty()

# ORGANIZANDO O LAYOUT DOS BOTÕES E CRIANDO A TELA PARA VISUALIZAÇÃO DOS DADOS QUANDO OS BOTÕES FOREM SELECIONADOS

def amostra_estratificada(df, coluna_estratificacao, n):
    # Proporção de amostra em relação ao tamanho total do dataset
    proporcao_amostra = n / len(df)
    
    # Amostragem estratificada
    df_amostra = df.groupby(coluna_estratificacao, group_keys=False).apply(lambda x: x.sample(frac=proporcao_amostra))
    
    # Se o número de linhas não corresponder ao número exato, realizar ajuste para coincidir
    if len(df_amostra) > n:
        df_amostra = df_amostra.sample(n)
    
    return df_amostra

with col1:
    if st.button("Amostra Estratificada", key='amostra_estratificada1'):
        toggle_button_state('amostra_estratificada1_state')
        if st.session_state['amostra_estratificada1_state']:
            amostra = amostra_estratificada(arquivo, coluna_estratificacao, n_linhas)
            info_placeholder.write(amostra)
        else:
            info_placeholder.empty()


with col2:
    if st.button("Salvar na sessão", key='amostra_estratificada4'):
        st.session_state['amostra_estratificada'] = amostra_estratificada(arquivo, coluna_estratificacao, n_linhas)
        st.success("Amostra estratificada salva na sessão com sucesso!")

st.markdown("<hr style='border: 1px solid cyan;'>", unsafe_allow_html=True)




#'''-------------------------------------- COMPARATIVO DAS 4 AMOSTRAGENS --------------------------------------'''

st.title("COMPARATIVO DAS 4 AMOSTRAGENS")
st.markdown("Aqui você pode comparar as amostras extraídas com os diferentes tipos de amostragem.")

# CRIANDO UMA TABELA COM A MÉDIA, MEDIANA, DESVIO PADRÃO E COEFICIENTE DE VARIAÇÃO E VARIAÇÃO DAS AMOSTRAS EXTRAÍDAS

# Criando um DataFrame com as amostras extraídas
amostra_simples = st.session_state.get('amostra_simples', pd.DataFrame())
amostra_sistematica = st.session_state.get('amostra_sistematica', pd.DataFrame())
amostra_grupos = st.session_state.get('amostra_grupos', pd.DataFrame())
amostra_estratificada = st.session_state.get('amostra_estratificada', pd.DataFrame())

# Calculando a média das amostras
media_amostra_simples = amostra_simples.select_dtypes(include='number').mean().to_frame().T if not amostra_simples.empty else pd.DataFrame()
media_amostra_sistematica = amostra_sistematica.select_dtypes(include='number').mean().to_frame().T if not amostra_sistematica.empty else pd.DataFrame()
media_amostra_grupos = amostra_grupos.select_dtypes(include='number').mean().to_frame().T if not amostra_grupos.empty else pd.DataFrame()
media_amostra_estratificada = amostra_estratificada.select_dtypes(include='number').mean().to_frame().T if not amostra_estratificada.empty else pd.DataFrame()

# Concatenando os DataFrames e colocando os nomes das amostras na primeira coluna
media_amostra_simples.insert(0, 'Amostra', 'Amostra Simples')
media_amostra_sistematica.insert(0, 'Amostra', 'Amostra Sistemática')
media_amostra_grupos.insert(0, 'Amostra', 'Amostra por Grupos')
media_amostra_estratificada.insert(0, 'Amostra', 'Amostra Estratificada')
comparativo_media = pd.concat([media_amostra_simples, media_amostra_sistematica, media_amostra_grupos, media_amostra_estratificada])

# Exibindo a tabela
st.write("MÉDIA DAS AMOSTRAS")
st.write(comparativo_media)

# Calcuiando a mediana das amostras
mediana_amostra_simples = amostra_simples.select_dtypes(include='number').median().to_frame().T if not amostra_simples.empty else pd.DataFrame()
mediana_amostra_sistematica = amostra_sistematica.select_dtypes(include='number').median().to_frame().T if not amostra_sistematica.empty else pd.DataFrame()
mediana_amostra_grupos = amostra_grupos.select_dtypes(include='number').median().to_frame().T if not amostra_grupos.empty else pd.DataFrame()
mediana_amostra_estratificada = amostra_estratificada.select_dtypes(include='number').median().to_frame().T if not amostra_estratificada.empty else pd.DataFrame()

# Concatenando os DataFrames e colocando os nomes das amostras na primeira coluna
mediana_amostra_simples.insert(0, 'Amostra', 'Amostra Simples')
mediana_amostra_sistematica.insert(0, 'Amostra', 'Amostra Sistemática')
mediana_amostra_grupos.insert(0, 'Amostra', 'Amostra por Grupos')
mediana_amostra_estratificada.insert(0, 'Amostra', 'Amostra Estratificada')
comparativo_mediana = pd.concat([mediana_amostra_simples, mediana_amostra_sistematica, mediana_amostra_grupos, mediana_amostra_estratificada])

# Exibindo a tabela
st.write("MEDIANA DAS AMOSTRAS")
st.write(comparativo_mediana)


# Calculando o desvio padrão das amostras
std_amostra_simples = amostra_simples.select_dtypes(include='number').std().to_frame().T if not amostra_simples.empty else pd.DataFrame()
std_amostra_sistematica = amostra_sistematica.select_dtypes(include='number').std().to_frame().T if not amostra_sistematica.empty else pd.DataFrame()
std_amostra_grupos = amostra_grupos.select_dtypes(include='number').std().to_frame().T if not amostra_grupos.empty else pd.DataFrame()
std_amostra_estratificada = amostra_estratificada.select_dtypes(include='number').std().to_frame().T if not amostra_estratificada.empty else pd.DataFrame()

# Concatenando os DataFrames e colocando os nomes das amostras na primeira coluna
std_amostra_simples.insert(0, 'Amostra', 'Amostra Simples')
std_amostra_sistematica.insert(0, 'Amostra', 'Amostra Sistemática')
std_amostra_grupos.insert(0, 'Amostra', 'Amostra por Grupos')
std_amostra_estratificada.insert(0, 'Amostra', 'Amostra Estratificada')
comparativo_std = pd.concat([std_amostra_simples, std_amostra_sistematica, std_amostra_grupos, std_amostra_estratificada])

# Exibindo a tabela
st.write("DESVIO PADRÃO DAS AMOSTRAS")
st.write(comparativo_std)


# Calculando o coeficiente de variação das amostras
cv_amostra_simples = (amostra_simples.select_dtypes(include='number').std() / amostra_simples.select_dtypes(include='number').mean()).to_frame().T if not amostra_simples.empty else pd.DataFrame()
cv_amostra_sistematica = (amostra_sistematica.select_dtypes(include='number').std() / amostra_sistematica.select_dtypes(include='number').mean()).to_frame().T if not amostra_sistematica.empty else pd.DataFrame()
cv_amostra_grupos = (amostra_grupos.select_dtypes(include='number').std() / amostra_grupos.select_dtypes(include='number').mean()).to_frame().T if not amostra_grupos.empty else pd.DataFrame()
cv_amostra_estratificada = (amostra_estratificada.select_dtypes(include='number').std() / amostra_estratificada.select_dtypes(include='number').mean()).to_frame().T if not amostra_estratificada.empty else pd.DataFrame()

# Concatenando os DataFrames e colocando os nomes das amostras na primeira coluna
cv_amostra_simples.insert(0, 'Amostra', 'Amostra Simples')
cv_amostra_sistematica.insert(0, 'Amostra', 'Amostra Sistemática')
cv_amostra_grupos.insert(0, 'Amostra', 'Amostra por Grupos')
cv_amostra_estratificada.insert(0, 'Amostra', 'Amostra Estratificada')
comparativo_cv = pd.concat([cv_amostra_simples, cv_amostra_sistematica, cv_amostra_grupos, cv_amostra_estratificada])

# Exibindo a tabela
st.write("COEFICIENTE DE VARIAÇÃO DAS AMOSTRAS")
st.write(comparativo_cv)


# Calculando a variação das amostras
var_amostra_simples = amostra_simples.select_dtypes(include='number').var().to_frame().T if not amostra_simples.empty else pd.DataFrame()
var_amostra_sistematica = amostra_sistematica.select_dtypes(include='number').var().to_frame().T if not amostra_sistematica.empty else pd.DataFrame()
var_amostra_grupos = amostra_grupos.select_dtypes(include='number').var().to_frame().T if not amostra_grupos.empty else pd.DataFrame()
var_amostra_estratificada = amostra_estratificada.select_dtypes(include='number').var().to_frame().T if not amostra_estratificada.empty else pd.DataFrame()

# Concatenando os DataFrames e colocando os nomes das amostras na primeira coluna
var_amostra_simples.insert(0, 'Amostra', 'Amostra Simples')
var_amostra_sistematica.insert(0, 'Amostra', 'Amostra Sistemática')
var_amostra_grupos.insert(0, 'Amostra', 'Amostra por Grupos')
var_amostra_estratificada.insert(0, 'Amostra', 'Amostra Estratificada')
comparativo_var = pd.concat([var_amostra_simples, var_amostra_sistematica, var_amostra_grupos, var_amostra_estratificada])

# Exibindo a tabela
st.write("VARIÂNCIA DAS AMOSTRAS")
st.write(comparativo_var)