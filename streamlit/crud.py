from db_connect import connect_db

# Função para inserir um novo filme
def insert_filme(num_filme, titulo_original, titulo_brasil, diretor, ano_lancamento, pais_origem, categoria, duracao):
    db = connect_db()
    cursor = db.cursor()
    diret_c = diretor.title()

    query = "SELECT nome_diretor FROM diretor WHERE nome_diretor = %s"
    cursor.execute(query, (diret_c,))
    result = cursor.fetchone()

    if result is None:
        query = "INSERT INTO diretor (nome_diretor, num_diretor) VALUES (%s, %s)"
        cursor.execute(query, (diret_c, max_diretor_key()))
        db.commit()

    query = """
        INSERT INTO filme (num_filme, titulo_original, titulo_brasil, nome_diretor, ano_lancamento, pais_origem, categoria, duracao)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (num_filme, titulo_original, titulo_brasil, diret_c, ano_lancamento, pais_origem, categoria, duracao)
    cursor.execute(query, values)
    db.commit()

# Função para pegar o próximo número de filme disponível
def get_new_numfilm():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT MAX(num_filme) FROM filme")
    num_filme = cursor.fetchone()
    return num_filme[0] + 1

# Função para ler todos os diretores
def get_diretores():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT nome_diretor FROM diretor")
    diretores = cursor.fetchall()
    for i in range(len(diretores)):
        diretores[i] = diretores[i][0]
    return diretores

# Verifica a maior chave de diretor
def max_diretor_key():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT MAX(num_diretor) FROM diretor")
    num_diretor = cursor.fetchone()
    return num_diretor[0] + 1

# Função para inserir diretor
def insert_diretor(nome_diretor):
    db = connect_db()
    cursor = db.cursor()
    query = """
        INSERT INTO diretor (nome_diretor)
        VALUES (%s)
    """
    cursor.execute(query, (nome_diretor,))
    db.commit()

# Função para remover diretor
def remover_diretor(nome_diretor):
    db = connect_db()
    cursor = db.cursor()
    query = """
        DELETE FROM diretor WHERE nome_diretor = %s
    """
    cursor.execute(query, (nome_diretor,))
    db.commit()                                                      

# Função para ler todos os filmes
def get_filmes():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM filme")
    filmes = cursor.fetchall()
    return filmes

# Função para atualizar um filme
def update_filme(num_filme, titulo_original, titulo_brasil, ano_lancamento, pais_origem, categoria, duracao, nome_diretor):
    db = connect_db()
    cursor = db.cursor()
    query = """
        UPDATE filme
        SET titulo_original = %s, titulo_brasil = %s, ano_lancamento = %s, pais_origem = %s, categoria = %s, duracao = %s, nome_diretor = %s
        WHERE num_filme = %s
    """
    values = (titulo_original, titulo_brasil, ano_lancamento, pais_origem, categoria, duracao, nome_diretor, num_filme)
    cursor.execute(query, values)
    db.commit()

# Função para deletar um filme
def delete_filme(num_filme):
    db = connect_db()
    cursor = db.cursor()
    query = "DELETE FROM filme WHERE num_filme = %s"
    cursor.execute(query, (num_filme,))
    db.commit()

# Função para buscar uma exibição
def get_exibicoes():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT f.titulo_brasil, c.nome, e.data
        FROM exibicao e
        JOIN filme f ON e.num_filme = f.num_filme
        JOIN canal c ON e.num_canal = c.num_canal
    """)
    exibicoes = cursor.fetchall()
    return exibicoes
def update_diretor(num_filme, num_diretor):
    db = connect_db()
    cursor = db.cursor()
    query = """
        UPDATE filme
        SET num_diretor = %s
        WHERE num_filme = %s
    """
    values = (num_diretor, num_filme)
    cursor.execute(query, values)
    db.commit()

# Consulta os filmes mais recentes
def get_filmes_recentes(conn, limit=5):
    cursor = conn.cursor()
    query = "SELECT * FROM filme ORDER BY num_filme DESC LIMIT %s"
    cursor.execute(query, (limit,))
    filmes = cursor.fetchall()
    cursor.close()
    return filmes

# Consulta de filmes com filtros de pesquisa
def get_filmes_filtrado(titulo, cat, ano, pais, diretor):
    db = connect_db()
    cursor = db.cursor()

    print(titulo, cat, ano, pais, diretor)

    # Query base
    query = """
        SELECT * FROM filme
        WHERE (%s IS NULL OR (titulo_brasil LIKE %s OR titulo_original LIKE %s))
        AND (%s IS NULL OR categoria = %s)
        AND (%s IS NULL OR ano_lancamento = %s)
        AND (%s IS NULL OR pais_origem = %s)
        AND (%s IS NULL OR nome_diretor = %s)
    """

    # Atribuir None para variáveis vazias e evitar problemas com %s
    if titulo:
        titulo = f"%{titulo}%"

    # Executar a query com os valores
    cursor.execute(query, (titulo, titulo, titulo, cat, cat, ano, ano, pais, pais, diretor, diretor))
    filmes = cursor.fetchall()
    return filmes

# Consulta se o filme já está cadastrado
def filme_ja_cadastrado(titulo_brasil):
    db = connect_db()
    cursor = db.cursor()

    # Query para verificar se o filme com o mesmo título já está cadastrado
    query = """
        SELECT COUNT(*) FROM filme
        WHERE titulo_brasil = %s
    """
    cursor.execute(query, (titulo_brasil,))
    result = cursor.fetchone()

    # Se o resultado for maior que 0, significa que já existe um filme com o mesmo título
    return result[0] > 0

# Consulta o filme por ano
def get_filmes_por_ano(conn):
    query = """
    SELECT ano_lancamento, COUNT(*) as total
    FROM filme
    GROUP BY ano_lancamento
    ORDER BY ano_lancamento ASC
    """
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

# Função para exclusão de diretor em cascata
def delete_diretoraf(nome_diretor):
    db = connect_db()
    cursor = db.cursor()
    query = "SELECT num_filme FROM filme WHERE nome_diretor = %s"
    cursor.execute(query, (nome_diretor,))
    result = cursor.fetchall()
    print(result)
    
    for i in range(len(result)):
        query = "DELETE FROM exibicao WHERE num_filme = %s"
        cursor.execute(query, (result[i][0],))
        db.commit()
        print('Exibicao deletada')

    query = "DELETE FROM filme WHERE nome_diretor = %s"
    cursor.execute(query, (nome_diretor,))
    db.commit()
    print('Filme deletado')

    query = "DELETE FROM diretor WHERE nome_diretor = %s"
    cursor.execute(query, (nome_diretor,))
    db.commit()
    print('Diretor deletado')
    print('Ready to rock!')

# Função de início de rotina
def start_routine():
    db = connect_db()
    cursor = db.cursor()

    query = "SELECT nome_diretor FROM diretor"
    cursor.execute(query, "")
    result_diretor = cursor.fetchall()

    query = "SELECT nome_diretor FROM filme"
    cursor.execute(query, "")
    result_filme = cursor.fetchall()

    for i in range(len(result_diretor)):
        if result_diretor[i] not in result_filme:
            query = "DELETE FROM diretor WHERE nome_diretor = %s"
            values = (result_diretor[i][0], )
            cursor.execute(query, values)
            db.commit()

__all__ = ['insert_filme', 'get_filmes', 'update_filme', 'delete_filme', 'get_exibicoes', 'get_filmes_recentes', 'get_filmes_filtrado', 'get_filmes_por_ano', 'filme_ja_cadastrado', 'get_new_numfilm', 'get_diretores', 'insert_diretor', 'get_diretor_key', 'pesquisa_diretor', 'remove_diretor', 'start_routine', 'delete_diretoraf']