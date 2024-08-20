import streamlit as st
import pandas as pd
from PIL import Image
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv


# Configurando a página
st.set_page_config(
    page_title="Genômica", 
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
st.title("Análise de Dados Genômicos de Proteínas para arquivos FASTA")