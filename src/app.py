import streamlit as st
import pandas as pd
from crud import insert_filme, get_filmes, update_filme, delete_filme, get_filmes_recentes, get_filmes_filtrado, get_filmes_por_ano
from db_connect import connect_db 

# Conectando ao banco de dados
conn = connect_db()

# Título do aplicativo
st.title("Sistema de Programação de Filmes 🎬")

st.markdown("""
    <style>
        /* Cor de fundo do app */
        .main { background-color: #000000; }

        /* Títulos */
        h1, h2, h3 { color: #FFFFFF; }
            
        /* Botões */
        .stButton>button { background-color: #FFD700; color: #000000; border: none; }
        .stButton>button:hover { background-color: #FFFFFF; color: #000000; }

        /* Painéis de dados */
        .stDataFrame>div>div { border: none; } 

        /* Mensagens de sucesso */
        .stSuccess { color: #00FF00; font-weight: bold; }

        /* Páginas CRUD */
        .crud-page { 
            background-color: #ffffff; 
            border-radius: 10px;
        }
        
        /* Cor do texto dentro das caixas de input */
        .stTextInput input, .stNumberInput input, .stSelectbox select {
            color: #FFFFFF;  /* Texto branco dentro das caixas */
        }

        /* Cor dos labels acima das caixas de input */
        .stTextInput label, .stNumberInput label, .stSelectbox label {
            color: #FFFFFF;  /* Labels brancos acima das caixas */
            font-weight: bold;
        }

        /* Ajuste de margens do conteúdo */
        form {
            margin-top: 0;  /* Elimina o espaçamento acima do formulário */
            margin-bottom: 0; /* Elimina o espaçamento abaixo do formulário */
        }

        /* Remover estilização da tabela de filmes recentemente adicionados */
        .result-table {
            background-color: initial; /* Remove o fundo personalizado */
            padding: 0; /* Remove o padding */
            border-radius: 0; /* Remove o arredondamento */
        }
        .result-table th, .result-table td {
            background-color: initial; /* Remove o fundo das células */
            color: initial; /* Remove a cor personalizada do texto */
        }
    </style>
""", unsafe_allow_html=True)



# Inicializando o estado da página
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Início"

# Função para mudar a página
def change_page(page):
    st.session_state.current_page = page

# Exibindo a tela inicial e botões de navegação
if st.session_state.current_page == "Início":
    st.subheader("Filmes Recentemente Adicionados")
    
    # Exibindo filmes recentes
    filmes_recentes = get_filmes_recentes(conn)
    df = pd.DataFrame(filmes_recentes, columns=["Número", "Título Original", "Título Brasil", "Ano", "País", "Categoria", "Duração", "Diretor", "Coluna Extra"])
    html = df.to_html(index=False, classes='result-table')
    st.markdown(html, unsafe_allow_html=True)


    st.subheader("Extras")
    col1, = st.columns(1)
    with col1:
        if st.button("Gráficos ➡️"):
            change_page("Gráficos")
    
    # Exibindo botões para navegação entre os CRUD
    st.subheader("Ações CRUD")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("Cadastrar Filme ➕"):
            change_page("Cadastrar Filme")

    with col2:
        if st.button("Consultar Filmes ❔"):
            change_page("Consultar Filmes")

    with col3:
        if st.button("Atualizar Filme ✏️"):
            change_page("Atualizar Filme")

    with col4:
        if st.button("Remover Filme 🗑️"):
            change_page("Remover Filme")

# Páginas de CRUD baseadas no estado da sessão
elif st.session_state.current_page == "Cadastrar Filme":
    st.markdown("<div class='crud-page'>", unsafe_allow_html=True)
    st.subheader("Cadastro de Filmes")
    
    with st.form("Cadastro Filme"):
        num_filme = st.number_input("Número do Filme", min_value=1)
        titulo_original = st.text_input("Título Original")
        titulo_brasil = st.text_input("Título no Brasil")
        ano_lancamento = st.number_input("Ano de Lançamento", min_value=1800, max_value=2024)
        pais_origem = st.text_input("País de Origem")
        categoria = st.selectbox("Categoria", ["Animação", "Drama", "Comédia", "Romance", "Ação", "Ficção Científica", "Nome do Diretor"])
        duracao = st.number_input("Duração (minutos)", min_value=1)
        num_diretor = st.text_input("Nome do Diretor")

        if st.form_submit_button("Cadastrar"):
            insert_filme(num_filme, titulo_original, titulo_brasil, ano_lancamento, pais_origem, categoria, duracao, num_diretor)
            st.markdown(f"<div class='stSuccess'>Filme '{titulo_brasil}' cadastrado com sucesso!</div>", unsafe_allow_html=True)
    
    if st.button("Voltar"):
        change_page("Início")  # Botão para retornar à página inicial

    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.current_page == "Consultar Filmes":
    st.markdown("<div class='crud-page'>", unsafe_allow_html=True)
    st.subheader("Lista de Filmes")

    # Formulário de pesquisa
    form = st.form('pesquisa_filmes')

    with form:
        titulo = st.text_input("Digite o título do filme")
        cat = st.selectbox("Selecione a categoria", ["", "Animação", "Drama", "Comédia", "Romance", "Ação", "Ficção Científica"], placeholder='')
        ano = st.number_input("Digite o ano de lançamento", min_value=1800, max_value=2024, value=None)
        pais = st.selectbox("Selecione o país de origem", ["", "Brasil", "Estados Unidos", "França", "Itália", "Japão", "Reino Unido"], placeholder='')
        src = st.form_submit_button("Pesquisar")


    # Filtrar os filmes
    if src:
        filmes = get_filmes_filtrado(titulo, cat, ano, pais)
        df = pd.DataFrame(filmes, columns=["Número", "Título Original", "Título Brasil", "Ano", "País", "Categoria", "Duração","Diretor", "Coluna Adicional"])
        
        if df.empty:
            st.markdown("<div class='stSuccess'>Nenhum filme encontrado com os filtros selecionados!</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='stSuccess'>Filmes encontrados com sucesso!</div>", unsafe_allow_html=True)
            st.dataframe(df, height=400)  # Set the height of the dataframe

    else:
        # Se não há pesquisa, exibir todos os filmes
        filmes = get_filmes()
        df = pd.DataFrame(filmes, columns=["Número", "Título Original", "Título Brasil", "Ano", "País", "Categoria", "Duração","Diretor", "Coluna Adicional"])
        st.dataframe(df)

    # Botão de voltar
    if st.button("Voltar"):
        change_page("Início")  # Botão para retornar à página inicial

    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.current_page == "Atualizar Filme":
    st.markdown("<div class='crud-page'>", unsafe_allow_html=True)
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

            if st.form_submit_button("Atualizar"):
                update_filme(num_filme, titulo_original, titulo_brasil, ano_lancamento, pais_origem, categoria, duracao)
                st.markdown(f"<div class='stSuccess'>Filme '{titulo_brasil}' atualizado com sucesso!</div>", unsafe_allow_html=True)
    
    if st.button("Voltar"):
        change_page("Início")  # Botão para retornar à página inicial

    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.current_page == "Remover Filme":
    st.markdown("<div class='crud-page'>", unsafe_allow_html=True)
    st.subheader("Remover Filme")
    filmes = get_filmes()
    filme_selecionado = st.selectbox("Selecione um Filme para Remover", filmes, format_func=lambda x: x[2])
    
    if st.button(f"Remover '{filme_selecionado[2]}'"):
        delete_filme(filme_selecionado[0])
        st.markdown(f"<div class='stSuccess'>Filme '{filme_selecionado[2]}' removido com sucesso!</div>", unsafe_allow_html=True)
    
    if st.button("Voltar"):
        change_page("Início")  

    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.current_page == "Gráficos":
    st.subheader("Gráficos")
    st.write("Aqui você pode adicionar gráficos personalizados")

     # Gráfico de filmes por ano
    st.subheader("Filmes por Ano")
    
    # Obter dados para o gráfico
    filmes_por_ano = get_filmes_por_ano(conn)
    
    # Transformar em DataFrame
    df_ano = pd.DataFrame(filmes_por_ano, columns=["Ano", "Total de Filmes"])
    
    # Exibir gráfico de barras
    st.bar_chart(df_ano.set_index('Ano'))
    if st.button("Voltar"):
        change_page("Início")  # Botão para retornar à página inicial

    st.markdown("</div>", unsafe_allow_html=True)



conn.close()