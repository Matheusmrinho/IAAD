import streamlit as st
import pandas as pd
from crud import filme_ja_cadastrado, insert_filme, get_filmes, update_filme, delete_filme, get_filmes_recentes, get_filmes_filtrado, get_filmes_por_ano, get_new_numfilm, get_diretores, start_routine
from db_connect import connect_db 
import plotly.express as px
from datetime import datetime

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

        /* Botões (remover o fundo amarelo e deixar o padrão) */
        .stButton>button { 
            color: #FFFFFF;  /* Cor do texto preto */
            border: 1px solid #000000;  /* Borda preta opcional */
        }
        .stButton>button:hover { 
            background-color: #FFFFFF;  /* Fundo branco ao passar o mouse */
            color: #000000;  /* Texto preto */
        }

        /* Painéis de dados */
        .stDataFrame>div>div { border: none; }

        /* Mensagens de sucesso */
        .stSuccess { color: #00FF00; font-weight: bold; }

        /* Páginas CRUD */
        .crud-page {
            background-color: #FFFFFF;
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

        /* Estilização da tabela de filmes recentemente adicionados */
        .result-table {
            background-color: initial; /* Remove o fundo personalizado */
            padding: 0; /* Remove o padding */
            border-radius: 0; /* Remove o arredondamento */
            text-align: center; /* Centraliza o texto na tabela */
        }
        .result-table th, .result-table td {
            background-color: initial; /* Remove o fundo das células */
            color: initial; /* Remove a cor personalizada do texto */
            text-align: center;  /* Centraliza o texto das células */
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
    start_routine()
    st.subheader("Filmes Recentemente Adicionados")
    
    # Exibindo filmes recentes
    filmes_recentes = get_filmes_recentes(conn)  
    df = pd.DataFrame(filmes_recentes, columns=["Número", "Título Original", "Título Brasil", "Ano", "País", "Categoria", "Duração", "Diretor", "Exibições"])
    html = df.to_html(index=False, classes='result-table')
    st.markdown(html, unsafe_allow_html=True)

    st.subheader("Extras")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Gráficos ➡️"):
            change_page("Gráficos")
    
    with col2:
        if st.button("Triggers ➡️"):
            change_page("Triggers")
    
    with col3:
        if st.button("View ➡️"):
            change_page("View")
    
    
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
        diretores = get_diretores()
        num_value = get_new_numfilm()
        num_filme = st.number_input("Número do Filme", min_value=int(num_value))
        titulo_original = st.text_input("Título Original")
        titulo_brasil = st.text_input("Título no Brasil")
        diretor = st.text_input("Diretor")
        ano_lancamento = st.number_input("Ano de Lançamento", min_value=1901, max_value=datetime.now().year)
        pais_origem = st.text_input("País de Origem")
        categoria = st.selectbox("Categoria", ["Animação", "Drama", "Comédia", "Romance", "Ação", "Ficção Científica"])
        duracao = st.number_input("Duração (minutos)", min_value=1)

        if st.form_submit_button("Cadastrar"):
        # Verificar se o filme já existe com base no título original
            if filme_ja_cadastrado(titulo_brasil):
        # Exibir mensagem de erro se o filme já estiver cadastrado
                 st.markdown(
            f"<div class='stError'>Erro: O filme '{titulo_brasil}' já está cadastrado! Tente um título diferente.</div>",
            unsafe_allow_html=True
        )
            else:
                try:
                    # Inserir o filme no banco de dados
                    insert_filme(num_filme, titulo_original, titulo_brasil, diretor, ano_lancamento, pais_origem, categoria, duracao)
                    st.markdown(f"<div class='stSuccess'>Filme '{titulo_brasil}' cadastrado com sucesso!</div>", unsafe_allow_html=True)
                #except Exception as e:
                    #st.markdown("<div class='stError'>Erro: O índice já existe. Tente cadastrar um filme com um número diferente!</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f"<div class='stError'>Erro: {e}</div>", unsafe_allow_html=True)

    
    if st.button("Voltar"):
        change_page("Início")  # Botão para retornar à página inicial

    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.current_page == "Consultar Filmes":
    st.markdown("<div class='crud-page'>", unsafe_allow_html=True)
    st.subheader("Lista de Filmes")

    # Formulário de pesquisa
    form = st.form('pesquisa_filmes')

    with form:
        titulo = st.text_input("Digite o título do filme", placeholder="Título em inglês ou português")
        cat = st.selectbox("Selecione a categoria", ["", "Animação", "Drama", "Comédia", "Romance", "Ação", "Ficção Científica"], placeholder='')
        diretor = st.selectbox("Selecione o diretor", [""] + get_diretores(), placeholder='')
        ano = st.number_input("Digite o ano de lançamento", min_value=1901, max_value=datetime.now().year, value=None)
        pais = st.selectbox("Selecione o país de origem", ["", "Brasil", "EUA", "França", "Itália", "Japão", "Reino Unido"], placeholder='')
        src = st.form_submit_button("Pesquisar")


     # Filtrar os filmes
    if src:
        # Tratar campos vazios como None para a consulta
        if not titulo:
            titulo = None
        if not cat:
            cat = None
        if ano == 0:  # Evitar o valor 0 para o ano
            ano = None
        if not pais:
            pais = None
        if not diretor:
            diretor = None

        # Obter filmes filtrados
        filmes = get_filmes_filtrado(titulo, cat, ano, pais, diretor)
        df = pd.DataFrame(filmes, columns=["Número", "Título Original", "Título Brasil", "Ano", "País", "Categoria", "Duração", "Diretor", "Exibições"])
        
        if df.empty:
            st.markdown("<div class='stSuccess'>Nenhum filme encontrado com os filtros selecionados!</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='stSuccess'>Filmes encontrados com sucesso!</div>", unsafe_allow_html=True)
            st.dataframe(df, height=400)  # Define o tamanho da tabela exibida

    else:
        # Se não há pesquisa, exibir todos os filmes
        filmes = get_filmes()
        df = pd.DataFrame(filmes, columns=["Número", "Título Original", "Título Brasil", "Ano", "País", "Categoria", "Duração", "Diretor", "Exibições"])
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
            diretor = st.text_input("Diretor", value=filme_selecionado[7])
            ano_lancamento = st.number_input("Ano de Lançamento", min_value=1901, max_value=datetime.now().year, value=filme_selecionado[3])
            pais_origem = st.text_input("País de Origem", value=filme_selecionado[4])
            categoria = st.text_input("Categoria", value=filme_selecionado[5])
            duracao = st.number_input("Duração", min_value=1, value=filme_selecionado[6])
            
            if st.form_submit_button("Atualizar"):
                update_filme(num_filme, titulo_original, titulo_brasil, ano_lancamento, pais_origem, categoria, duracao, diretor)
                st.markdown(f"<div class='stSuccess'>Filme '{titulo_brasil}' atualizado com sucesso!</div>", unsafe_allow_html=True)

    
    if st.button("Voltar"):
        change_page("Início")  

    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.current_page == "Remover Filme":
    st.markdown("<div class='crud-page'>", unsafe_allow_html=True)
    st.subheader("Remover Filme")
    filmes = get_filmes()
    filme_selecionado = st.selectbox("Selecione um Filme para Remover", filmes, format_func=lambda x: x[2])
    
    if st.button(f"Remover '{filme_selecionado[2]}'"):
        try:
            delete_filme(filme_selecionado[0])
            st.markdown(f"<div class='stSuccess'>Filme '{filme_selecionado[2]}' removido com sucesso!</div>", unsafe_allow_html=True)
            st.session_state.current_page = "Remover Filme"
        except Exception as e:
            st.markdown(f"<div class='stError'>Erro ao remover filme: ele está em exibição</div>", unsafe_allow_html=True)
    
    if st.button("Voltar"):
        change_page("Início")  

    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.current_page == "Modo Pesquisa":
    st.markdown("<div class='crud-page'>", unsafe_allow_html=True)
    st.subheader("Pesquisa de Filmes")
    form = st.form('filme')

    # Adicionando filtros
    with form:
        titulo = st.text_input("Digite o título do filme")
        cat = st.selectbox("Selecione a categoria", ["", "Animação", "Drama", "Comédia", "Romance", "Ação", "Ficção Científica"], placeholder='')
        ano = st.number_input("Digite o ano de lançamento", min_value=1901, max_value=datetime.now().year, value=None)
        pais = st.selectbox("Selecione o país de origem", ["", "Brasil", "Estados Unidos", "França", "Itália", "Japão", "Reino Unido"], placeholder='')
        src = st.form_submit_button("Pesquisar")

    # Função para filtrar os filmes
    if src:
        filmes = get_filmes_filtrado(titulo, cat, ano, pais)
        print(filmes)
        df = pd.DataFrame(filmes, columns=["Número", "Título Original", "Título Brasil", "Ano", "País", "Categoria", "Duração", "Diretor", "Exibições"])
        
        if df.empty:
            st.markdown("<div class='stSuccess'>Nenhum filme encontrado com os filtros selecionados!</div>", unsafe_allow_html=True)
        else:
            st.dataframe(df, height=300, width=800)
    
    if st.button("Voltar"):
        change_page("Início")  # Botão para retornar à página inicial

    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.current_page == "Gráficos":
    st.markdown("<div class='crud-page'>", unsafe_allow_html=True)
    st.subheader("Gráficos de Filmes")

    # Gráfico de filmes por ano
    st.subheader("Pesquise sobre os filmes!")

    
    filmes_dados = get_filmes()  

    # Transformar em DataFrame
    df_filmes = pd.DataFrame(filmes_dados, columns=["Número", "Título Original", "Título Brasil", "Ano", "País", "Categoria", "Duração", "Diretor", "Exibições"])

    # Exibir uma lista para o usuário selecionar qual dado será mostrado no gráfico
    opcoes = ["Ano", "País", "Duração", "Diretor"]  
    variavel_escolhida = st.selectbox("Escolha a variável para mostrar no gráfico", opcoes)


    # Contar os filmes por variável escolhida
    if variavel_escolhida == "Ano":
        filmes_por_variavel = df_filmes.groupby("Ano").size().reset_index(name='Total de Filmes')
    elif  variavel_escolhida == "País":
        filmes_por_variavel = df_filmes.groupby("País").size().reset_index(name='Total de Filmes')
    elif variavel_escolhida == "Duração":
        filmes_por_variavel = df_filmes.groupby("Duração").size().reset_index(name='Total de Filmes')
    elif variavel_escolhida == "Diretor":
        filmes_por_variavel = df_filmes.groupby("Diretor").size().reset_index(name='Total de Filmes')

    # Exibir o gráfico de barras com base na variável escolhida
    st.bar_chart(filmes_por_variavel.set_index(variavel_escolhida)['Total de Filmes'])

    # Obter todos os dados dos filmes
    filmes_dados = get_filmes()  # Ajuste conforme necessário
    df_filmes = pd.DataFrame(filmes_dados, columns=["Número", "Título Original", "Título Brasil", "Ano", "País", "Categoria", "Duração", "Diretor", "Exibições"])

    # Escolha das variáveis
    opcoes_variaveis = ["Ano", "País", "Duração", "Diretor"] 

    variavel_x = st.selectbox("Escolha a variável para o eixo X", opcoes_variaveis)
    variavel_y = st.selectbox("Escolha a variável para o eixo Y", opcoes_variaveis)

        # Filtrando dados para o gráfico
    if variavel_x == "Ano":
        x_data = df_filmes['Ano']
    elif variavel_x == "Duração":
        x_data = df_filmes['Duração']
    elif variavel_x == 'País':
        x_data = df_filmes['País']
    else:
        x_data = df_filmes['Diretor']

    if variavel_y == "Ano":
        y_data = df_filmes['Ano']
    elif variavel_y == "Duração":
        y_data = df_filmes['Duração']
    elif variavel_y == 'País':
        y_data = df_filmes['País']
    else:
        y_data = df_filmes['Diretor']
    # Exibir gráfico de dispersão
    st.subheader(f"Gráfico de Dispersão: {variavel_x} vs {variavel_y}")
    if not x_data.empty and not y_data.empty:
        scatter_data = pd.DataFrame({variavel_x: x_data, variavel_y: y_data})
    if variavel_x == "País":
        scatter_data[variavel_x] = scatter_data[variavel_x].astype(str)
    # Exibir gráfico de dispersão
    st.write(scatter_data)
    st.bar_chart(scatter_data.set_index(variavel_x))
    fig = px.scatter(scatter_data, x=variavel_x, y=variavel_y, title=f"Gráfico de Dispersão: {variavel_x} vs {variavel_y}")
    st.plotly_chart(fig)

    def plot_filmes_por_diretor():
        filmes_dados = get_filmes()  
    df_filmes = pd.DataFrame(filmes_dados, columns=["Número", "Título Original", "Título Brasil", "Ano", "País", "Categoria", "Duração", "Diretor", "Exibições"])

    # Agrupar os filmes por diretor e coletar os títulos em uma lista
    filmes_por_diretor = df_filmes.groupby("Diretor")["Título Original"].apply(list).reset_index()
    filmes_por_diretor.columns = ["Diretor", "Títulos"]

    
    filmes_por_diretor["Número de Filmes"] = filmes_por_diretor["Títulos"].apply(len)

    
    fig = px.bar(filmes_por_diretor, 
                 x='Diretor', 
                 y='Número de Filmes', 
                 title='Número de Filmes por Diretor',
                 hover_data=['Títulos'],
                 labels={'Número de Filmes': 'Número de Filmes', 'Diretor': 'Diretor'})

    
    st.plotly_chart(fig)

    if st.button("Voltar"):
        change_page("Início")

elif st.session_state.current_page == "Triggers":
    st.markdown("<div class='crud-page'>", unsafe_allow_html=True)
    st.subheader("Triggers")

    query_filme_log = """
    SELECT * FROM filme_log
    WHERE new_titulo IS NOT NULL  -- Filtra para mostrar apenas as alterações de título
    """
    df_filme_log = pd.read_sql(query_filme_log, conn)
    st.write("Logs de Alterações em Títulos de Filmes")
    st.dataframe(df_filme_log)

    query_filme_delete_log = """
    SELECT * FROM filme_log 
    WHERE new_titulo IS NULL
    """
    df_filme_delete_log = pd.read_sql(query_filme_delete_log, conn)
    st.write("Logs de Exclusões de Filmes")
    st.dataframe(df_filme_delete_log)

    query_qtd_exibicoes = "SELECT num_filme, titulo_original, qtd_exibicoes FROM filme"
    df_qtd_exibicoes = pd.read_sql(query_qtd_exibicoes, conn)
    st.write("Quantidade de Exibições por Filme")
    st.dataframe(df_qtd_exibicoes)

    query_exibicao_log = "SELECT * FROM log_exibicao"
    df_exibicao_log = pd.read_sql(query_exibicao_log, conn)
    st.write("Logs de Alterações em Exibições")
    st.dataframe(df_exibicao_log)

    query_duracao_filme = "SELECT num_filme, titulo_original, duracao FROM filme WHERE duracao < 40"
    df_duracao_filme = pd.read_sql(query_duracao_filme, conn)
    st.write("Filmes com Duração Inferior a 40 Minutos")
    st.dataframe(df_duracao_filme)

    query_exibicoes_apos_delete = "SELECT * FROM exibicao"
    df_exibicoes_apos_delete = pd.read_sql(query_exibicoes_apos_delete, conn)
    st.write("Exibições Atuais Após Exclusões de Filmes")
    st.dataframe(df_exibicoes_apos_delete)

    query_canal_sigla = "SELECT num_canal, nome, sigla FROM canal"
    df_canal_sigla = pd.read_sql(query_canal_sigla, conn)
    st.write("Atualização Automática da Sigla dos Canais")
    st.dataframe(df_canal_sigla)

    if st.button("Voltar"):
        change_page("Início")

    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.current_page == "View":
    st.markdown("<div class='crud-page'>", unsafe_allow_html=True)
    st.subheader("View")

    query_view = "SELECT * FROM view_filmes_maior_100"
    df_view = pd.read_sql(query_view, conn)

    # Exibir os dados da view no Streamlit
    st.write("Visualização da View de Filmes com Duração ≥ 100 minutos")
    st.dataframe(df_view)

    query_view = "SELECT * FROM nome_filme_canal_data_exibicao"
    df_view = pd.read_sql(query_view, conn)

    st.write("Filmes com canais, datas, horários de exibição e categoria")
    st.dataframe(df_view)

    if st.button("Voltar"):
        change_page("Início")

    st.markdown("</div>", unsafe_allow_html=True)

conn.close()