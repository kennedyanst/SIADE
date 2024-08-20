import streamlit as st
import pandas as pd
from PIL import Image
from collections import Counter

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
    st.subheader(f"Código Genético: {gene_name}")
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
            rna_sequence = sequence.replace("T", "U")  # Transcreve DNA para RNA
            
            for i in range(0, len(rna_sequence), 3):
                codon = rna_sequence[i:i+3]
                if len(codon) == 3:
                    amino_acid = codon_to_amino_acid.get(codon, "Unknown")
                    amino_acid_sequence.append(amino_acid)
            
            return amino_acid_sequence
        
        # Traduzindo a sequência de nucleotídeos em aminoácidos
        amino_acid_sequence = translate_sequence(sequence, codon_to_amino_acid)
        
        # Contando a quantidade de cada aminoácido
        amino_acid_counts = Counter(amino_acid_sequence)
        
        # Criando um DataFrame para exibir a tabela
        df_amino_acids = pd.DataFrame(amino_acid_counts.items(), columns=['Aminoácido', 'Quantidade'])
        
        # Exibindo a tabela de aminoácidos e suas quantidades
        st.subheader(f"Tabela de Aminoácidos para: {gene_name}")
        st.table(df_amino_acids)
    else:
        st.warning("Por favor, digite o nome do gene.")
