--View para obter todos os filmes exibidos por um canal específico
CREATE VIEW filmes_exibidos_por_canal AS view1
SELECT f.titulo_brasil, c.nome, e.data
FROM exibicao e
JOIN filme f ON e.num_filme = f.num_filme
JOIN canal c ON e.num_canal = c.num_canal;
--View para contar quantas vezes um filme foi exibido
CREATE VIEW numero_exibicoes_por_filme AS view2
SELECT f.titulo_brasil, COUNT(e.num_filme) AS numero_exibicoes
FROM exibicao e
JOIN filme f ON e.num_filme = f.num_filme
GROUP BY f.titulo_brasil;
--View para obter a duração média dos filmes por categoria
CREATE VIEW duracao_media_filmes_por_categoria AS view3
SELECT f.categoria, AVG(f.duracao) AS duracao_media
FROM filme f
GROUP BY f.categoria;
--View para obter o nome do filme, canal e data de exibição (Inner Join)
CREATE VIEW nome_filme_canal_data_exibicao AS 
SELECT f.titulo_brasil, c.nome AS canal_nome, e.data AS data_exibicao
FROM exibicao e
JOIN filme f ON e.num_filme = f.num_filme
JOIN canal c ON e.num_canal = c.num_canal;
--View para obter a quantidade de filmes por categoria
CREATE VIEW quantidade_filmes_por_categoria AS view5
SELECT f.categoria, COUNT(f.num_filme) AS quantidade_filmes
FROM filme f
GROUP BY f.categoria
HAVING quantidade_filmes > 2;