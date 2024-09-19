import streamlit as st
import pandas as pd
from crud import insert_filme, get_filmes, update_filme, delete_filme, get_exibicoes

# Título do aplicativo
st.title("Sistema de Programação de Filmes 🎬")

# Menu de navegação
menu = ["Cadastrar Filme", "Consultar Filmes", "Atualizar Filme", "Remover Filme", "Exibições"]
choice = st.sidebar.selectbox("Menu", menu)

# Cadastro de filme
if choice == "Cadastrar Filme":
    st.subheader("Cadastro de Filmes")
    
    with st.form("Cadastro Filme"):
        num_filme = st.number_input("Número do Filme", min_value=1)
        titulo_original = st.text_input("Título Original")
        titulo_brasil = st.text_input("Título no Brasil")
        ano_lancamento = st.number_input("Ano de Lançamento", min_value=1800, max_value=2024)
        pais_origem = st.text_input("País de Origem")
        categoria = st.selectbox("Categoria", ["Animação", "Drama", "Comédia", "Romance", "Ação", "Ficção Científica"])
        duracao = st.number_input("Duração (minutos)", min_value=1)

        if st.form_submit_button("Cadastrar"):
            insert_filme(num_filme, titulo_original, titulo_brasil, ano_lancamento, pais_origem, categoria, duracao)
            st.success(f"Filme '{titulo_brasil}' cadastrado com sucesso!")

# Consulta de filmes
elif choice == "Consultar Filmes":
    st.subheader("Lista de Filmes")
    filmes = get_filmes()
    df = pd.DataFrame(filmes, columns=["Número", "Título Original", "Título Brasil", "Ano", "País", "Categoria", "Duração",'Número do Diretor'])
    st.dataframe(df)

# Atualização de filmes
elif choice == "Atualizar Filme":
    st.subheader("Atualizar Filme")
    filmes = get_filmes()
    filme_selecionado = st.selectbox("Selecione um Filme", filmes, format_func=lambda x: x[2])
    
    if filme_selecionado:
        with st.form("Atualizar Filme"):
            num_filme = filme_selecionado[0]
            titulo_original = st.text_input("Título Original", value=filme_selecionado[1])
            titulo_brasil = st.text_input("Título no Brasil", value=filme_selecionado[2])
            ano_lancamento = st.number_input("Ano de Lançamento", min_value=1800, max_value=2024, value=filme_selecionado[3])
            pais_origem = st.text_input("País de Origem", value=filme_selecionado[4])
            categoria = st.text_input("Categoria", value=filme_selecionado[5])
            duracao = st.number_input("Duração", min_value=1, value=filme_selecionado[6])
            num_diretor = st.number_input("Número do Diretor", min_value=1, value=filme_selecionado[7])

            if st.form_submit_button("Atualizar"):
                update_filme(num_filme, titulo_original, titulo_brasil, ano_lancamento, pais_origem, categoria, duracao)
                st.success(f"Filme '{titulo_brasil}' atualizado com sucesso!")

# Remover filme
elif choice == "Remover Filme":
    st.subheader("Remover Filme")
    filmes = get_filmes()
    filme_selecionado = st.selectbox("Selecione um Filme para Remover", filmes, format_func=lambda x: x[2])
    
    if st.button(f"Remover '{filme_selecionado[2]}'"):
        delete_filme(filme_selecionado[0])
        st.success(f"Filme '{filme_selecionado[2]}' removido com sucesso!")

# Exibições de filmes
elif choice == "Exibições":
    st.subheader("Exibições de Filmes")
    exibicoes = get_exibicoes()
    df = pd.DataFrame(exibicoes, columns=["Filme", "Canal", "Data/Hora"])
    st.dataframe(df)
