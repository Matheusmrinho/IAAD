-- Consulta para obter todos os filmes exibidos por um canal específico
SELECT f.titulo_brasil, c.nome, e.data
FROM exibicao e
JOIN filme f ON e.num_filme = f.num_filme
JOIN canal c ON e.num_canal = c.num_canal
WHERE c.nome = 'HBO';

-- Consulta para contar quantas vezes um filme foi exibido
SELECT f.titulo_brasil, COUNT(e.num_filme) AS numero_exibicoes
FROM exibicao e
JOIN filme f ON e.num_filme = f.num_filme
GROUP BY f.titulo_brasil;

-- Consulta para obter a duração média dos filmes por categoria
SELECT f.categoria, AVG(f.duracao) AS duracao_media
FROM filme f
GROUP BY f.categoria;   

-- Consulta com join para obter o nome do filme, canal e data de exibição (Inner Join)
SELECT f.titulo_brasil, c.nome AS canal_nome, e.data AS data_exibicao
FROM exibicao e
JOIN filme f ON e.num_filme = f.num_filme
JOIN canal c ON e.num_canal = c.num_canal;

-- consulta com having para obter a quantidade de filmes por categoria
SELECT f.categoria, COUNT(f.num_filme) AS quantidade_filmes
FROM filme f
GROUP BY f.categoria
HAVING quantidade_filmes > 2;

-- Script para adicionar a tabela diretor
-- Script para criar a tabela diretor
CREATE TABLE diretor (
    num_diretor INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- Adicionando a coluna num_diretor à tabela filme e definindo como chave estrangeira
ALTER TABLE filme
ADD CONSTRAINT fk_diretor
FOREIGN KEY (num_diretor) REFERENCES diretor(num_diretor);
