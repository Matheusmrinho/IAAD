from db_connect import connect_db


# Função para inserir um novo filme
def insert_filme(num_filme, titulo_original, titulo_brasil, ano_lancamento, pais_origem, categoria, duracao, num_diretor):
    db = connect_db()
    cursor = db.cursor()
    query = """
        INSERT INTO filme (num_filme, titulo_original, titulo_brasil, ano_lancamento, pais_origem, categoria, duracao, num_diretor)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (num_filme, titulo_original, titulo_brasil, ano_lancamento, pais_origem, categoria, duracao, num_diretor)
    cursor.execute(query, values)
    db.commit()

# Função para ler todos os filmes
def get_filmes():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT f.*, d.num_diretor AS num_diretor
        FROM filme f
        LEFT JOIN diretor d ON f.num_diretor = d.num_diretor
    """)
    filmes = cursor.fetchall()
    return filmes

# Função para atualizar um filme
def update_filme(num_filme, titulo_original, titulo_brasil, ano_lancamento, pais_origem, categoria, duracao, num_diretor):
    db = connect_db()
    cursor = db.cursor()
    query = """
        UPDATE filme
        SET titulo_original = %s, titulo_brasil = %s, ano_lancamento = %s, pais_origem = %s, categoria = %s, duracao = %s, num_diretor = %s
        WHERE num_filme = %s
    """
    values = (titulo_original, titulo_brasil, ano_lancamento, pais_origem, categoria, duracao, num_diretor, num_filme)
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

def get_filmes_recentes(conn, limit=5):
    cursor = conn.cursor()
    query = """
        SELECT f.*, d.num_diretor AS num_diretor
        FROM filme f
        LEFT JOIN diretor d ON f.num_diretor = d.num_diretor
        ORDER BY f.num_filme DESC LIMIT %s
    """
    cursor.execute(query, (limit,))
    filmes = cursor.fetchall()
    cursor.close()
    return filmes

def get_filmes_filtrado(titulo, cat, ano, pais, num_diretor=None):
    db = connect_db()
    cursor = db.cursor()

    if titulo == "": titulo = None
    if cat == "": cat = None
    if ano == "": ano = None
    if pais == "": pais = None
    
    query = """
        SELECT f.*, d.num_diretor AS num_diretor
        FROM filme f
        LEFT JOIN diretor d ON f.num_diretor = d.num_diretor
        WHERE (f.titulo_brasil LIKE %s OR %s IS NULL)
        AND (f.categoria = %s OR %s IS NULL)
        AND (f.ano_lancamento = %s OR %s IS NULL)
        AND (f.pais_origem = %s OR %s IS NULL)
        AND (f.num_diretor = %s OR %s IS NULL)
    """
    values = (f"%{titulo}%", f"%{titulo}%", cat, cat, ano, ano, pais, pais, num_diretor, num_diretor)
    cursor.execute(query, values)
    filmes = cursor.fetchall()
    return filmes

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

__all__ = ['insert_filme', 'get_filmes', 'update_filme', 'delete_filme', 'get_exibicoes', 'get_filmes_recentes', 'get_filmes_filtrado', 'get_filmes_por_ano']
