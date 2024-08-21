import streamlit as st
import pandas as pd
from PIL import Image
from collections import Counter
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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
st.header("Selecione o arquivo FASTA que deseja analisar e obtenha informações sobre a proteína e seus aminoácidos.")

# Entrada para o nome do gene
gene_name = st.text_input("Digite o nome do gene:")

# Upload do arquivo FASTA
uploaded_file = st.file_uploader("Carregue o arquivo FASTA", type=["fasta", "fna"])

if uploaded_file is not None:
    # Função para ler a sequência de DNA de um arquivo FASTA
    def parse_fasta(file):
        sequence = ""
        for line in file:
            line = line.decode("utf-8")  # Decodifica a linha de bytes para string
            if not line.startswith(">"):
                sequence += line.strip()
        return sequence
    
    # Lendo a sequência do arquivo carregado
    sequence = parse_fasta(uploaded_file)
    
    # Exibindo a sequência de nucleotídeos (código genético)
    st.subheader(f"Código Genético para: {gene_name}")
    st.text_area("Sequência de Nucleotídeos:", value=sequence, height=150)
    
    # Verificação se o usuário digitou o nome do gene
    if gene_name:
        # Caminho para salvar o arquivo
        save_path = f"./{gene_name}.fasta"
        
        # Salvando o arquivo
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"O arquivo foi salvo com o nome: {save_path}")
        
        # Dicionário de códons e seus respectivos aminoácidos
        codon_to_amino_acid = {
            'UUU': 'Fenilalanina (Phe)', 'UUC': 'Fenilalanina (Phe)',
            'UUA': 'Leucina (Leu)', 'UUG': 'Leucina (Leu)',
            'UCU': 'Serina (Ser)', 'UCC': 'Serina (Ser)', 'UCA': 'Serina (Ser)', 'UCG': 'Serina (Ser)',
            'UAU': 'Tirosina (Tyr)', 'UAC': 'Tirosina (Tyr)',
            'UAA': 'STOP', 'UAG': 'STOP',
            'UGU': 'Cisteína (Cys)', 'UGC': 'Cisteína (Cys)',
            'UGA': 'STOP', 'UGG': 'Triptofano (Trp)',
            'CUU': 'Leucina (Leu)', 'CUC': 'Leucina (Leu)', 'CUA': 'Leucina (Leu)', 'CUG': 'Leucina (Leu)',
            'CCU': 'Prolina (Pro)', 'CCC': 'Prolina (Pro)', 'CCA': 'Prolina (Pro)', 'CCG': 'Prolina (Pro)',
            'CAU': 'Histidina (His)', 'CAC': 'Histidina (His)',
            'CAA': 'Glutamina (Gln)', 'CAG': 'Glutamina (Gln)',
            'CGU': 'Arginina (Arg)', 'CGC': 'Arginina (Arg)', 'CGA': 'Arginina (Arg)', 'CGG': 'Arginina (Arg)',
            'AUU': 'Isoleucina (Ile)', 'AUC': 'Isoleucina (Ile)', 'AUA': 'Isoleucina (Ile)',
            'AUG': 'Metionina (Met) (START)',
            'ACU': 'Treonina (Thr)', 'ACC': 'Treonina (Thr)', 'ACA': 'Treonina (Thr)', 'ACG': 'Treonina (Thr)',
            'AAU': 'Asparagina (Asn)', 'AAC': 'Asparagina (Asn)',
            'AAA': 'Lisina (Lys)', 'AAG': 'Lisina (Lys)',
            'AGU': 'Serina (Ser)', 'AGC': 'Serina (Ser)',
            'AGA': 'Arginina (Arg)', 'AGG': 'Arginina (Arg)',
            'GUU': 'Valina (Val)', 'GUC': 'Valina (Val)', 'GUA': 'Valina (Val)', 'GUG': 'Valina (Val)',
            'GCU': 'Alanina (Ala)', 'GCC': 'Alanina (Ala)', 'GCA': 'Alanina (Ala)', 'GCG': 'Alanina (Ala)',
            'GAU': 'Ácido aspártico (Asp)', 'GAC': 'Ácido aspártico (Asp)',
            'GAA': 'Ácido glutâmico (Glu)', 'GAG': 'Ácido glutâmico (Glu)',
            'GGU': 'Glicina (Gly)', 'GGC': 'Glicina (Gly)', 'GGA': 'Glicina (Gly)', 'GGG': 'Glicina (Gly)',
        }

        # Função para traduzir a sequência de nucleotídeos em aminoácidos
        def translate_sequence(sequence, codon_to_amino_acid):
            amino_acid_sequence = []
            codons_used = []
            rna_sequence = sequence.replace("T", "U")  # Transcreve DNA para RNA
            
            for i in range(0, len(rna_sequence), 3):
                codon = rna_sequence[i:i+3]
                if len(codon) == 3:
                    amino_acid = codon_to_amino_acid.get(codon, "Unknown")
                    amino_acid_sequence.append(amino_acid)
                    codons_used.append(codon)
            
            return amino_acid_sequence, codons_used
        
        # Traduzindo a sequência de nucleotídeos em aminoácidos
        amino_acid_sequence, codons_used = translate_sequence(sequence, codon_to_amino_acid)
        
        # Contando a quantidade de cada aminoácido
        amino_acid_counts = Counter(amino_acid_sequence)
        
        # Criando uma lista de tuplas para armazenar os aminoácidos, códons e suas quantidades
        data = []
        for amino_acid, codon in zip(amino_acid_sequence, codons_used):
            data.append((amino_acid, codon, amino_acid_counts[amino_acid]))
        
        # Criando um DataFrame para exibir a tabela
        df_amino_acids = pd.DataFrame(data, columns=['Aminoácido', 'Códon', 'Quantidade']).drop_duplicates(subset=['Aminoácido']).sort_values(by='Quantidade', ascending=False)
        
        # Exibindo a tabela de aminoácidos, códons e suas quantidades
        st.subheader(f"Tabela de Aminoácidos para: {gene_name} ")
        st.table(df_amino_acids)
        
        # Gráfico de correlação
        st.subheader(f"Gráfo de Correlação entre Aminoácidos da Proteína: {gene_name}")
        
        # Criando um grafo
        G = nx.Graph()
        
        # Adicionando os nós e as conexões (arestas) ao grafo
        for i in range(len(amino_acid_sequence) - 1):
            G.add_edge(amino_acid_sequence[i], amino_acid_sequence[i + 1])
        
        # Desenhando o grafo
        pos = nx.spring_layout(G)  # Layout do grafo
        plt.figure(figsize=(10, 8))
        nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=10, font_weight="bold", edge_color="gray")
        
        # Exibindo o grafo no Streamlit
        st.pyplot(plt)

        def compute_co_occurrence_matrix(amino_acid_sequence):
            amino_acids = list(set(amino_acid_sequence))
            matrix = pd.DataFrame(0, index=amino_acids, columns=amino_acids)
            
            for i in range(len(amino_acid_sequence) - 1):
                amino_acid_1 = amino_acid_sequence[i]
                amino_acid_2 = amino_acid_sequence[i + 1]
                matrix.at[amino_acid_1, amino_acid_2] += 1
                matrix.at[amino_acid_2, amino_acid_1] += 1
    
            return matrix
        

        # Calculando a matriz de co-ocorrência
        co_occurrence_matrix = compute_co_occurrence_matrix(amino_acid_sequence)
        
        # Calculando a correlação
        correlation_matrix = co_occurrence_matrix.corr()
        
        # Exibindo a matriz de correlação
        st.subheader(f"Matriz de Correlação dos Aminoácidos da Proteína: {gene_name}")
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

        # Obtendo a matriz de correlação sem os valores 1 (diagonais)
        correlation_values = correlation_matrix.values

        # Substituindo os valores 1 por NaN para ignorá-los na busca pela maior correlação
        np.fill_diagonal(correlation_values, np.nan)

        # Encontrando o maior valor de correlação que não seja 1
        max_correlation_value = np.nanmax(correlation_values)

        # Encontrando a menor correlação (excluindo NaN)
        min_correlation_value = np.nanmin(correlation_values)

        

        st.write("A matriz de correlação é uma matriz simétrica que mostra a correlação entre os aminoácidos da proteína. "
                 "Valores próximos de 1 indicam uma forte correlação positiva, enquanto valores próximos de -1 indicam uma forte correlação negativa. ")
        
        # Exibindo os valores
        st.write(f"A maior correlação entre aminoácidos diferentes tem o valor de {max_correlation_value:.2f} e a menor correlação tem o valor de {min_correlation_value:.2f}.")
        st.write(f" maior correlação ocorre entre os aminoácidos {correlation_matrix.stack().idxmax()} e a menor correlação ocorre entre os aminoácidos {correlation_matrix.stack().idxmin()}.")
    else:
        st.warning("Por favor, digite o nome do gene.")
