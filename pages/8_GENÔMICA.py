import streamlit as st
import pandas as pd
from PIL import Image

# Configurando a página
st.set_page_config(
    page_title="Genômica", 
    layout="wide",
    page_icon="./favicon_io/favicon.ico"
)

# Adicionando CSS para ajustar o tamanho dos botões
with open("css/estilo.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Criando a página
logo_udf = Image.open("logo_udf_online_branco.png")
st.sidebar.image(logo_udf, use_column_width=True)
st.sidebar.markdown("<hr style='border: 1px solid cyan;'>", unsafe_allow_html=True)
logo_fap = Image.open("fap.jpg")
st.sidebar.image(logo_fap, use_column_width=True)

# TÍTULO
st.title("Análise de Dados Genômicos de Proteínas para arquivos FASTA")

# Descrição
st.header("Selecione o arquivo FASTA que deseja analisar e obtenha informações sobre a proteína.")

# Entrada para o nome do gene
gene_name = st.text_input("Digite o nome do gene:")

# Upload do arquivo FASTA
uploaded_file = st.file_uploader("Carregue o arquivo FASTA", type=["fasta"])

# Verificação se o usuário carregou um arquivo e digitou o nome do gene
if uploaded_file is not None and gene_name:
    # Caminho para salvar o arquivo
    save_path = f"./{gene_name}.fasta"
    
    # Salvando o arquivo
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"O arquivo foi salvo com o nome: {save_path}")
else:
    st.warning("Por favor, digite o nome do gene e carregue um arquivo FASTA.")
