import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar o Firebase Admin SDK
cred = credentials.Certificate("iaad-3d9ff-firebase-adminsdk-3mph7-da53c867a3.json")
firebase_admin.initialize_app(cred)

# Conectar ao Firestore
db = firestore.client()

# ------------------- CREATE  -------------------
def create_canal(num_canal, nome, sigla):
    # Verificar se o canal já existe
    if document_exists('canal', str(num_canal)):
        print(f'Erro: Canal com o número {num_canal} já existe.')
        return

    # Criar o canal se não houver duplicidade
    canal_ref = db.collection('canal').document(str(num_canal))
    canal_ref.set({
        'num_canal': num_canal,
        'nome': nome,
        'sigla': sigla
    })
    print(f'Canal {nome} criado com sucesso!')
    return canal_ref


def create_filme(num_filme, titulo_original, titulo_brasil, ano_lancamento, pais_origem, categoria, duracao):
    # Verificar se o filme já existe
    if document_exists('filme', str(num_filme)):
        print(f'Erro: Filme com o número {num_filme} já existe.')
        return

    # Criar o filme se não houver duplicidade
    filme_ref = db.collection('filme').document(str(num_filme))
    filme_ref.set({
        'num_filme': num_filme,
        'titulo_original': titulo_original,
        'titulo_brasil': titulo_brasil,
        'ano_lancamento': ano_lancamento,
        'pais_origem': pais_origem,
        'categoria': categoria,
        'duracao': duracao
    })
    print(f'Filme {titulo_original} criado com sucesso!')
    return filme_ref

def create_exibicao(num_filme, num_canal, data):
    # Verificar integridade: se o filme e o canal existem
    if not document_exists('filme', str(num_filme)):
        print(f'Erro: Filme {num_filme} não existe.')
        return
    if not document_exists('canal', str(num_canal)):
        print(f'Erro: Canal {num_canal} não existe.')
        return

    # Verificar se a exibição já existe
    exibicoes_existentes = db.collection('exibicao') \
        .where('filme_ref', '==', db.collection('filme').document(str(num_filme))) \
        .where('canal_ref', '==', db.collection('canal').document(str(num_canal))) \
        .where('data', '==', data).get()

    if exibicoes_existentes:
        print(f"Erro: Já existe uma exibição para o filme {num_filme} no canal {num_canal} na data {data}.")
        return

    # Criar exibição se não houver duplicidade
    filme_ref = db.collection('filme').document(str(num_filme))
    canal_ref = db.collection('canal').document(str(num_canal))
    
    exibicao_ref = db.collection('exibicao').document()
    exibicao_ref.set({
        'filme_ref': filme_ref,
        'canal_ref': canal_ref,
        'data': data
    })
    print(f'Exibição do filme {num_filme} no canal {num_canal} na data {data} criada com sucesso!')
    return exibicao_ref

# ------------------- READ -------------------
def read_canal(num_canal):
    canal_ref = db.collection('canal').document(str(num_canal))
    doc = canal_ref.get()
    if doc.exists:
        print(f'Canal encontrado: {doc.to_dict()}')
        return doc.to_dict()
    else:
        print('Canal não encontrado.')
        return None

def read_filme(num_filme):
    filme_ref = db.collection('filme').document(str(num_filme))
    doc = filme_ref.get()
    if doc.exists:
        print(f'Filme encontrado: {doc.to_dict()}')
        return doc.to_dict()
    else:
        print('Filme não encontrado.')
        return None

def read_exibicao(num_filme, num_canal):
    # Verificar integridade: se o filme e o canal existem
    if not document_exists('filme', str(num_filme)):
        print(f'Erro: Filme {num_filme} não existe.')
        return
    if not document_exists('canal', str(num_canal)):
        print(f'Erro: Canal {num_canal} não existe.')
        return

    # Buscar exibições
    exibicoes = db.collection('exibicao').where('filme_ref', '==', db.collection('filme').document(str(num_filme))) \
                                        .where('canal_ref', '==', db.collection('canal').document(str(num_canal))).get()
    if exibicoes:
        for exibicao in exibicoes:
            exibicao_data = exibicao.to_dict()

            # Buscar o nome do filme e do canal usando as referências
            filme_ref = exibicao_data['filme_ref']
            canal_ref = exibicao_data['canal_ref']

            filme_doc = filme_ref.get()  # Obter o documento do filme
            canal_doc = canal_ref.get()  # Obter o documento do canal

            if filme_doc.exists and canal_doc.exists:
                filme_data = filme_doc.to_dict()
                canal_data = canal_doc.to_dict()

                print(f"Exibição encontrada:")
                print(f"Nome do Filme: {filme_data['titulo_original']}")
                print(f"Nome do Canal: {canal_data['nome']}")
                print(f"Data da Exibição: {exibicao_data['data']}")
            else:
                print("Erro: O filme ou canal referenciado não existe.")
    else:
        print('Nenhuma exibição encontrada.')

    return exibicoes


# ------------------- UPDATE -------------------
def update_canal(num_canal, nome=None, sigla=None):
    canal_ref = db.collection('canal').document(str(num_canal))
    updates = {}
    if nome:
        updates['nome'] = nome
    if sigla:
        updates['sigla'] = sigla
    canal_ref.update(updates)
    print(f'Canal {num_canal} atualizado com sucesso!')

def update_filme(num_filme, titulo_original=None, titulo_brasil=None, ano_lancamento=None, pais_origem=None, categoria=None, duracao=None):
    filme_ref = db.collection('filme').document(str(num_filme))
    updates = {}
    if titulo_original:
        updates['titulo_original'] = titulo_original
    if titulo_brasil:
        updates['titulo_brasil'] = titulo_brasil
    if ano_lancamento:
        updates['ano_lancamento'] = ano_lancamento
    if pais_origem:
        updates['pais_origem'] = pais_origem
    if categoria:
        updates['categoria'] = categoria
    if duracao:
        updates['duracao'] = duracao
    filme_ref.update(updates)
    print(f'Filme {num_filme} atualizado com sucesso!')

def update_exibicao(num_filme, num_canal, data, nova_data=None):
    # Verificar integridade: se o filme e o canal existem
    if not document_exists('filme', str(num_filme)):
        print(f'Erro: Filme {num_filme} não existe.')
        return
    if not document_exists('canal', str(num_canal)):
        print(f'Erro: Canal {num_canal} não existe.')
        return

    # Buscar e atualizar a exibição
    exibicoes = db.collection('exibicao').where('filme_ref', '==', db.collection('filme').document(str(num_filme))) \
                                        .where('canal_ref', '==', db.collection('canal').document(str(num_canal))) \
                                        .where('data', '==', data).get()
    if exibicoes:
        for exibicao in exibicoes:
            exibicao_ref = db.collection('exibicao').document(exibicao.id)
            exibicao_ref.update({
                'data': nova_data if nova_data else data  # Atualiza a data se fornecida
            })
            print(f'Exibição atualizada com sucesso! Nova data: {nova_data}')
    else:
        print('Exibição não encontrada.')

# ------------------- DELETE -------------------
def delete_canal(num_canal):
    canal_ref = db.collection('canal').document(str(num_canal))
    canal_ref.delete()
    print(f'Canal {num_canal} deletado com sucesso!')

def delete_filme(num_filme):
    filme_ref = db.collection('filme').document(str(num_filme))
    filme_ref.delete()
    print(f'Filme {num_filme} deletado com sucesso!')

def delete_exibicao(num_filme, num_canal, data):
    # Verificar integridade: se o filme e o canal existem
    if not document_exists('filme', str(num_filme)):
        print(f'Erro: Filme {num_filme} não existe.')
        return
    if not document_exists('canal', str(num_canal)):
        print(f'Erro: Canal {num_canal} não existe.')
        return

    # Buscar e deletar a exibição
    exibicoes = db.collection('exibicao').where('filme_ref', '==', db.collection('filme').document(str(num_filme))) \
                                        .where('canal_ref', '==', db.collection('canal').document(str(num_canal))) \
                                        .where('data', '==', data).get()
    if exibicoes:
        for exibicao in exibicoes:
            db.collection('exibicao').document(exibicao.id).delete()
            print(f'Exibição {num_filme} no canal {num_canal} na data {data} deletada com sucesso!')
    else:
        print('Exibição não encontrada.')

# Função auxiliar para verificar se um documento existe
def document_exists(collection, doc_id):
    doc_ref = db.collection(collection).document(doc_id)
    return doc_ref.get().exists

# Criar canal, filme e exibição
create_canal(1, "Canal Exemplo", "CEX")
create_filme(101, "Titulo Original", "Titulo Brasil", 2023, "Brasil", "Drama", 120)
create_exibicao(101, 1, "2024-09-11T12:00:00")

# Ler dados
read_canal(1)
read_filme(101)
read_exibicao(101, 1)

# Atualizar dados
update_canal(1, nome="Canal Atualizado")
update_filme(101, titulo_original="Novo Titulo")

# Deletar dados
delete_canal(1)
delete_filme(101)
delete_exibicao(101, 1, "2024-09-11T12:00:00")
